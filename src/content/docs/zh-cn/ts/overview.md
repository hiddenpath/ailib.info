---
title: TypeScript SDK 概述
description: ai-lib-ts v1.0.0 架构与公开 API — AI-Protocol 的 TypeScript 运行时。
---

# TypeScript SDK 概述

**ai-lib-ts**（v1.0.0）是 [AI-Protocol](https://github.com/ailib-official/ai-protocol) 的 TypeScript / Node.js 运行时，npm 包名 `@ailib-official/ai-lib-ts`，提供三个入口：

| 导入路径 | 层级 | 适用场景 |
|--------|------|----------|
| `@ailib-official/ai-lib-ts` | E + P 门面 | 完整 SDK（默认） |
| `@ailib-official/ai-lib-ts/core` | 仅执行层 | 最小体积，无策略层 transport 包装 |
| `@ailib-official/ai-lib-ts/contact` | 仅策略层 | 韧性、路由，无 `AiClient` |

## 主要执行路径

聊天场景下，**`AiClient` 不会调用底层 `Pipeline` 算子 API**。流程为：

1. 加载提供商清单
2. 根据清单字段构建 HTTP 请求
3. 通过 **`HttpTransport`** 发送
4. 使用清单 `response_paths` 与 OpenAI 风格回退解析 JSON / SSE

`Pipeline` 仍作为合规测试与高级集成 API 公开。本运行时**没有** `ProviderDriver`。

## 能力边界（如实描述）

| 领域 | 运行时提供 | 不包含 |
|------|------------|--------|
| **MCP** | `McpToolBridge` 格式转换 | 接入 `AiClient` 的 MCP 传输 |
| **Computer Use** | V2 配置类型 | 动作执行环境 |
| **热更新** | — | 未实现 |
| **韧性** | 默认 transport 上的清单重试 | 熔断/限流/背压需显式配置 |
| **Embeddings** | `EmbeddingClient` | 非清单 Pipeline 路径 |

## 下一步

- [快速开始](/zh-cn/ts/quickstart/)
- [流式处理](/zh-cn/ts/streaming/)
- [韧性模式](/zh-cn/ts/resilience/)
