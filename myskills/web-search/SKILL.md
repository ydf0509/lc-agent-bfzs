---
name: web-search
description: 使用 web-search MCP 进行互联网搜索，支持多引擎组合查询
metadata:
  group: "信息检索"
---

# Web Search MCP 使用指南

## 工具

使用 `searchWeb` 工具发起搜索。

## 参数

- `query`: 搜索关键词
- `engines`: 搜索引擎列表，可选值：
  - `duckduckgo`
  - `sogou`
  - `brave`
  - `exa`
  - `csdn`
  - `juejin`

每次搜索可组合使用多个引擎，例如 `["duckduckgo", "brave", "exa"]`

## 注意事项

**禁止使用以下引擎**（免费用户不可用，搜不到内容）：
- `baidu`
- `bing`
- `startpage`

## 使用示例

搜索技术文档：
```json
{
  "query": "LangChain 2026 最新用法",
  "engines": ["duckduckgo", "brave", "csdn"]
}
```

搜索中文社区内容：
```json
{
  "query": "FastAPI WebSocket 最佳实践",
  "engines": ["sogou", "csdn", "juejin"]
}
```

搜索英文资源：
```json
{
  "query": "LangGraph state management",
  "engines": ["duckduckgo", "brave", "exa"]
}
```
