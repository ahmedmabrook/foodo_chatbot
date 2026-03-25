"""Composition root — the only file that instantiates all concrete adapters.

To swap a technology:
  1. Write a new adapter implementing the relevant port ABC.
  2. Replace the class reference here.
  Nothing else changes.
"""
from functools import lru_cache

from foodo_chatbot.adapters.agents.placeholder_agent import PlaceholderAgent
from foodo_chatbot.adapters.llm.gemini_adapter import GeminiAdapter
from foodo_chatbot.adapters.vector_store.pinecone_adapter import PineconeAdapter
from foodo_chatbot.services.chat_service import ChatService


@lru_cache(maxsize=1)
def build_chat_service() -> ChatService:
    return ChatService(
        llm=GeminiAdapter(),
        vector_store=PineconeAdapter(),
        agent=PlaceholderAgent(),
    )
