"""foodo_chatbot — pluggable RAG chatbot module.

Usage:
    from foodo_chatbot import build_chat_service

    svc = build_chat_service()
    conversation = await svc.handle(session_id, user_message, metadata)
    reply = conversation.messages[-1].content
"""
from .container import build_chat_service

__all__ = ["build_chat_service"]
