"""Placeholder agent adapter — echo skeleton. Replace with real agent logic in a future branch."""
from foodo_chatbot.domain.entities import Conversation
from foodo_chatbot.domain.ports import AgentPort


class PlaceholderAgent(AgentPort):
    async def run(self, conversation: Conversation) -> str:
        last = conversation.last_user_message()
        if last:
            return f"[placeholder] Echo: {last.content}"
        return "[placeholder] No message received."
