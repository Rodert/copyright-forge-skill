from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import initialize
from .routers import auth, dashboard, exports, labels, logs, priorities, projects, search, settings, stats, statuses, tasks

app = FastAPI(title="FlowTask API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
def startup() -> None:
    initialize()


for router in (auth.router, dashboard.router, projects.router, tasks.router, statuses.router, priorities.router, labels.router, search.router, stats.router, logs.router, settings.router, exports.router):
    app.include_router(router, prefix="/api")
