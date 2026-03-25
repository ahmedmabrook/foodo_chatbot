# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project
`foodo_chatbot` is an installable Python package (not a server) that `foodo.ai/api` imports directly. It provides RAG retrieval + agent orchestration as Python classes using a Layered Port/Adapter architecture.

## Commands

```bash
# Setup
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && pip install -e .

# Tests
pytest tests/unit/ -v          # unit tests — no network calls
pytest tests/integration/ -v   # integration tests — mocked adapters
pytest -v                      # all tests

# Single test
pytest tests/unit/test_entities.py -v

# Smoke test (requires .env with real keys)
python -c "
import asyncio
from foodo_chatbot import build_chat_service
async def main():
    svc = build_chat_service()
    conv = await svc.handle('test-session', 'hello', {})
    print(conv.messages[-1].content)
asyncio.run(main())
"
```

## Architecture

Three layers — dependency arrows always point inward (toward `domain/`):

```
adapters/   — concrete third-party implementations (Pinecone, Gemini, agents)
    ↓
services/   — use-case orchestration; imports domain/ only
    ↓
domain/     — pure Python entities + abstract port contracts (ABCs); zero external imports
```

**Composition root**: `foodo_chatbot/container.py` is the only file that instantiates all concrete adapters and wires them into `ChatService`. Swap a technology by writing a new adapter that implements the relevant port ABC, then update `container.py`.

**Public API**: `from foodo_chatbot import build_chat_service`

## Ports (abstract contracts in `domain/ports.py`)
- `LLMPort` — `embed(text) -> list[float]`, `complete(prompt, system_prompt) -> str`
- `VectorStorePort` — `upsert(id, vector, metadata)`, `query(vector, top_k, filter) -> list[dict]`
- `AgentPort` — `run(conversation) -> str`
- `ChatUseCase` — `handle(session_id, user_message, metadata) -> Conversation`

## Current Adapters
- **LLM**: `GeminiAdapter` (`google-generativeai`, model: `gemini-1.5-flash`, embeddings: `text-embedding-004` dim=768)
- **Vector Store**: `PineconeAdapter` (index dimension must be 768, metric: cosine)
- **Agent**: `PlaceholderAgentAdapter` — echo skeleton, replace in a future branch

## Environment Variables
Copy `.env.example` to `.env` and fill in:
- `PINECONE_API_KEY`, `PINECONE_INDEX_NAME` (default: `foodo-chatbot`)
- `GOOGLE_API_KEY`, `GEMINI_MODEL_NAME`, `GEMINI_EMBEDDING_MODEL`

Pinecone index must be created manually (dim=768, metric=cosine) before real usage.

## Installing into foodo.ai
```bash
# from foodo.ai/api directory:
pip install -e ../foodo_chatbot
```
```python
from foodo_chatbot import build_chat_service
svc = build_chat_service()
conv = await svc.handle(session_id, user_message, metadata)
```
