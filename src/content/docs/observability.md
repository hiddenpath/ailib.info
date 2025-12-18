---
title: Observability
group: Guide
order: 80
status: stable
---

# Observability

ai-lib provides comprehensive observability features for monitoring and debugging AI applications in production.

## Metrics System

The `metrics` module exposes traits (`Metrics`, `Timer`) for collecting performance and usage metrics. A noop implementation ships by default; plug in your collector by implementing these traits.

### Core Metrics

- **request_count**: Total number of AI requests
- **latency**: Request duration (histogram p50/p95/p99)
- **token_usage**: Tokens consumed per request
- **error_count**: Errors by class and type
- **provider_success_rate**: Success rate per provider

### Built-in Metrics

```rust
use ai_lib::metrics::{Metrics, Timer};

// Request counting
metrics.incr_counter("ai_requests_total", 1).await;

// Latency histogram
if let Some(timer) = metrics.start_timer("ai_request_duration").await {
    // ... execute request ...
    timer.stop();
}

// Error tracking
metrics.incr_counter("ai_errors_total", 1).await;

// Token usage
metrics.incr_counter("ai_tokens_used", token_count).await;
```

## Error Monitoring

Built-in error monitoring with configurable thresholds and alerting:

```rust
use ai_lib::error_handling::monitoring::{ErrorMonitor, ErrorThresholds};
use ai_lib::error_handling::ErrorContext;

let thresholds = ErrorThresholds {
    error_rate_threshold: 0.1, // 10% error rate
    consecutive_errors: 5,
    time_window: Duration::from_secs(60),
};

let monitor = ErrorMonitor::new(metrics, thresholds);
let context = ErrorContext::default();
monitor.record_error(&error, &context).await;
```

## Client Integration

Create clients with custom metrics:

```rust
use ai_lib::{AiClient, Provider};
use std::sync::Arc;

let metrics = Arc::new(MyCustomMetrics::new());
let client = AiClient::new_with_metrics(Provider::OpenAI, metrics)?;
```

## Custom Metrics Implementation

```rust
use ai_lib::metrics::{Metrics, Timer};
use std::time::Instant;

struct CustomMetrics {
    // Your metrics storage
}

impl Metrics for CustomMetrics {
    async fn incr_counter(&self, name: &str, value: u64) {
        // Implement counter logic
    }
    
    async fn start_timer(&self, name: &str) -> Option<Box<dyn Timer + Send>> {
        Some(Box::new(CustomTimer::new(name)))
    }
    
    async fn record_error(&self, name: &str, error_type: &str) {
        // Record error metrics
    }
    
    async fn record_success(&self, name: &str, success: bool) {
        // Record success/failure metrics
    }
}
```

## Advanced Features

### Tagged Metrics

```rust
// Counters with tags
metrics.incr_counter_with_tags("ai_requests_total", 1, &[
    ("provider", "openai"),
    ("model", "gpt-4")
]).await;

// Histograms with tags
metrics.record_histogram_with_tags("ai_request_duration", 1.5, &[
    ("provider", "openai"),
    ("success", "true")
]).await;
```

### Request Tracking

```rust
use ai_lib::metrics::MetricsExt;

// Record complete request with timing and success
metrics.record_request(
    "ai_request",
    timer,
    success
).await;

// With additional tags
metrics.record_request_with_tags(
    "ai_request",
    timer,
    success,
    &[("provider", "openai"), ("model", "gpt-4")]
).await;
```

## Integration Examples

### Prometheus Integration

```rust
use ai_lib::metrics::{Metrics, Timer};
use prometheus::{Counter, Histogram, Registry};

struct PrometheusMetrics {
    request_counter: Counter,
    request_duration: Histogram,
}

impl Metrics for PrometheusMetrics {
    async fn incr_counter(&self, name: &str, value: u64) {
        if name == "ai_requests_total" {
            self.request_counter.inc_by(value as f64);
        }
    }
    
    async fn start_timer(&self, name: &str) -> Option<Box<dyn Timer + Send>> {
        if name == "ai_request_duration" {
            Some(Box::new(PrometheusTimer::new(self.request_duration.clone())))
        } else {
            None
        }
    }
}
```

### OpenTelemetry Integration

```rust
use opentelemetry::{global, trace::Tracer};

async fn traced_request(client: &AiClient, request: ChatCompletionRequest) -> Result<ChatCompletionResponse, AiLibError> {
    let tracer = global::tracer("ai-lib");
    let span = tracer.start("ai.chat_completion");
    
    let _guard = span.enter();
    span.set_attribute("provider", client.current_provider().to_string());
    span.set_attribute("model", request.model.clone());
    
    let result = client.chat_completion(request).await;
    
    match &result {
        Ok(response) => {
            span.set_attribute("success", true);
            span.set_attribute("tokens_used", response.usage.total_tokens as u64);
        }
        Err(error) => {
            span.set_attribute("success", false);
            span.set_attribute("error", error.to_string());
        }
    }
    
    result
}
```

## Best Practices

1. **Consistent Naming**: Use consistent metric names across your application
2. **Tag Usage**: Use tags for dimensional analysis
3. **Performance**: Implement metrics asynchronously to avoid blocking
4. **Error Handling**: Always handle metric collection errors gracefully
5. **Resource Management**: Use appropriate data structures for metric storage

## Next Steps

- Learn about [Reliability Features](/docs/reliability-overview) for production deployments
- Check [Advanced Examples](/docs/advanced-examples) for practical patterns
- Explore [Extension Guide](/docs/extension) for custom implementations
