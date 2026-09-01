# FlowTask

FlowTask 是一个个人任务与项目管理系统示例。前端提供项目、任务、标签和统计视图；后端使用 FastAPI 和 SQLite 提供 JSON API，并保存项目、任务、标签、操作日志与用户设置。

## Run

```bash
cd backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8000`.
