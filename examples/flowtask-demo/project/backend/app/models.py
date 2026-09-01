from typing import Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class ProjectInput(BaseModel):
    name: str
    status: str = "规划中"
    color: str = "#2f6756"


class TaskInput(BaseModel):
    title: str
    project_id: Optional[int] = None
    status: str = "待办"
    priority: str = "中"
    due_date: Optional[str] = None
    labels: str = ""


class LabelInput(BaseModel):
    name: str
    color: str = "#3867d6"


class SettingInput(BaseModel):
    value: str
