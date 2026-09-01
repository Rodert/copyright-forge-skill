import csv
import io
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ..services import rows

router = APIRouter(tags=["exports"])


@router.get("/exports/tasks")
def export_tasks() -> StreamingResponse:
    buffer = io.StringIO(); writer = csv.DictWriter(buffer, fieldnames=["id", "title", "status", "priority", "due_date", "labels"])
    writer.writeheader(); writer.writerows(rows("SELECT id, title, status, priority, due_date, labels FROM tasks ORDER BY id"))
    return StreamingResponse(iter([buffer.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=flowtask-tasks.csv"})
