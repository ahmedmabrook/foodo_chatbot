from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    pinecone_api_key: str = ""
    pinecone_index_name: str = "foodo-chatbot"

    google_api_key: str = ""
    gemini_model_name: str = "gemini-1.5-flash"
    gemini_embedding_model: str = "models/text-embedding-004"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
