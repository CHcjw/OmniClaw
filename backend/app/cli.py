"""CLI 入口骨架"""

import typer
from rich.console import Console
from rich.table import Table

from backend.app.core.config import get_settings, mask_secret

app = typer.Typer(help="Omni Claw CLI（骨架阶段）")

@app.command()
def run() -> None:
    """主交互入口（占位）"""
    # 这里先保留占位，后续接入 LangGraph 主循环。
    typer.echo("Omni Claw run 命令骨架已就绪")


@app.command()
def config() -> None:
    """配置检查入口"""
    settings = get_settings()
    console = Console()

    table = Table(title="Omni Claw 配置摘要")
    table.add_column("配置项", style="cyan")
    table.add_column("当前值", style="green")

    table.add_row("app_env", settings.app_env)
    table.add_row("provider", settings.provider)
    table.add_row("model_name", settings.model_name)
    table.add_row("workspace_dir", settings.workspace_dir)
    table.add_row("logs_dir", settings.logs_dir)
    table.add_row("tasks_dir", settings.tasks_dir)
    table.add_row("db_path", settings.db_path)
    table.add_row("openai_api_key", mask_secret(settings.openai_api_key))
    table.add_row("anthropic_api_key", mask_secret(settings.anthropic_api_key))

    console.print(table)

@app.command()
def monitor() -> None:
    """监控入口（占位）"""
    # 后续在这里接入 JSONL 事件实时监控。
    typer.echo("Omni Claw monitor 命令骨架已就绪")


@app.command()
def tasks() -> None:
    """任务入口（占位）"""
    # 后续在这里接入任务 CRUD 与状态流转。
    typer.echo("Omni Claw tasks 命令骨架已就绪")


def main() -> None:
    """脚本入口"""
    app()


if __name__ == "__main__":
    main()
