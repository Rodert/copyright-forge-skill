from fastapi import APIRouter
from ..services import rows, task_metrics

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard")
def dashboard() -> dict:
    return {"metrics": task_metrics(), "recent_tasks": rows("SELECT * FROM tasks ORDER BY id DESC LIMIT 5"), "projects": rows("SELECT * FROM projects ORDER BY id")}
