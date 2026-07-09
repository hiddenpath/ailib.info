---
title: Go SDK 概述
description: ai-lib-go v1.0.0 架构与公开 API — AI-Protocol 的 Go 运行时。
---

# Go SDK 概述

**ai-lib-go**（v1.0.0，Go 1.21+）是 [AI-Protocol](https://github.com/ailib-official/ai-protocol) 的 Go 运行时。

| 包 | 层级 | 职责 |
|---------|-------|------|
| `pkg/ailib` | 执行层 (E) | `Client`、清单 HTTP 聊天、能力端点 |
| `pkg/contact` | 策略层 (P) | `FallbackClient`、熔断策略 |

## 主要执行路径

`Client.Chat` → 清单端点解析 → JSON HTTP → 微重试（`internal/resilience`）→ 响应附带 `ExecutionMetadata`。

无清单时，`WithBaseURL` + `WithAPIKey` 使用 OpenAI 兼容默认值。

流式：`ChatStream` → SSE 解码器（默认 `openai_sse`）。

## 能力边界

| 领域 | 实际情况 |
|------|---------|
| MCP / Computer Use | 清单 HTTP 路由 + 能力门控 — 非完整 wire 客户端 |
| 熔断 | 仅 `pkg/contact` |
| 多模态 | 透传 `Message.Content` JSON |

## 下一步

- [快速开始](/zh-cn/go/quickstart/)
- [流式处理](/zh-cn/go/streaming/)
- [韧性模式](/zh-cn/go/resilience/)
