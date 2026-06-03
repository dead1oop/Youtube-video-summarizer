from textblob import TextBlob


class SentimentAnalyzer:
    def analyze(self, transcript: str) -> dict:
        blob = TextBlob(transcript[:50000])
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        if polarity > 0.1:
            label = "Positive"
        elif polarity < -0.1:
            label = "Negative"
        else:
            label = "Neutral"

        sentences = blob.sentences[:20] if blob.sentences else []
        highlights = []
        for sent in sentences:
            p = sent.sentiment.polarity
            if abs(p) > 0.3:
                highlights.append({"text": str(sent)[:200], "polarity": round(p, 3)})

        return {
            "label": label,
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3),
            "highlights": highlights[:10],
        }
