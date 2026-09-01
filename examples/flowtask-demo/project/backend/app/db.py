import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parents[1] / "flowtask.db"


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize() -> None:
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT NOT NULL, status TEXT NOT NULL, color TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, project_id INTEGER, title TEXT NOT NULL, status TEXT NOT NULL, priority TEXT NOT NULL, due_date TEXT, labels TEXT NOT NULL DEFAULT '');
        CREATE TABLE IF NOT EXISTS labels (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, color TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS activity_logs (id INTEGER PRIMARY KEY, action TEXT NOT NULL, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        """)
        if not db.execute("SELECT 1 FROM projects LIMIT 1").fetchone():
            db.executemany("INSERT INTO projects (name, status, color) VALUES (?, ?, ?)", [("FlowTask 产品迭代", "进行中", "#2f6756"), ("个人学习计划", "规划中", "#b76c37")])
            db.executemany("INSERT INTO tasks (project_id, title, status, priority, due_date, labels) VALUES (?, ?, ?, ?, ?, ?)", [(1, "完成任务筛选", "进行中", "高", "2026-09-18", "前端,体验"), (1, "编写 API 文档", "待办", "中", "2026-09-21", "后端"), (2, "学习 FastAPI", "已完成", "低", "2026-09-10", "学习")])
            db.executemany("INSERT INTO labels (name, color) VALUES (?, ?)", [("前端", "#3867d6"), ("后端", "#7c4dff"), ("体验", "#e67e22"), ("学习", "#16a085")])
            db.executemany("INSERT INTO activity_logs (action, created_at) VALUES (?, ?)", [("创建了 FlowTask 产品迭代项目", "2026-09-01 09:00"), ("更新了任务筛选", "2026-09-01 10:30")])
            db.execute("INSERT INTO settings (key, value) VALUES ('theme', 'system')")
