from modules.ai_client import generate


class Summarizer:
    def summarize(self, transcript: str, style: str = "concise") -> str:
        prompts = {
            "concise": "Write a concise bullet-point summary of this video transcript.",
            "detailed": "Write a detailed structured summary with sections and key takeaways.",
            "eli5": "Explain the main ideas from this transcript in simple terms (ELI5).",
        }
        prompt = prompts.get(style, prompts["concise"])
        return generate(prompt, transcript)
