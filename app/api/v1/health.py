from fastapi import APIRouter, Response, status

from app.core.config import get_settings
from app.db.session import check_database

router = APIRouter()


@router.get("/health")
def health(response: Response) -> dict:
    db_ok = check_database()
    if not db_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {
        "status": "ok" if db_ok else "degraded",
        "app": "moinsystems-ai-chatbot",
        "env": get_settings().app_env,
        "database": "up" if db_ok else "down",
    }
