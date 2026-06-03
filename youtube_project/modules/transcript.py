"""Extract YouTube transcripts — yt-dlp primary (works with broken SSL on Windows)."""

import json
import re
import tempfile
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

import requests

from modules.ssl_fix import apply_ssl_fix

apply_ssl_fix()


@dataclass
class _Snippet:
    text: str
    duration: float = 1.0


@dataclass
class _Transcript:
    snippets: list
    language_code: str

    def __iter__(self):
        return iter(self.snippets)


class TranscriptExtractor:
    def extract(self, url: str, language: str = "en") -> dict:
        video_id = self._parse_video_id(url)
        if not video_id:
            return {"success": False, "error": "Invalid YouTube URL."}

        result, error, method = self._fetch_transcript(url, video_id, language)
        if error:
            return {"success": False, "error": error}

        snippets, lang = result
        text = " ".join(s.text for s in snippets)
        title, thumbnail = self._get_metadata(video_id)

        return {
            "success": True,
            "video_id": video_id,
            "url": url,
            "title": title,
            "thumbnail": thumbnail,
            "transcript": text,
            "language": lang,
            "word_count": len(text.split()),
            "duration_estimate": sum(s.duration for s in snippets),
            "fetch_method": method,
        }

    def _fetch_transcript(self, url: str, video_id: str, language: str):
        snippets, lang = self._fetch_ytdlp(url, video_id, language)
        if snippets:
            return (snippets, lang), None, "yt-dlp"

        snippets, lang = self._fetch_transcript_api(video_id, language)
        if snippets:
            return (snippets, lang), None, "youtube-api"

        snippets, lang = self._fetch_timedtext(video_id, language)
        if snippets:
            return (snippets, lang), None, "timedtext"

        return None, "Could not get transcript. Use a video with captions/subtitles enabled.", ""

    def _fetch_ytdlp(self, url: str, video_id: str, language: str):
        try:
            import yt_dlp
        except ImportError:
            return None, language

        opts = {
            "skip_download": True,
            "quiet": True,
            "no_warnings": True,
            "nocheckcertificate": True,
        }

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
        except Exception:
            return None, language

        sub_url = self._pick_subtitle_url(info, language)
        if not sub_url:
            return None, language

        try:
            resp = requests.get(sub_url, timeout=30, verify=False)
            text = self._parse_subtitle_content(resp.text, resp.headers.get("content-type", ""))
            if not text:
                return None, language
            sentences = re.split(r"(?<=[.!?])\s+", text)
            snippets = [_Snippet(s.strip()) for s in sentences if len(s.strip()) > 2]
            return snippets, language
        except Exception:
            return None, language

    def _pick_subtitle_url(self, info: dict, language: str) -> str | None:
        for pool in (info.get("subtitles") or {}, info.get("automatic_captions") or {}):
            for code in (language, "en", "en-US", "en-orig", "a.en"):
                entries = pool.get(code) or pool.get(code.replace("-", "_"))
                if not entries:
                    continue
                for ext in ("json3", "vtt", "srv3", "ttml"):
                    for entry in entries:
                        if entry.get("ext") == ext and entry.get("url"):
                            return entry["url"]
        return None

    def _parse_subtitle_content(self, content: str, content_type: str) -> str:
        content = content.strip()
        if not content:
            return ""

        if "json" in content_type or content.startswith("{"):
            try:
                data = json.loads(content)
                events = data.get("events", [])
                parts = []
                for ev in events:
                    for seg in ev.get("segs", []):
                        t = seg.get("utf8", "").strip()
                        if t and t != "\n":
                            parts.append(t)
                return " ".join(parts)
            except json.JSONDecodeError:
                pass

        lines = []
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("WEBVTT") or "-->" in line or line.isdigit():
                continue
            if re.match(r"^[\d:.]+$", line):
                continue
            lines.append(re.sub(r"<[^>]+>", "", line))
        return " ".join(lines)

    def _fetch_transcript_api(self, video_id: str, language: str):
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            from youtube_transcript_api._errors import (
                NoTranscriptFound,
                TranscriptsDisabled,
                VideoUnavailable,
            )

            fetched = YouTubeTranscriptApi().fetch(
                video_id, languages=[language, "en"]
            )
            snippets = [
                _Snippet(s.text, getattr(s, "duration", 1.0)) for s in fetched
            ]
            return snippets, fetched.language_code
        except Exception:
            return None, language

    def _fetch_timedtext(self, video_id: str, language: str):
        for lang in (language, "en"):
            for kind in ("", "&kind=asr"):
                url = f"https://www.youtube.com/api/timedtext?v={video_id}&lang={lang}{kind}"
                try:
                    resp = requests.get(url, timeout=20, verify=False)
                    if resp.status_code != 200:
                        continue
                    text = self._parse_timedtext_xml(resp.text)
                    if text:
                        sentences = re.split(r"(?<=[.!?])\s+", text)
                        snippets = [_Snippet(s.strip()) for s in sentences if s.strip()]
                        return snippets, lang
                except Exception:
                    continue
        return None, language

    def _parse_timedtext_xml(self, content: str) -> str:
        texts = re.findall(r">([^<]+)</text>", content)
        return " ".join(t.strip() for t in texts if t.strip())

    def _parse_video_id(self, url: str) -> str | None:
        url = url.strip()
        if re.match(r"^[a-zA-Z0-9_-]{11}$", url):
            return url
        parsed = urlparse(url)
        if parsed.hostname in ("youtu.be", "www.youtu.be"):
            return parsed.path.lstrip("/").split("/")[0] or None
        if "youtube.com" in (parsed.hostname or ""):
            if parsed.path == "/watch":
                return parse_qs(parsed.query).get("v", [None])[0]
            match = re.match(r"^/(embed|v|shorts)/([^/?]+)", parsed.path)
            if match:
                return match.group(2)
        return None

    def _get_metadata(self, video_id: str) -> tuple[str, str]:
        thumbnail = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        title = f"Video {video_id}"
        try:
            import yt_dlp

            with yt_dlp.YoutubeDL({"quiet": True, "nocheckcertificate": True}) as ydl:
                info = ydl.extract_info(
                    f"https://www.youtube.com/watch?v={video_id}",
                    download=False,
                )
                title = info.get("title") or title
        except Exception:
            try:
                resp = requests.get(
                    f"https://www.youtube.com/watch?v={video_id}",
                    timeout=15,
                    verify=False,
                )
                match = re.search(r'"title"\s*:\s*"([^"]+)"', resp.text)
                if match:
                    title = bytes(match.group(1), "utf-8").decode("unicode_escape")
            except Exception:
                pass
        return title, thumbnail
