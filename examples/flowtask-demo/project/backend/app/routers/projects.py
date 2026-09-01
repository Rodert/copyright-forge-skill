from fastapi import APIRouter
from ..db import connect
from ..models import ProjectInput
from ..services import log, rows

router = APIRouter(tags=["projects"])


@router.get("/projects")
def list_projects() -> list[dict]:
    return rows("SELECT * FROM projects ORDER BY id DESC")


@router.post("/projects")
def create_project(payload: ProjectInput) -> dict:
    with connect() as db:
        cursor = db.execute("INSERT INTO projects (name, status, color) VALUES (?, ?, ?)", (payload.name, payload.status, payload.color))
    log(f"创建项目：{payload.name}")
    return {"id": cursor.lastrowid, **payload.model_dump()}
