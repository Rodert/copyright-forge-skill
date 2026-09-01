from typing import Optional

from fastapi import APIRouter
from ..db import connect
from ..models import TaskInput
from ..services import log, rows

router = APIRouter(tags=["tasks"])


@router.get("/tasks")
def list_tasks(status: Optional[str] = None, q: Optional[str] = None) -> list[dict]:
    query, values = "SELECT * FROM tasks WHERE 1=1", []
    if status:
        query += " AND status = ?"; values.append(status)
    if q:
        query += " AND title LIKE ?"; values.append(f"%{q}%")
    return rows(query + " ORDER BY id DESC", tuple(values))


@router.post("/tasks")
def create_task(payload: TaskInput) -> dict:
    with connect() as db:
        cursor = db.execute("INSERT INTO tasks (project_id, title, status, priority, due_date, labels) VALUES (?, ?, ?, ?, ?, ?)", (payload.project_id, payload.title, payload.status, payload.priority, payload.due_date, payload.labels))
    log(f"创建任务：{payload.title}")
    return {"id": cursor.lastrowid, **payload.model_dump()}
