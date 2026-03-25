"""Integration tests: wires the full container with mocked adapters — no real Pinecone or Gemini calls."""
from unittest.mock import AsyncMock, patch

import pytest

from foodo_chatbot.services.chat_service import ChatService


@pytest.fixture(autouse=True)
def mock_adapters(monkeypatch):
    """Patch all concrete adapters before the container is built."""
    fake_llm = AsyncMock()
    fake_llm.embed.return_value = [0.0] * 768
    fake_llm.complete.return_value = "mocked"

    fake_vs = AsyncMock()
    fake_vs.query.return_value = []

    fake_agent = AsyncMock()
    fake_agent.run.return_value = "[placeholder] Echo: hello"

    monkeypatch.setattr(
        "foodo_chatbot.adapters.llm.gemini_adapter.GeminiAdapter.__init__",
        lambda self: None,
    )
    monkeypatch.setattr(
        "foodo_chatbot.adapters.vector_store.pinecone_adapter.PineconeAdapter.__init__",
        lambda self: None,
    )

    with (
        patch("foodo_chatbot.container.GeminiAdapter", return_value=fake_llm),
        patch("foodo_chatbot.container.PineconeAdapter", return_value=fake_vs),
        patch("foodo_chatbot.container.PlaceholderAgent", return_value=fake_agent),
    ):
        yield fake_llm, fake_vs, fake_agent


async def test_build_chat_service_returns_chat_service(mock_adapters):
    from foodo_chatbot.container import build_chat_service

    build_chat_service.cache_clear()
    svc = build_chat_service()
    assert isinstance(svc, ChatService)


async def test_full_handle_pipeline(mock_adapters):
    from foodo_chatbot.container import build_chat_service

    build_chat_service.cache_clear()
    svc = build_chat_service()
    conv = await svc.handle("session-1", "hello", {})

    assert conv.session_id == "session-1"
    assert len(conv.messages) == 2
    assert conv.messages[0].role == "user"
    assert conv.messages[1].role == "assistant"


async def test_public_api_import():
    from foodo_chatbot import build_chat_service

    build_chat_service.cache_clear()
    svc = build_chat_service()
    assert svc is not None
