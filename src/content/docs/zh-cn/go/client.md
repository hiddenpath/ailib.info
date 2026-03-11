---
title: AiClient (Go)
description: Go AiClient 接口参考。
---

# AiClient

`AiClient` 是使用 `ai-lib-go` 的主要入口点。它管理底层的 `net/http` 客户端、清单解析、错误映射和流式管道。

## 实例化

```go
aiClient, err := client.NewAiClient(ctx, providerName, options)
```

- `providerName`: 供应商清单的确切名称（例如 `openai`, `anthropic`, `gemini`）。
- `options`: 可选参数，如自定义清单路径、HTTP 客户端覆盖或显式的 API 密钥（尽管更推荐使用环境变量）。

## 上下文集成

与其他运行时不同，Go SDK 深度利用 `context.Context` 进行弹性设计在生命周期管理：

```go
ctx, cancel := context.WithTimeout(context.Background(), 10 * time.Second)
defer cancel()

// 如果 HTTP 请求或流式传输时间超过 10 秒，它将自动取消。
stream := aiClient.Chat().Model("gpt-4o").User("列出 5 种颜色").Stream(ctx)
```

## 支持的端点

目前可以使用 `Chat()` 和 `Embeddings()` 构建器。多模态、MCP 和 Computer Use 支持正在为 `v0.1.0` 版本开发中。
