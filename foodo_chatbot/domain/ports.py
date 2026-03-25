"""Abstract port contracts. Only imports from domain entities — no third-party SDKs."""
from abc import ABC, abstractmethod

from .entities import Conversation


class VectorStorePort(ABC):
    @abstractmethod
    async def upsert(self, vector_id: str, vector: list[float], metadata: dict) -> None:
        ...

    @abstractmethod
    async def query(
        self,
        vector: list[float],
        top_k: int = 5,
        filter: dict | None = None,
    ) -> list[dict]:
        """Returns list of {id, score, metadata} dicts."""
        ...


class LLMPort(ABC):
    @abstractmethod
    async def complete(self, prompt: str, system_prompt: str = "") -> str:
        ...

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        ...


class AgentPort(ABC):
    @abstractmethod
    async def run(self, conversation: Conversation) -> str:
        """Invoke the agent pipeline; returns the assistant reply string."""
        ...


class ChatUseCase(ABC):
    @abstractmethod
    async def handle(
        self,
        session_id: str,
        user_message: str,
        metadata: dict,
    ) -> Conversation:
        ...
