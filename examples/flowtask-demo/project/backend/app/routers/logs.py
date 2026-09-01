from fastapi import APIRouter
from ..services import rows

router = APIRouter(tags=["operation-logs"])


@router.get("/operation-logs")
def operation_logs() -> list[dict]:
    return rows("SELECT * FROM activity_logs ORDER BY id DESC LIMIT 50")
