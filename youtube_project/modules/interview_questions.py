from modules.ai_client import generate


class InterviewQuestionGenerator:
    def generate(self, transcript: str, count: int = 10) -> str:
        prompt = (
            f"Generate {count} interview-style questions and brief ideal answers "
            "based on the concepts in this transcript. Format as numbered list."
        )
        return generate(prompt, transcript)
