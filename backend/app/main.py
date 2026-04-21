"""FastAPI 入口（骨架占位）。"""

from fastapi import FastAPI


app = FastAPI(title="Omni Claw API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """健康检查接口，用于确认服务是否启动。"""
    return {"status": "ok"}
