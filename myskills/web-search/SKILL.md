---
name: web-search
description: >-
  联网搜索、实时信息检索、事实核验。当用户需要最新互联网信息、查公开资料、
  找技术文章（CSDN/掘金/官方文档）、搜索英文技术文档、GitHub 仓库 README 时使用。
metadata:
  group: 信息检索
  pattern: tool-wrapper
---

# Web Search Skill

## 引擎选择

**调用 `search` 工具时必须显式传 `engines` 数组参数**（不依赖默认值 `["bing"]`，bing 不可用）。

| 搜索类型 | 推荐引擎 | 说明 |
|---------|---------|------|
| 中文技术 | `sogou`, `csdn`, `juejin` | 国内技术社区优先 |
| 英文技术 | `duckduckgo`, `brave` | 英文搜索质量高 |
| 通用/混合 | `duckduckgo`, `sogou`, `brave` | 兼顾中英文 |

## 引擎可用性速查

以下引擎不可用，**不要使用**：

| 引擎 | 原因 |
|------|------|
| `bing` | 返回 301（默认引擎，必须显式替换） |
| `startpage` | 返回 307 |
| `exa` | API 未配置，返回 0 条 |

`searchMode` 默认 `auto`，DuckDuckGo 结果不足时可切 `playwright`。

## 搜索工作流

搜索结果包含 `title`、`description`（摘要）、`url`。**limit 设大（30–50）来获取足够候选**，然后扫 description 判断相关性，只对需要的 URL 抓取全文。

```
- [ ] 1. 确定搜索需求：语言、领域、关键词
- [ ] 2. 选择引擎并执行搜索：engines=["sogou","csdn"], limit=40
      结果不足 → 换组合重试（baidu 兜底）
- [ ] 3. 扫 description 筛选：摘要够回答？→ 直接回答 + 标注来源
      需要详情 → 挑出相关 URL 进入步骤 4
- [ ] 4. 抓取原文：通用网页 → fetchWebContent；专项站点 → 专用抓取工具
- [ ] 5. 交叉验证 + 回答：多来源比对，标注 URL
```

## 内容抓取工具

| 场景 | 首选工具 | 备选 |
|------|---------|------|
| 通用网页 | `fetchWebContent` | — |
| CSDN 文章 | `fetchCsdnArticle` | `fetchWebContent` |
| 掘金文章 | `fetchJuejinArticle` | `fetchWebContent` |
| GitHub README | `fetchGithubReadme` | — |
| Linux Do | ❌ 不可用（ECONNREFUSED） | — |

`fetchWebContent` 参数：`url`（必填）、`maxChars`（1000–200000，默认 30000）、`readability`、`includeLinks`。

## 调用示例

```json
{"query": "FastAPI WebSocket 优势", "engines": ["sogou", "csdn", "juejin"], "limit": 40}
```
```json
{"query": "Python asyncio gather vs TaskGroup", "engines": ["duckduckgo"], "limit": 40}
```
```json
{"query": "LangGraph agent architecture", "engines": ["duckduckgo", "sogou"], "limit": 40}
```

搜索后根据 description 筛选相关 URL，再调 `fetchWebContent` 或对应抓取工具获取全文。

## 常见问题

| 问题 | 处理方式 |
|------|---------|
| 某引擎返回空/报错 | 自动排除，换备选引擎 |
| Limit 默认仅 10 条 | 设到 30–50 才有足够候选 |
| 偶发 JSON 序列化异常 | 保持参数重试一次 |
| CSDN 521 错误 | 切 `fetchWebContent` 直接抓原 URL |
| 所有引擎均失败 | 告知用户搜索服务暂不可用 |
