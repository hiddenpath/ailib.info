---
title: TypeScript 韧性模式
description: ai-lib-ts v1.0.0 生产可靠性模式。
---

# 韧性模式

ai-lib-ts（v1.0.0）在默认 P 层 `HttpTransport` 上应用**清单驱动的重试**。熔断、限流与背压**不会**通过 `AiClientBuilder` 自动启用，需在构建 transport 时传入 `resilience` 配置，或在客户端旁使用 `PreflightChecker`。

## 默认 `AiClient` 包含什么

| 模式 | 默认 `AiClient` |
|------|----------------|
| 非流式重试 | 是 |
| 熔断 | 否 |
| 限流 | 否 |
| 背压 | 否 |

## `/core` 与根包

`@ailib-official/ai-lib-ts/core` 使用无重试包装的 E 层 `HttpTransport`。需要策略行为请使用根包或 `/contact`。

## 下一步

- [高级特性](/zh-cn/ts/advanced/)
- [Client API](/zh-cn/ts/client/)
