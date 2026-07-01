"""bfzs 应用入口 — 演示如何使用 lc-agent 框架开发自定义 Agent 应用"""

import argparse
from pathlib import Path
from bfzs import init_loggers

def main():
    parser = argparse.ArgumentParser(description="lc-agent-bfzs 自定义 Agent 应用")
    parser.add_argument("--config", "-c", help="配置文件路径", default=None)
    parser.add_argument("--host", default="127.0.0.1", help="服务器地址")
    parser.add_argument("--port", "-p", type=int, default=8001, help="服务器端口")
    args = parser.parse_args()

    config_path = args.config or str(Path(__file__).parent.parent / "config.jsonc")

    from lc_agent import LcAgentApp, load_config

    config = load_config(config_path=config_path)

    # 导入框架内置通用工具
    import lc_agent.tools.contrib_tools.get_time  # noqa: F401
    import lc_agent.tools.contrib_tools.ask_user_tool  # noqa: F401

    # 导入自定义工具（导入即注册到全局 ToolRegistry）
    import bfzs.tools.file_tools  # noqa: F401
    import bfzs.tools.data_tools  # noqa: F401

    app = LcAgentApp(config, host=args.host, port=args.port)

    # 注册自定义 CompiledGraph Agent
    from bfzs.agents.research_agent import build_research_agent

    research_graph = build_research_agent(config)
    app.add_agent(
        name="research_assistant",
        graph=research_graph,
        description="研究助手：擅长多步骤信息收集、整理和分析",
    )

    app.run()


if __name__ == "__main__":
    main()
