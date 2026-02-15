---
title: 可观测性
description: 使用 AI-Lib 运行时的监控、指标、日志与追踪。
---

# 可观测性

两个运行时均为生产部署提供可观测性功能。

## Rust：结构化日志

ai-lib-rust 使用 `tracing` 生态：

```rust
use tracing_subscriber;

// Enable logging
tracing_subscriber::init();

// All AI-Lib operations emit structured log events
let client = AiClient::from_model("openai/gpt-4o").await?;
```

日志级别：
- `INFO` — 请求/响应摘要
- `DEBUG` — 协议加载、管道阶段
- `TRACE` — 单个帧、JSONPath 匹配

## Rust：调用统计

每次请求都会返回使用统计：

```rust
let (response, stats) = client.chat()
    .user("Hello")
    .execute_with_stats()
    .await?;

println!("Model: {}", stats.model);
println!("Provider: {}", stats.provider);
println!("Prompt tokens: {}", stats.prompt_tokens);
println!("Completion tokens: {}", stats.completion_tokens);
println!("Total tokens: {}", stats.total_tokens);
println!("Latency: {}ms", stats.latency_ms);
```

## Python：指标（Prometheus）

```python
from ai_lib_python.telemetry import MetricsCollector

metrics = MetricsCollector()

client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .metrics(metrics) \
    .build()

# After some requests...
prometheus_text = metrics.export_prometheus()
```

跟踪的指标：
- `ai_lib_requests_total` — 按 model/provider 的请求数
- `ai_lib_request_duration_seconds` — 延迟直方图
- `ai_lib_tokens_total` — 按类型的 token 使用量
- `ai_lib_errors_total` — 按类型的错误数

## Python：分布式追踪（OpenTelemetry）

```python
from ai_lib_python.telemetry import Tracer

tracer = Tracer(
    service_name="my-app",
    endpoint="http://jaeger:4317",
)

client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .tracer(tracer) \
    .build()
```

追踪包含以下 span：
- 协议加载
- 请求编译
- HTTP 传输
- 管道处理
- 事件映射

## Python：健康监控

```python
from ai_lib_python.telemetry import HealthChecker

health = HealthChecker()
status = await health.check()

print(f"Healthy: {status.is_healthy}")
print(f"Details: {status.details}")
```

## Python：用户反馈

收集 AI 响应的反馈：

```python
from ai_lib_python.telemetry import FeedbackCollector

feedback = FeedbackCollector()

# After getting a response
feedback.record(
    request_id=stats.request_id,
    rating=5,
    comment="Helpful response",
)
```

## 弹性可观测性

监控熔断器与速率限制器状态：

```rust
// Rust
let state = client.circuit_state(); // Closed, Open, HalfOpen
let inflight = client.current_inflight();
```

```python
# Python
signals = client.signals_snapshot()
print(f"Circuit: {signals.circuit_state}")
print(f"Inflight: {signals.current_inflight}")
```
