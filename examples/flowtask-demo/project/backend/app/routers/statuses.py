from fastapi import APIRouter

router = APIRouter(tags=["task-status"])


@router.get("/task-statuses")
def list_statuses() -> list[dict]:
    return [{"name": "待办", "order": 1}, {"name": "进行中", "order": 2}, {"name": "已完成", "order": 3}]
