from fastapi import APIRouter, HTTPException
from ..models import LoginRequest

router = APIRouter(tags=["authentication"])


@router.post("/auth/login")
def login(payload: LoginRequest) -> dict:
    if not payload.email or not payload.password:
        raise HTTPException(status_code=400, detail="请输入邮箱和密码")
    return {"user": {"name": "Demo User", "email": payload.email}, "session": "demo-session"}
