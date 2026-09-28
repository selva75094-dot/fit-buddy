from .config import get_settings


class GeminiService:
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured. Copy .env.example to .env and add your API key.")
        from google import genai

        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.settings = settings

    def generate(self, model: str, prompt: str) -> str:
        response = self.client.models.generate_content(model=model, contents=prompt)
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()
