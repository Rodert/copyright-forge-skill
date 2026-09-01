from fastapi import APIRouter
from ..services import rows, task_metrics

router = APIRouter(tags=["statistics"])


@router.get("/statistics")
def statistics() -> dict:
    return {"metrics": task_metrics(), "by_status": rows("SELECT status, COUNT(*) AS count FROM tasks GROUP BY status"), "by_priority": rows("SELECT priority, COUNT(*) AS count FROM tasks GROUP BY priority")}
