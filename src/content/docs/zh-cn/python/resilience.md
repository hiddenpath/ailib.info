---
title: 韧性模式（Python）
description: ai-lib-python v1.0.0 生产可靠性模式 — 熔断、限流、背压、重试。
---

# 韧性模式

ai-lib-python（v1.0.0）将**内置客户端背压**与**按需策略原语**分开：

- **`AiClient`：** 可选的 `max_inflight` 背压，通过 `AiClientBuilder` 或 `AI_LIB_MAX_INFLIGHT`。
- **`ai_lib_python.resilience`：** 重试策略、令牌桶限流、熔断器 — **不会**由 `AiClient.create()` 自动接线；请使用 `production_ready()` 或显式 `ResilientConfig`（见 `examples/resilience.py`）。

重试与回退决策使用 V2 标准错误码：归一化错误上的 `retryable` 与 `fallbackable` 元数据。

## 快速启用

```python
client = await (
    AiClient.builder()
    .model("deepseek/deepseek-chat")
    .production_ready()  # ResilientConfig.production()
    .build()
)
```

## 熔断器

通过停止向故障提供商发请求，防止级联失败。

**状态：** Closed → Open（达到失败阈值后）→ Half-Open（冷却后探测请求）。

通过 `ResilientConfig` / builder 方法配置 — 不依赖未文档化的环境变量。

## 限流器

令牌桶限流位于 `ai_lib_python.resilience`。在 builder 上配置：

```python
from ai_lib_python.resilience import RateLimitConfig

client = await (
    AiClient.builder()
    .model("openai/gpt-4o")
    .with_rate_limit(RateLimitConfig(requests_per_second=10))
    .build()
)
```

运行时**不会**读取 `AI_LIB_RPS` / `AI_LIB_RPM` 环境变量。

## 背压

限制并发在途请求：

```bash
export AI_LIB_MAX_INFLIGHT=50
```

或在 builder 上：`.max_inflight(50)`。

## 重试

由清单 `retry_policy` 与 `ResilientConfig` 驱动指数退避重试。仅被归类为可重试的错误会触发重试。

## 组合模式

启用 `production_ready()` 时的典型请求流程：

1. **背压** — 若已达最大在途数，等待槽位
2. **熔断器** — 若熔断打开，立即拒绝
3. **限流器** — 若受速率限制，等待令牌
4. **执行** — 经 pipeline 发送 HTTP 请求
5. **重试** — 可重试错误时退避并重试
6. **更新** — 记录成功/失败以供熔断器使用

## 下一步

- **[高级功能](/zh-cn/python/advanced/)** — 遥测、路由、插件
- **[AiClient API](/zh-cn/python/client/)** — 客户端用法
