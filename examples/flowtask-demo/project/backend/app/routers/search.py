from fastapi import APIRouter
from ..services import rows

router = APIRouter(tags=["search"])


@router.get("/search")
def search(q: str) -> dict:
    return {"projects": rows("SELECT * FROM projects WHERE name LIKE ?", (f"%{q}%",)), "tasks": rows("SELECT * FROM tasks WHERE title LIKE ? OR labels LIKE ?", (f"%{q}%", f"%{q}%"))}
