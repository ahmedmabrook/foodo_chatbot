from pinecone import Pinecone

from foodo_chatbot.config.settings import get_settings
from foodo_chatbot.domain.ports import VectorStorePort


class PineconeAdapter(VectorStorePort):
    """Pinecone vector store adapter. Index must be pre-created (dim=768, metric=cosine)."""

    def __init__(self) -> None:
        settings = get_settings()
        pc = Pinecone(api_key=settings.pinecone_api_key)
        self._index = pc.Index(settings.pinecone_index_name)

    async def upsert(self, vector_id: str, vector: list[float], metadata: dict) -> None:
        self._index.upsert(
            vectors=[{"id": vector_id, "values": vector, "metadata": metadata}]
        )

    async def query(
        self,
        vector: list[float],
        top_k: int = 5,
        filter: dict | None = None,
    ) -> list[dict]:
        kwargs: dict = {"vector": vector, "top_k": top_k, "include_metadata": True}
        if filter:
            kwargs["filter"] = filter
        response = self._index.query(**kwargs)
        return [
            {"id": m.id, "score": m.score, "metadata": m.metadata or {}}
            for m in response.matches
        ]
