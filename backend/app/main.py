"""FastAPI 入口"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.app.api.routes.runtime import router as runtime_router
from backend.app.storage.sqlite import init_db

app = FastAPI(title="Omni Claw API", version="0.1.0")

@asynccontextmanager
async def lifespan(_: FastAPI):
    """应用生命周期：启动时初始化资源"""
    await init_db("workspace/omniclaw.db")
    yield
    # 当前无额外清理逻辑，后续可在这里关闭连接池等资源


app = FastAPI(
    title="Omni Claw API",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/health")
def health() -> dict[str, str]:
    """健康检查接口，用于确认服务是否启动。"""
    return {"status": "ok"}


# 挂载 runtime 路由，形成 /runtime/status 接口
app.include_router(runtime_router)
