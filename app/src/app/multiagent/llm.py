import os
from typing import Optional

from langchain_core.language_models.chat_models import BaseChatModel  # type: ignore[import-not-found]  # isort: skip
from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore[import-not-found]  # isort: skip


class GoogleGenAILLM(ChatGoogleGenerativeAI):
    def __init__(
        self,
        model: Optional[str] = None,
        google_api_key: Optional[str] = None,
        **kwargs,
    ):
        model = model or os.getenv("DEFAULT_GOOGLEGENAI_MODEL")
        google_api_key = google_api_key or os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        super().__init__(model=model, google_api_key=google_api_key, **kwargs)
        self.google_api_key = google_api_key


class LLMFactory:
    _providers = {
        "google-genai": GoogleGenAILLM,
    }

    @classmethod
    def get_model(
        cls,
        model_provider: str,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> BaseChatModel:
        provider_key = model_provider.lower()
        if provider_key not in cls._providers:
            raise ValueError(f"Unsupported model provider: {model_provider}")
        provider_cls = cls._providers[provider_key]
        return provider_cls(model=model, google_api_key=api_key)
