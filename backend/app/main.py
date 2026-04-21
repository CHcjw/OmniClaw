"""FastAPI 入口（骨架占位）。"""

from fastapi import FastAPI

from backend.app.api.routes.runtime import router as runtime_router


app = FastAPI(title="Omni Claw API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """健康检查接口，用于确认服务是否启动。"""
    return {"status": "ok"}


# 中文注解：挂载 runtime 路由，形成 /runtime/status 接口。
app.include_router(runtime_router)
