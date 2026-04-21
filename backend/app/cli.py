"""CLI 入口骨架。"""

import typer


app = typer.Typer(help="Omni Claw CLI（骨架阶段）")


@app.command()
def run() -> None:
    """主交互入口（占位）。"""
    # 中文注解：这里先保留占位，后续接入 LangGraph 主循环。
    typer.echo("Omni Claw run 命令骨架已就绪")


@app.command()
def config() -> None:
    """配置入口（占位）。"""
    # 中文注解：后续在这里实现配置检查与写入。
    typer.echo("Omni Claw config 命令骨架已就绪")


@app.command()
def monitor() -> None:
    """监控入口（占位）。"""
    # 中文注解：后续在这里接入 JSONL 事件实时监控。
    typer.echo("Omni Claw monitor 命令骨架已就绪")


@app.command()
def tasks() -> None:
    """任务入口（占位）。"""
    # 中文注解：后续在这里接入任务 CRUD 与状态流转。
    typer.echo("Omni Claw tasks 命令骨架已就绪")


def main() -> None:
    """脚本入口。"""
    app()


if __name__ == "__main__":
    main()
