# -*- coding: utf-8 -*-
content = r"""---
name: langchain-query
description: Use when asked to write code using LangChain, LangGraph, or DeepAgents, or when asked about their latest API syntax and usage patterns. NOT for general Python questions.
---

# LangChain 家族最新用法查询技能

## 概述

当需要编写或查询 LangChain / LangGraph / DeepAgents 代码时，**禁止依赖 AI 预训练知识中的过时语法**。必须通过以下三阶数据源策略获取最新 API 用法，确保代码使用当前版本的框架语法。

## 三阶数据源策略

按优先级依次查询，前一阶不够用时进入下一阶：

### 第一阶：Context7 MCP 官方文档查询（默认首选）

使用 `mcp_context7_query-docs` 工具查询官方文档和 API 参考。

| 框架 | Context7 Library ID | 用途 |
|------|-------------------|------|
| LangChain | `/websites/langchain` | 文档、教程、概念指南 |
| LangChain API | `/websites/reference_langchain` | API 参考、函数签名、参数 |
| LangGraph | `/websites/langchain_oss_python_langgraph` | 文档、教程 |
| LangGraph API | `/websites/reference_langchain_python_langgraph` | API 参考 |
| DeepAgents | `/websites/langchain_oss_python_deepagents` | 文档、用法 |
| DeepAgents GitHub | `/langchain-ai/deepagents` | 源码级参考 |

**调用示例：**

```markdown
# 先 resolve 获取最新 library ID
mcp_context7_resolve-library-id(libraryName="LangChain", query="create_react_agent latest API")

# 再 query 获取详细文档
mcp_context7_query-docs(libraryId="/websites/langchain", query="How to use create_react_agent with tools in LangChain 2026")
```

### 第二阶：nbrag 知识库检索

当 Context7 文档不够用时，调用 nbrag 工具查询 `langchain_ai_codes_and_docs` 知识库。

该知识库包含 langchain 全家桶的源码和教程（langchain_core, langgraph, deepagents, langchain_openai 等）。

**多轮深入检索策略（禁止浅尝辄止）：**

```markdown
第 1 轮: nbrag_search_and_fetch(query="<核心API名> 用法 参数", collection_name="langchain_ai_codes_and_docs")
  → 获取匹配源码和教程原文

第 2 轮: nbrag_find_definition(symbol="<核心类/函数名>", collection_name="langchain_ai_codes_and_docs")
  → 精确定位类/函数完整定义（仅 .py 文件）

第 3 轮: nbrag_grep(keyword="<精确术语/导入路径>", collection_name="langchain_ai_codes_and_docs")
  → 搜索精确字符串、导入语句、装饰器等

第 4 轮: nbrag_get_raw_file(file_path="<上一步找到的文件路径>", collection_name="langchain_ai_codes_and_docs")
  → 获取完整源码文件，避免碎片化理解
```

**搜索上限**：10 轮不同策略和关键词都没找到 → 告知用户"知识库中可能没有相关内容"，不要无限重试。

### 第三阶：直接阅读 site-packages 源码

当前两阶仍不足以确认用法时，直接从 `D:\ProgramData\miniconda3\envs\py312\Lib\site-packages\` 下读取 langchain 相关包的源码。

使用 `Read` 工具读取关键文件，关注：
- 函数签名和参数类型注解
- 文档字符串（docstring）
- 类的 `__init__` 方法
- 关键方法的实现逻辑

**常用源码路径：**

```text
D:\ProgramData\miniconda3\envs\py312\Lib\site-packages\langchain\
D:\ProgramData\miniconda3\envs\py312\Lib\site-packages\langchain_core\
D:\ProgramData\miniconda3\envs\py312\Lib\site-packages\langgraph\
D:\ProgramData\miniconda3\envs\py312\Lib\site-packages\deepagents\
D:\ProgramData\miniconda3\envs\py312\Lib\site-packages\langchain_openai\
```

## 多轮检索流程

```text
用户提问（如 "用 LangGraph 写一个 agent"）
    │
    ▼
第 1 轮: Context7 MCP 查官方文档
    ├── mcp_context7_resolve-library-id → 获取最新 library ID
    └── mcp_context7_query-docs → 获取文档/API 参考
    │
    ├── 足够? → 直接写代码
    │
    ▼ 不够?
    │
第 2 轮: nbrag 知识库检索（至少 3-4 轮深入）
    ├── nbrag_search_and_fetch → 语义搜索 + 原文
    ├── nbrag_find_definition → 精确定义
    ├── nbrag_grep → 精确匹配
    └── nbrag_get_raw_file → 完整源码
    │
    ├── 足够? → 写代码
    │
    ▼ 不够?
    │
第 3 轮: 直接读 site-packages 源码
    └── Read → 函数签名、docstring、实现
    │
    ▼
    └── 综合所有信息写代码
```

## 常见错误

| 错误 | 后果 | 正确做法 |
|------|------|---------|
| 依赖 AI 预训练知识写 LangChain 代码 | 使用过时 API（如旧版 `LLMChain`、旧版 `AgentExecutor`） | 必须走三阶数据源查询最新语法 |
| 只查一轮 nbrag 就下结论 | 信息碎片化，遗漏关键参数 | 至少 3-4 轮深入：语义搜索 → 定义 → grep → 完整文件 |
| 混用不同版本的 API | 运行时错误 | 确认所有 API 来自同一版本 |
| 不查 Context7 直接跳 nbrag | 错过官方最新文档 | 默认首选 Context7 官方文档 |
"""

with open(r"D:\codes\lc-agent-bfzs\myskills\langchain-query\SKILL.md", "w", encoding="utf-8") as f:
    f.write(content)

print("SKILL.md written successfully")
