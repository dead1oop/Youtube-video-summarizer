import json
import re

from modules.ai_client import generate


class MCQGenerator:
    def generate(self, transcript: str, count: int = 5) -> list[dict]:
        prompt = (
            f"Generate exactly {count} multiple-choice questions from this transcript. "
            "Return ONLY valid JSON array with objects: "
            '{"question": "...", "options": ["A","B","C","D"], "answer": 0} '
            "where answer is the 0-based index of the correct option."
        )
        raw = generate(prompt, transcript)
        return self._parse_mcqs(raw, count)

    def _parse_mcqs(self, raw: str, count: int) -> list[dict]:
        match = re.search(r"\[[\s\S]*\]", raw)
        if match:
            try:
                data = json.loads(match.group())
                if isinstance(data, list) and data:
                    return data[:count]
            except json.JSONDecodeError:
                pass
        return [
            {
                "question": f"Sample question {i + 1} (set GEMINI_API_KEY for real MCQs)",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "answer": 0,
            }
            for i in range(min(count, 3))
        ]
