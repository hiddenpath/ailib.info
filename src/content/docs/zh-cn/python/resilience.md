---
title: 弹性（Python）
description: ai-lib-python v0.7.0 中的生产级可靠性模式 — ResilientExecutor、熔断器、速率限制器、回退。
---

# 弹性模式

ai-lib-python（v0.7.0+）包含围绕 `ResilientExecutor` 的完整弹性系统。重试与回退决策现已通过 `StandardErrorCode` 的 `retryable` 与 `fallbackable` 属性使用 V2 标准错误码，确保协议一致行为。

## ResilientExecutor

将所有可靠性模式整合为单一执行器：

```python
from ai_lib_python.resilience import (
    ResilientConfig, RetryConfig, RateLimiterConfig,
    CircuitBreakerConfig, BackpressureConfig
)

config = ResilientConfig(
    retry=RetryConfig(
        max_retries=3,
        initial_delay=1.0,
        max_delay=30.0,
        backoff_multiplier=2.0,
    ),
    rate_limiter=RateLimiterConfig(
        requests_per_second=10,
    ),
    circuit_breaker=CircuitBreakerConfig(
        failure_threshold=5,
        cooldown_seconds=30,
    ),
    backpressure=BackpressureConfig(
        max_inflight=50,
    ),
)

client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .resilience(config) \
    .build()
```

## 独立模式

### 熔断器

```python
from ai_lib_python.resilience import CircuitBreaker

breaker = CircuitBreaker(
    failure_threshold=5,
    cooldown_seconds=30,
)

# Check state
print(breaker.state)  # "closed", "open", "half_open"
```

### 速率限制器

令牌桶算法：

```python
from ai_lib_python.resilience import RateLimiter

limiter = RateLimiter(
    requests_per_second=10,
    burst_size=20,
)
```

### 背压

并发限制：

```python
from ai_lib_python.resilience import Backpressure

bp = Backpressure(max_inflight=50)
```

### 回退链

多目标故障转移：

```python
from ai_lib_python.resilience import FallbackChain

chain = FallbackChain([
    "openai/gpt-4o",
    "anthropic/claude-3-5-sonnet",
    "deepseek/deepseek-chat",
])
```

## PreflightChecker

请求执行前的统一门控：

```python
from ai_lib_python.resilience import PreflightChecker

checker = PreflightChecker()
# Checks circuit state, rate limits, inflight count
# before allowing a request through
```

## SignalsSnapshot

聚合的运行时状态：

```python
signals = client.signals_snapshot()
print(f"Circuit: {signals.circuit_state}")
print(f"Inflight: {signals.current_inflight}")
print(f"Rate remaining: {signals.rate_remaining}")
```

## 环境变量

| Variable | Purpose |
|----------|---------|
| `AI_LIB_RPS` | 速率限制（每秒请求数） |
| `AI_LIB_BREAKER_FAILURE_THRESHOLD` | 熔断器阈值 |
| `AI_LIB_BREAKER_COOLDOWN_SECS` | 冷却时间 |
| `AI_LIB_MAX_INFLIGHT` | 最大并发请求数 |

## 下一步

- **[高级功能](/python/advanced/)** — Telemetry、路由、插件
- **[AiClient API](/python/client/)** — 客户端使用
