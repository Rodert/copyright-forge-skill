from fastapi import APIRouter

router = APIRouter(tags=["priorities"])


@router.get("/priorities")
def list_priorities() -> list[dict]:
    return [{"name": "高", "color": "#c0392b"}, {"name": "中", "color": "#e67e22"}, {"name": "低", "color": "#2f6756"}]
