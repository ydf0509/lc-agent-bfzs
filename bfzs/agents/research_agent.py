"""研究助手 Agent — 演示如何创建自定义 CompiledGraph 并注册到框架

这是一个多步骤研究 Agent，能够：
1. 根据用户问题制定研究计划
2. 逐步执行研究（调用工具搜集信息）
3. 整合结果并给出结论
"""

from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages


class ResearchState(TypedDict):
    """研究 Agent 的状态定义"""
    messages: Annotated[list, add_messages]
    research_plan: str
    findings: list[str]
    step: int


RESEARCH_SYSTEM_PROMPT = """你是一个专业的研究助手。你的工作流程是：
1. 分析用户的问题，制定研究计划
2. 逐步执行研究计划
3. 整合所有发现，给出完整的分析报告

请用中文回答，条理清晰，有理有据。"""


def build_research_agent(config: dict):
    """构建研究助手的 CompiledGraph。

    Args:
        config: 应用配置字典，用于获取 LLM 配置

    Returns:
        编译后的 LangGraph StateGraph (CompiledGraph)
    """
    provider_conf = {}
    for name, conf in config.get("provider", {}).items():
        if isinstance(conf, dict) and conf.get("models"):
            provider_conf = conf
            break

    model_id = config.get("agent", {}).get("default_model", "gpt-4")
    llm = ChatOpenAI(
        model=model_id,
        base_url=provider_conf.get("base_url") or None,
        api_key=provider_conf.get("api_key", "not-set"),
        temperature=0.3,
    )

    async def plan_node(state: ResearchState) -> dict:
        """制定研究计划"""
        messages = [SystemMessage(content=RESEARCH_SYSTEM_PROMPT)] + state["messages"]
        planning_prompt = (
            "请分析用户的问题，制定一个简洁的研究计划（2-3个步骤）。"
            "只输出计划本身，格式：步骤1: xxx\n步骤2: xxx"
        )
        messages.append(HumanMessage(content=planning_prompt))
        response = await llm.ainvoke(messages)
        return {
            "research_plan": response.content,
            "step": 1,
            "messages": [AIMessage(content=f"📋 研究计划:\n{response.content}")],
        }

    async def research_node(state: ResearchState) -> dict:
        """执行研究"""
        messages = [SystemMessage(content=RESEARCH_SYSTEM_PROMPT)] + state["messages"]
        research_prompt = (
            f"根据研究计划:\n{state['research_plan']}\n\n"
            f"现在执行步骤 {state['step']}，给出你的分析和发现。"
        )
        messages.append(HumanMessage(content=research_prompt))
        response = await llm.ainvoke(messages)
        findings = state.get("findings", []) + [response.content]
        return {
            "findings": findings,
            "step": state["step"] + 1,
            "messages": [AIMessage(content=f"🔍 步骤{state['step']}发现:\n{response.content}")],
        }

    async def summarize_node(state: ResearchState) -> dict:
        """整合总结"""
        messages = [SystemMessage(content=RESEARCH_SYSTEM_PROMPT)] + state["messages"]
        findings_text = "\n\n".join(
            f"发现{i+1}: {f}" for i, f in enumerate(state.get("findings", []))
        )
        summary_prompt = (
            f"请整合以下研究发现，给出一份简洁、结构化的最终报告:\n\n{findings_text}"
        )
        messages.append(HumanMessage(content=summary_prompt))
        response = await llm.ainvoke(messages)
        return {
            "messages": [AIMessage(content=f"📝 研究报告:\n{response.content}")],
        }

    def should_continue_research(state: ResearchState) -> str:
        """判断是否继续研究"""
        plan_lines = [l for l in state.get("research_plan", "").split("\n") if l.strip()]
        total_steps = max(len(plan_lines), 2)
        if state.get("step", 1) > total_steps:
            return "summarize"
        return "research"

    graph = StateGraph(ResearchState)

    graph.add_node("plan", plan_node)
    graph.add_node("research", research_node)
    graph.add_node("summarize", summarize_node)

    graph.set_entry_point("plan")
    graph.add_edge("plan", "research")
    graph.add_conditional_edges("research", should_continue_research, {
        "research": "research",
        "summarize": "summarize",
    })
    graph.add_edge("summarize", END)

    return graph.compile()
