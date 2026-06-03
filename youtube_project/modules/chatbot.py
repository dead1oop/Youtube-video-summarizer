from modules.ai_client import generate


class VideoChatbot:
    def __init__(self, transcript: str, title: str = ""):
        self.transcript = transcript
        self.title = title

    def ask(self, question: str) -> str:
        prompt = (
            f"You are a helpful tutor answering questions about the video '{self.title}'. "
            f"Answer based only on the transcript. Question: {question}"
        )
        return generate(prompt, self.transcript)
