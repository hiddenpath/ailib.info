---
title: Go 韧性模式
description: ai-lib-go v1.0.0 生产可靠性模式。
---

# 韧性模式

ai-lib-go（v1.0.0）在执行层提供清单驱动的微重试；熔断与多提供商回退位于 **`pkg/contact`** 策略层。V2 标准错误码的 `retryable` / `fallbackable` 属性决定重试与回退行为。

## 执行层重试

`pkg/ailib` 的 `internal/resilience` 对可重试错误做短延迟重试，无需额外配置即可用于基础 HTTP 聊天。

## 熔断（pkg/contact）

通过 `FallbackClient` 与 contact 层策略避免向持续失败的提供商发送请求：

- **Closed** — 正常转发
- **Open** — 失败过多，立即拒绝
- **Half-Open** — 冷却期后试探性放行

## 多提供商回退

```go
import "github.com/ailib-official/ai-lib-go/pkg/contact"

fb := contact.NewFallbackClient([]ailib.Client{primary, secondary})
```

按顺序尝试客户端，直至成功或全部失败。

## 能力边界（如实描述）

| 模式 | pkg/ailib | pkg/contact |
|------|-----------|-------------|
| HTTP 微重试 | 是 | — |
| 熔断 | 否 | 是 |
| 多提供商回退 | 否 | 是 |
| 全局限流/背压 | 否 | 需自行集成 |

## 下一步

- **[高级特性](/zh-cn/go/advanced/)**
- **[Client API](/zh-cn/go/client/)**
