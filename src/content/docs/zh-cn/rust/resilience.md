---
title: 韧性模式（Rust）
description: ai-lib-rust v1.0.1 生产可靠性模式 — 熔断、限流、背压、重试。
---

# 韧性模式

ai-lib-rust（v1.0.1）将**内置客户端背压**与**按需策略原语**分开：

- **`AiClient`：** `max_inflight` 信号量（`AI_LIB_MAX_INFLIGHT` / `AiClientBuilder::max_inflight`）— 默认客户端路径已启用。
- **`ai_lib_rust::resilience`：** 重试策略、令牌桶限流、熔断器 — **不会**由 `AiClient::new` 自动接线；需在客户端旁配置并应用（见 `examples/resilience_patterns.rs`）。

`AiClient` 内部的重试与回退决策使用 V2 标准错误码：`StandardErrorCode` 上的 `retryable` 与 `fallbackable`。

## 熔断器

通过停止向故障提供商发请求，防止级联失败：

**状态：**

- **Closed** — 正常运行，请求通行
- **Open** — 失败过多，请求立即拒绝
- **Half-Open** — 冷却后允许一次探测请求

**配置：**

```bash
export AI_LIB_BREAKER_FAILURE_THRESHOLD=5
export AI_LIB_BREAKER_COOLDOWN_SECS=30
```

连续失败达到 `FAILURE_THRESHOLD` 后熔断打开，并在 `COOLDOWN_SECS` 内保持打开，之后再探测。

## 限流器

令牌桶算法防止超出提供商速率限制：

```bash
export AI_LIB_RPS=10    # Max requests per second
export AI_LIB_RPM=600   # Max requests per minute
```

超出限制的请求会排队而非直接拒绝，从而平滑吞吐。

## 背压

用信号量限制并发在途请求：

```bash
export AI_LIB_MAX_INFLIGHT=50
```

达到上限时，新请求会等待直到有空闲槽位。

## 重试

由协议清单中的重试策略驱动指数退避重试：

```yaml
# In the provider manifest
retry_policy:
  strategy: 'exponential_backoff'
  max_retries: 3
  initial_delay_ms: 1000
  max_delay_ms: 30000
  retryable_errors:
    - 'rate_limited'
    - 'overloaded'
    - 'server_error'
```

仅被归类为可重试的错误会触发重试。例如认证错误会立即失败。

## 组合模式

所有韧性模式可协同工作。典型请求流程：

1. **背压** — 若已达最大在途数，等待槽位
2. **熔断器** — 若熔断打开，立即拒绝
3. **限流器** — 若受速率限制，等待令牌
4. **执行** — 发送请求
5. **重试** — 若为可重试错误，等待后重试
6. **更新** — 记录成功/失败以供熔断器使用

## 可观测性

运行时监控韧性状态：

```rust
// Check circuit breaker state
let state = client.circuit_state();
println!("Circuit: {:?}", state); // Closed, Open, HalfOpen

// Check current inflight count
let inflight = client.current_inflight();
```

## 下一步

- **[高级功能](/zh-cn/rust/advanced/)** — Embeddings、缓存、插件
- **[AiClient API](/zh-cn/rust/client/)** — 客户端用法
