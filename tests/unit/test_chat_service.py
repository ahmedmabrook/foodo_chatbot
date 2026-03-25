from unittest.mock import AsyncMock

import pytest

from foodo_chatbot.services.chat_service import ChatService


@pytest.fixture
def fake_llm():
    llm = AsyncMock()
    llm.embed.return_value = [0.1] * 768
    llm.complete.return_value = "mocked completion"
    return llm


@pytest.fixture
def fake_vector_store():
    vs = AsyncMock()
    vs.query.return_value = []
    return vs


@pytest.fixture
def fake_agent():
    agent = AsyncMock()
    agent.run.return_value = "placeholder reply"
    return agent


@pytest.fixture
def service(fake_llm, fake_vector_store, fake_agent):
    return ChatService(llm=fake_llm, vector_store=fake_vector_store, agent=fake_agent)


async def test_handle_returns_two_messages(service):
    conv = await service.handle("s1", "What should I eat?", {})
    assert len(conv.messages) == 2
    assert conv.messages[0].role == "user"
    assert conv.messages[1].role == "assistant"


async def test_handle_assistant_reply_matches_agent_output(service, fake_agent):
    fake_agent.run.return_value = "eat more protein"
    conv = await service.handle("s1", "advice?", {})
    assert conv.messages[-1].content == "eat more protein"


async def test_handle_calls_embed_with_user_message(service, fake_llm):
    await service.handle("s1", "hello", {})
    fake_llm.embed.assert_called_once_with("hello")


async def test_handle_calls_vector_store_query(service, fake_vector_store):
    await service.handle("s1", "hello", {})
    fake_vector_store.query.assert_called_once()


async def test_handle_calls_agent_run(service, fake_agent):
    await service.handle("s1", "hello", {})
    fake_agent.run.assert_called_once()


async def test_handle_preserves_session_id(service):
    conv = await service.handle("my-session", "hi", {})
    assert conv.session_id == "my-session"


async def test_handle_attaches_metadata(service):
    conv = await service.handle("s1", "hi", {"trainer_id": "t42"})
    assert conv.metadata["trainer_id"] == "t42"
