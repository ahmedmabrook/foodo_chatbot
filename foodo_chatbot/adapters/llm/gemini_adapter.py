import google.generativeai as genai

from foodo_chatbot.config.settings import get_settings
from foodo_chatbot.domain.ports import LLMPort


class GeminiAdapter(LLMPort):
    """Google AI Studio (Gemini) LLM adapter."""

    def __init__(self) -> None:
        settings = get_settings()
        genai.configure(api_key=settings.google_api_key)
        self._model = genai.GenerativeModel(settings.gemini_model_name)
        self._embedding_model = settings.gemini_embedding_model

    async def complete(self, prompt: str, system_prompt: str = "") -> str:
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = self._model.generate_content(full_prompt)
        return response.text

    async def embed(self, text: str) -> list[float]:
        result = genai.embed_content(
            model=self._embedding_model,
            content=text,
            task_type="retrieval_query",
        )
        return result["embedding"]
