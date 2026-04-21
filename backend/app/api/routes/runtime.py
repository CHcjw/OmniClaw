"""运行时路由骨架"""

# 接入运行时状态与控制接口
from fastapi import APIRouter
# 统一管理“运行时”相关的 HTTP 接口
router = APIRouter(prefix="/runtime", tags=["runtime"])

@router.get("/status")
def get_runtime_status() -> dict[str, str]:
    """返回运行时占位状态"""
    # 后续替换成真实状态（心跳、任务队列、模型通道等）
    return {"status": "idle", "message": "runtime router is ready"}