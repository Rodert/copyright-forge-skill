from fastapi import APIRouter
from ..db import connect
from ..models import LabelInput
from ..services import rows

router = APIRouter(tags=["labels"])


@router.get("/labels")
def list_labels() -> list[dict]:
    return rows("SELECT * FROM labels ORDER BY name")


@router.post("/labels")
def create_label(payload: LabelInput) -> dict:
    with connect() as db:
        cursor = db.execute("INSERT INTO labels (name, color) VALUES (?, ?)", (payload.name, payload.color))
    return {"id": cursor.lastrowid, **payload.model_dump()}
