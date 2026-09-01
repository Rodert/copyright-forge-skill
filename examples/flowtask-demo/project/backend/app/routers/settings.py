from fastapi import APIRouter
from ..db import connect
from ..models import SettingInput
from ..services import rows

router = APIRouter(tags=["settings"])


@router.get("/settings")
def list_settings() -> list[dict]:
    return rows("SELECT * FROM settings ORDER BY key")


@router.put("/settings/{key}")
def update_setting(key: str, payload: SettingInput) -> dict:
    with connect() as db:
        db.execute("INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, payload.value))
    return {"key": key, "value": payload.value}
