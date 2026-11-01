"""Needs a running Postgres with pgvector at DATABASE_URL (skipped otherwise)."""
import pytest
from sqlalchemy import text

from app.db.session import check_database, engine

pytestmark = pytest.mark.skipif(not check_database(), reason="database not reachable")

TABLES = {
    "chat_session", "chat_message", "lead_submission",
    "email_notification", "knowledge_document", "knowledge_chunk",
}


def test_schema_tables_exist():
    with engine.connect() as c:
        rows = c.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public'"))
        assert TABLES <= {r[0] for r in rows}


def test_pgvector_enabled():
    with engine.connect() as c:
        assert c.execute(text("SELECT 1 FROM pg_extension WHERE extname='vector'")).scalar() == 1


def test_health_endpoint_reports_db_up(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200 and r.json()["database"] == "up"
