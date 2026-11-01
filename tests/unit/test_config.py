from app.core.config import Settings


def test_cors_origins_parsed():
    s = Settings(allowed_origins="https://a.com, https://b.com")
    assert s.cors_origins == ["https://a.com", "https://b.com"]


def test_database_url_comes_from_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://u:p@h:5432/d")
    assert Settings().database_url.endswith("@h:5432/d")
