"""Shared AI client with Gemini support and local extractive fallback."""

import os
import re
from collections import Counter

from modules.env_loader import load_env

load_env()

GEMINI_MODELS = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
]

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "is", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "do", "does", "did", "will", "would", "could", "should", "may",
    "might", "that", "this", "these", "those", "it", "its", "i", "you", "he",
    "she", "we", "they", "them", "their", "what", "which", "who", "when",
    "where", "why", "how", "all", "each", "every", "both", "few", "more",
    "most", "other", "some", "such", "no", "not", "only", "own", "same", "so",
    "than", "too", "very", "just", "also", "now", "about", "into", "through",
    "during", "before", "after", "above", "below", "up", "down", "out", "off",
    "over", "under", "again", "further", "then", "once", "here", "there",
    "because", "until", "while", "can", "your", "our", "my", "me", "him",
    "her", "his", "from", "with", "as", "by", "if", "um", "uh", "like", "yeah",
}


def _get_api_key() -> str | None:
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def _extract_response_text(response) -> str:
    try:
        text = response.text
        if text and text.strip():
            return text.strip()
    except (ValueError, AttributeError):
        pass

    parts = []
    for candidate in getattr(response, "candidates", []) or []:
        content = getattr(candidate, "content", None)
        if not content:
            continue
        for part in getattr(content, "parts", []) or []:
            if hasattr(part, "text") and part.text:
                parts.append(part.text)
    return "\n".join(parts).strip()


def _call_gemini(full_prompt: str) -> tuple[str | None, str | None]:
    api_key = _get_api_key()
    if not api_key:
        return None, "No API key set. Add GEMINI_API_KEY to .env for AI summaries."

    import google.generativeai as genai

    genai.configure(api_key=api_key)
    last_error = None

    for model_name in GEMINI_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                full_prompt,
                generation_config={"temperature": 0.4, "max_output_tokens": 2048},
            )
            text = _extract_response_text(response)
            if text:
                return text, None
            last_error = f"{model_name}: empty response"
        except Exception as exc:
            last_error = f"{model_name}: {exc}"

    return None, last_error or "All Gemini models failed."


def generate(prompt: str, transcript: str, max_chars: int = 30000) -> str:
    """Generate text from a prompt plus transcript context."""
    text = transcript.strip()
    if not text:
        return "No transcript available. Analyze a video with captions enabled first."

    excerpt = text[:max_chars]
    full_prompt = f"{prompt}\n\n--- TRANSCRIPT ---\n{excerpt}"

    ai_text, error = _call_gemini(full_prompt)
    if ai_text:
        return ai_text

    if "summar" in prompt.lower():
        summary = _extractive_summary(text)
        if error:
            return f"{summary}\n\n---\n*Local summary (AI unavailable: {error})*"
        return summary

    if error:
        return f"*AI unavailable: {error}*"
    return "Set GEMINI_API_KEY in a `.env` file for AI-powered features."


def _extractive_summary(text: str, num_sentences: int = 10) -> str:
    """Build a bullet-point summary without an API key."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s.strip() for s in sentences if len(s.strip()) > 25]
    if not sentences:
        chunk = text[:800].strip()
        return f"- {chunk}" if chunk else "No transcript content to summarize."

    word_freq: Counter[str] = Counter()
    for sentence in sentences:
        for word in re.findall(r"\b[a-zA-Z]{3,}\b", sentence.lower()):
            if word not in STOPWORDS:
                word_freq[word] += 1

    if not word_freq:
        picked = sentences[:num_sentences]
    else:
        scores = []
        for i, sentence in enumerate(sentences):
            words = re.findall(r"\b[a-zA-Z]{3,}\b", sentence.lower())
            content_words = [w for w in words if w not in STOPWORDS]
            if not content_words:
                continue
            score = sum(word_freq[w] for w in content_words) / len(content_words)
            scores.append((score, i, sentence))

        scores.sort(reverse=True)
        top_indices = sorted(idx for _, idx, _ in scores[:num_sentences])
        picked = [sentences[i] for i in top_indices]

    bullets = "\n".join(f"- {s}" for s in picked)
    return f"**Summary** (extracted from transcript)\n\n{bullets}"
