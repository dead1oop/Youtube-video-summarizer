from modules.ai_client import generate


class NotesGenerator:
    def generate(self, transcript: str) -> str:
        prompt = (
            "Create structured study notes from this transcript. "
            "Use headings, bullet points, definitions, and key formulas if any."
        )
        return generate(prompt, transcript)
