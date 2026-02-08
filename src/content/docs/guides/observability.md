---
title: Observability
description: Monitoring, metrics, logging, and tracing with AI-Lib runtimes.
---

# Observability

Both runtimes provide observability features for production deployments.

## Rust: Structured Logging

ai-lib-rust uses the `tracing` ecosystem:

```rust
use tracing_subscriber;

// Enable logging
tracing_subscriber::init();

// All AI-Lib operations emit structured log events
let client = AiClient::from_model("openai/gpt-4o").await?;
```

Log levels:
- `INFO` — Request/response summaries
- `DEBUG` — Protocol loading, pipeline stages
- `TRACE` — Individual frames, JSONPath matches

## Rust: Call Statistics

Every request returns usage statistics:

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

## Python: Metrics (Prometheus)

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

Tracked metrics:
- `ai_lib_requests_total` — Request count by model/provider
- `ai_lib_request_duration_seconds` — Latency histogram
- `ai_lib_tokens_total` — Token usage by type
- `ai_lib_errors_total` — Error count by type

## Python: Distributed Tracing (OpenTelemetry)

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

Traces include spans for:
- Protocol loading
- Request compilation
- HTTP transport
- Pipeline processing
- Event mapping

## Python: Health Monitoring

```python
from ai_lib_python.telemetry import HealthChecker

health = HealthChecker()
status = await health.check()

print(f"Healthy: {status.is_healthy}")
print(f"Details: {status.details}")
```

## Python: User Feedback

Collect feedback on AI responses:

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

## Resilience Observability

Monitor circuit breaker and rate limiter state:

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
