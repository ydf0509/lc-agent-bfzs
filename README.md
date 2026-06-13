# lc-agent-bfzs

基于 [lc-agent](../lc-agent) 框架开发的自定义 Agent 应用示例。

## 项目结构

```
lc-agent-bfzs/
├── pyproject.toml          # 项目配置，依赖 lc-agent
├── config.jsonc            # 运行时配置
├── bfzs/                   # Python 包
│   ├── main.py             # 入口：配置 → 注册工具 → 注册Agent → 启动
│   ├── tools/              # 自定义工具（按分组）
│   │   ├── file_tools.py   # [file_mgmt] 文件管理
│   │   └── data_tools.py   # [data_analysis] 数据分析
│   └── agents/             # 自定义 CompiledGraph Agent
│       └── research_agent.py   # 研究助手（多步骤 LangGraph）
└── myskills/               # 自定义 Skills（SKILL.md 格式）
    ├── code-review/
    │   └── SKILL.md        # [开发辅助] 代码审查
    └── doc-summarize/
        └── SKILL.md        # [文本处理] 文档摘要
```

## 安装运行

```bash
# 前提：已安装 lc-agent 框架
pip install -e D:\codes\lc-agent

# 安装本项目
pip install -e .

# 启动（默认端口 8001）
bfzs
# 或
python -m bfzs.main --port 8001

# 访问 Web UI
# http://127.0.0.1:8001
```

## 使用方式说明

本项目演示了 lc-agent 框架的三种核心扩展方式：

### 1. 自定义工具

使用 `@tool` 装饰器，导入即自动注册到全局 ToolRegistry：

```python
from lc_agent import tool

@tool(group="file_mgmt", group_description="文件管理")
def read_file(file_path: str) -> str:
    """读取文件内容"""
    ...
```

### 2. 自定义 Agent（CompiledGraph）

使用 LangGraph 构建自定义 StateGraph，通过 `app.add_agent()` 注册：

```python
from langgraph.graph import StateGraph, END

graph = StateGraph(MyState)
graph.add_node("plan", plan_node)
graph.add_node("execute", execute_node)
graph.set_entry_point("plan")
graph.add_edge("plan", "execute")
graph.add_edge("execute", END)

compiled = graph.compile()
app.add_agent("my_agent", compiled, description="我的Agent")
```

### 3. 自定义 Skills

在 `myskills/` 目录下创建 SKILL.md，遵循 agentskills.io 规范：

```yaml
---
name: my-skill          # 文件夹名必须与此一致
description: 技能描述
metadata:
  group: "技能组名"     # 用于按组激活/屏蔽
---
# 技能指令内容
```

## 配置

编辑 `config.jsonc` 配置 LLM、数据库、Skills 目录等。支持 JSONC 注释和 `{env:VAR}` 环境变量。

## 思考过程显示

框架使用 `ChatOpenAIReasoning` 类自动提取模型的推理内容（`reasoning_content`），支持在前端显示"思考中"面板。

| 模型 | 思考过程 | 说明 |
|------|:---:|------|
| `ds-deepseek-v4-flash` | 始终显示 | DeepSeek 官方 API |
| `ark-deepseek-v4-flash` | 始终显示 | 字节方舟 Coding Plan |
| `ark-glm-5.1` | 复杂任务时显示 | 简单问题不触发思考 |

## 与框架的关系

```
lc-agent（框架，pip install）
    ↓ import
lc-agent-bfzs（本项目，用户业务代码）
```

- 不修改框架代码
- 通过 import + 装饰器 + 配置文件扩展
- 框架提供 Web UI / API / 引擎 / 持久化 / reasoning 提取
- 本项目只写业务逻辑（tools / agents / skills）
