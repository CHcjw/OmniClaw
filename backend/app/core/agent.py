"""LangGraph 主循环"""

from __future__ import annotations

from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    ToolMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from backend.app.core.config import get_settings

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def _build_llm() -> ChatOpenAI:
    """创建 LLM 实例"""
    s = get_settings()
    if not s.openai_api_key:
        raise ValueError("OpenAI API key is not set")
    return ChatOpenAI(
        api_key=s.openai_api_key,
        base_url=s.openai_api_base,
        model=s.model_name,
        temperature=0.2
    )

def _agent_node(state: AgentState) -> AgentState :
    """模型节点：读取消息并生成 AI 回复"""
    llm = _build_llm()
    ai_msg = llm.invoke(state["messages"])
    return {"messages": [ai_msg]}

def _tools_node(state: AgentState) -> AgentState:
    """工具节点：先做占位回注，再接真实工具分类"""
    last = state["messages"][-1]
    if not isinstance(last, AIMessage):
        return {"messages": []}

    tool_calls = getattr(last, "tool_calls", None) or []
    tool_results: list[ToolMessage] = []

    for call in tool_calls:
        tool_results.append(
            ToolMessage(
                content=f"工具占位响应：暂未注册工具 '{call['name']}'，请先注册工具后再使用",
                tool_call_id=call["id"],
            )
        )
    return {"messages": tool_results}

def _route_after_agent(state: AgentState) -> str:
    """路由：若有工具调用则去工具节点，否则结束"""
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and getattr(last, "tool_calls", None):
        return "tools"
    return "end"

def build_graph():
    """构建并编译 Langgraph"""
    graph = StateGraph(AgentState)
    graph.add_node("agent", _agent_node)
    graph.add_node("tools", _tools_node)
    
    graph.set_entry_point("agent")
    graph.add_conditional_edges(
        "agent",
        _route_after_agent,
        {
            "tools": "tools",
            "end": END,
        }
    )
    graph.add_edge("tools", "agent")
    return graph.compile()

def run_once(user_input: str) -> str:
    """最小调用入口，输入一句，返回最后一条 AI 文本"""
    app = build_graph()
    init_messages: list[BaseMessage] = [
        SystemMessage(content="你是我的人工智能助手，协助我完成任务"),
        HumanMessage(content=user_input),
    ]
    result = app.invoke({"messages": init_messages})
    
    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage):
            return msg.content or ""
    return ""