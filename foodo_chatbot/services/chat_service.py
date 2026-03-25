"""ChatService — concrete use case. Imports domain only; no adapter or SDK imports."""
from foodo_chatbot.domain.entities import Conversation
from foodo_chatbot.domain.ports import AgentPort, ChatUseCase, LLMPort, VectorStorePort


class ChatService(ChatUseCase):
    def __init__(
        self,
        llm: LLMPort,
        vector_store: VectorStorePort,
        agent: AgentPort,
    ) -> None:
        self._llm = llm
        self._vector_store = vector_store
        self._agent = agent

    async def handle(
        self,
        session_id: str,
        user_message: str,
        metadata: dict,
    ) -> Conversation:
        conversation = Conversation(session_id=session_id, metadata=metadata)
        conversation.add_message("user", user_message)

        # 1. Embed the user message for retrieval
        embedding = await self._llm.embed(user_message)

        # 2. Retrieve relevant context from vector store
        await self._vector_store.query(embedding, top_k=5)

        # 3. Delegate to agent (placeholder returns echo; real logic added later)
        reply = await self._agent.run(conversation)

        conversation.add_message("assistant", reply)
        return conversation
