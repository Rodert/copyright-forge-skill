from .db import connect


def rows(query: str, parameters: tuple = ()) -> list[dict]:
    with connect() as db:
        return [dict(row) for row in db.execute(query, parameters).fetchall()]


def log(action: str) -> None:
    with connect() as db:
        db.execute("INSERT INTO activity_logs (action, created_at) VALUES (?, datetime('now'))", (action,))


def task_metrics() -> dict:
    items = rows("SELECT status, priority FROM tasks")
    return {"total": len(items), "done": sum(item["status"] == "已完成" for item in items), "high_priority": sum(item["priority"] == "高" for item in items)}
