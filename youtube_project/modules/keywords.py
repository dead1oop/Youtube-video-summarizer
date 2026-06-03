import re

try:
    import yake
except ImportError:
    yake = None


class KeywordExtractor:
    def extract(self, transcript: str, top_n: int = 15) -> list[dict]:
        if yake:
            kw = yake.KeywordExtractor(lan="en", n=1, top=top_n)
            keywords = kw.extract_keywords(transcript[:30000])
            return [{"keyword": k, "score": round(s, 4)} for k, s in keywords]

        words = re.findall(r"\b[a-zA-Z]{5,}\b", transcript.lower())
        stop = {
            "about", "after", "again", "being", "could", "every", "first",
            "going", "really", "right", "should", "their", "there", "these",
            "think", "those", "through", "video", "watch", "would", "youtube",
        }
        freq: dict[str, int] = {}
        for w in words:
            if w not in stop:
                freq[w] = freq.get(w, 0) + 1
        ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return [{"keyword": k, "score": float(v)} for k, v in ranked]
