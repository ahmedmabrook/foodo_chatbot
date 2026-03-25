from foodo_chatbot.domain.entities import Conversation, Message


def test_add_message_appends():
    conv = Conversation(session_id="s1")
    conv.add_message("user", "hello")
    assert len(conv.messages) == 1
    assert conv.messages[0].role == "user"
    assert conv.messages[0].content == "hello"


def test_add_message_returns_message():
    conv = Conversation(session_id="s1")
    msg = conv.add_message("assistant", "hi back")
    assert isinstance(msg, Message)
    assert msg.role == "assistant"


def test_last_user_message_returns_most_recent():
    conv = Conversation(session_id="s1")
    conv.add_message("user", "first")
    conv.add_message("assistant", "reply")
    conv.add_message("user", "second")
    msg = conv.last_user_message()
    assert msg is not None
    assert msg.content == "second"


def test_last_user_message_skips_assistant():
    conv = Conversation(session_id="s1")
    conv.add_message("user", "hello")
    conv.add_message("assistant", "world")
    msg = conv.last_user_message()
    assert msg.content == "hello"


def test_last_user_message_returns_none_when_empty():
    conv = Conversation(session_id="s1")
    assert conv.last_user_message() is None


def test_conversation_has_unique_id():
    c1 = Conversation(session_id="s1")
    c2 = Conversation(session_id="s2")
    assert c1.id != c2.id
