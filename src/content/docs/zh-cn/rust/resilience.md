---
title: 弹性（Rust）
description: ai-lib-rust v0.7.1 中的生产级可靠性模式 — 熔断器、速率限制器、背压、重试。
---

# 弹性模式

ai-lib-rust（v0.7.1）开箱即用提供生产级可靠性模式。重试与回退决策使用 V2 标准错误码：`StandardErrorCode` 上的 `retryable` 与 `fallbackable` 属性决定错误是否触发重试或模型回退。

## 熔断器

通过停止向故障提供商发送请求来防止级联故障：

**状态：**
- **Closed（闭合）** — 正常操作，请求通过
- **Open（打开）** — 故障过多，请求立即被拒绝
- **Half-Open（半开）** — 冷却后允许一次测试请求

**配置：**

```bash
export AI_LIB_BREAKER_FAILURE_THRESHOLD=5
export AI_LIB_BREAKER_COOLDOWN_SECS=30
```

连续 `FAILURE_THRESHOLD` 次故障后熔断器打开，保持打开 `COOLDOWN_SECS` 秒后再进行测试。

## 速率限制器

令牌桶算法防止超出提供商速率限制：

```bash
export AI_LIB_RPS=10    # Max requests per second
export AI_LIB_RPM=600   # Max requests per minute
```

超出限制的请求会被排队而非拒绝，以提供平稳的吞吐量。

## 背压

使用信号量限制并发在途请求：

```bash
export AI_LIB_MAX_INFLIGHT=50
```

达到限制时，新请求会等待直到有空闲槽位。

## 重试

由协议清单的重试策略驱动的指数退避重试：

```yaml
# In the provider manifest
retry_policy:
  strategy: "exponential_backoff"
  max_retries: 3
  initial_delay_ms: 1000
  max_delay_ms: 30000
  retryable_errors:
    - "rate_limited"
    - "overloaded"
    - "server_error"
```

只有被归类为可重试的错误才会触发重试。例如，身份验证错误会立即失败。

## 模式组合

所有弹性模式协同工作。典型的请求流程：

1. **背压** — 若已达最大在途数则等待槽位
2. **熔断器** — 若熔断器打开则立即拒绝
3. **速率限制器** — 若被限速则等待令牌
4. **执行** — 发送请求
5. **重试** — 若是可重试错误，等待后重试
6. **更新** — 记录成功/失败以更新熔断器

## 可观测性

在运行时监控弹性状态：

```rust
// Check circuit breaker state
let state = client.circuit_state();
println!("Circuit: {:?}", state); // Closed, Open, HalfOpen

// Check current inflight count
let inflight = client.current_inflight();
```

## 下一步

- **[高级功能](/rust/advanced/)** — Embeddings、缓存、插件
- **[AiClient API](/rust/client/)** — 客户端使用
