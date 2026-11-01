# MoinSystems AI Public Website Chatbot

FastAPI + PostgreSQL/pgvector backend (RAG, grounded LLM answers, lead capture, email notification)
and a React + TypeScript widget. No CRM: leads are validated and emailed to `info@moinsystemsai.com`.

Status: **Day 1 complete** (foundation, config, DB, schema, health). See the 8-day milestone doc.

## Requirements
- Python 3.11+ (`.python-version` pins 3.11.9 for Render)
- PostgreSQL 15+ with the `pgvector` extension

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # then edit values; .env is git-ignored
createdb moin_chatbot
alembic upgrade head            # creates the vector extension and all tables
uvicorn app.main:app --reload
```
Check: `curl localhost:8000/api/v1/health` and open `http://localhost:8000/docs`.

## Environment variables
See `.env.example`. Key ones: `DATABASE_URL`, `ALLOWED_ORIGINS`, `LLM_PROVIDER`
(`openai`|`claude`), `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`, `LEAD_NOTIFY_TO`, SMTP settings.
Secrets only ever live in environment variables (Render secrets in production).

## Commands
| Task | Command |
|---|---|
| Run API | `uvicorn app.main:app --reload` |
| Migrate | `alembic upgrade head` |
| New migration | `alembic revision --autogenerate -m "message"` |
| Tests | `pytest` (DB tests skip if Postgres is unreachable) |
| Lint | `ruff check .` |

## Health endpoint
`GET /api/v1/health` returns 200 `{"status":"ok","database":"up"}` or 503 `{"status":"degraded","database":"down"}`.

## Layout
```
app/api/v1/   routes (health now; sessions, chat, leads, feedback later)
app/core/     config (typed settings), logging
app/db/       engine/session, models, alembic migrations
app/rag/ llm/ chat/ leads/ email/ schemas/   later milestones
data/         RAG dataset JSONL (Day 2)
scripts/      ingest.py, evaluate_rag.py (Days 2-3)
tests/        unit, integration, rag, api
widget/       React + TypeScript widget (Day 7)
```

## Tables
`chat_session`, `chat_message`, `lead_submission`, `email_notification`,
`knowledge_document`, `knowledge_chunk` (with `vector(1536)` embedding; dimension is revisited on Day 2
once the embedding model is chosen).
