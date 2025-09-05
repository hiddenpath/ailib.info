---
title: 可观测性
group: 指南
order: 80
status: stable
---

# 可观测性

ai-lib为生产环境中的AI应用程序监控和调试提供全面的可观测性功能。

## 指标系统

`metrics`模块暴露特征（`Metrics`、`Timer`）用于收集性能和使用指标。默认提供无操作实现；通过实现这些特征来插入你的收集器。

### 核心指标

- **request_count**：AI请求总数
- **latency**：请求持续时间（直方图p50/p95/p99）
- **token_usage**：每个请求消耗的令牌数
- **error_count**：按类别和类型分类的错误数
- **provider_success_rate**：每个提供商的成功率

### 内置指标

```rust
use ai_lib::metrics::{Metrics, Timer};

// 请求计数
metrics.incr_counter("ai_requests_total", 1).await;

// 延迟直方图
let timer = metrics.start_timer("ai_request_duration").await;
// ... 执行请求 ...
timer.stop();

// 错误跟踪
metrics.incr_counter("ai_errors_total", 1).await;

// 令牌使用
metrics.incr_counter("ai_tokens_used", token_count).await;
```

## 错误监控

内置错误监控，具有可配置的阈值和告警：

```rust
use ai_lib::error_handling::monitoring::{ErrorMonitor, ErrorThresholds};

let thresholds = ErrorThresholds {
    error_rate_threshold: 0.1, // 10%错误率
    consecutive_errors: 5,
    time_window: Duration::from_secs(60),
};

let monitor = ErrorMonitor::new(metrics, thresholds);
monitor.record_error(&error, &context).await;
```

## 客户端集成

使用自定义指标创建客户端：

```rust
use ai_lib::{AiClient, Provider};
use std::sync::Arc;

let metrics = Arc::new(MyCustomMetrics::new());
let client = AiClient::new_with_metrics(Provider::OpenAI, metrics)?;
```

## 可观测性架构

### 核心组件

ai-lib的可观测性系统基于以下核心组件：

- **指标收集**：性能和使用指标
- **分布式跟踪**：请求链路跟踪
- **结构化日志**：可搜索的日志记录
- **健康检查**：系统状态监控

### 指标系统

#### 内置指标

```rust
use ai_lib::metrics::{Metrics, Timer};

// 请求计数
metrics.incr_counter("ai_requests_total", 1).await;

// 延迟直方图
let timer = metrics.start_timer("ai_request_duration").await;
// ... 执行请求 ...
timer.stop();

// 错误计数
metrics.incr_counter("ai_errors_total", 1).await;

// 令牌使用
metrics.incr_counter("ai_tokens_used", token_count).await;
```

#### 自定义指标

```rust
use ai_lib::metrics::{Metrics, Timer};
use std::sync::Arc;

struct CustomMetrics {
    // 自定义指标存储
}

impl Metrics for CustomMetrics {
    async fn incr_counter(&self, name: &str, value: u64) {
        // 实现自定义计数器逻辑
        match name {
            "ai_requests_total" => {
                // 记录总请求数
                self.record_request_count(value);
            }
            "ai_errors_total" => {
                // 记录错误数
                self.record_error_count(value);
            }
            "ai_tokens_used" => {
                // 记录令牌使用
                self.record_token_usage(value);
            }
            _ => {
                // 处理其他指标
                self.record_custom_metric(name, value);
            }
        }
    }
    
    async fn start_timer(&self, name: &str) -> Option<Box<dyn Timer + Send>> {
        Some(Box::new(CustomTimer::new(name)))
    }
}
```

### 分布式跟踪

#### OpenTelemetry集成

```rust
use opentelemetry::{global, trace::Tracer};
use ai_lib::{AiClient, Provider, ChatCompletionRequest};

async fn traced_chat_completion(
    client: &AiClient,
    request: ChatCompletionRequest,
) -> Result<ChatCompletionResponse, AiLibError> {
    let tracer = global::tracer("ai-lib");
    let span = tracer.start("ai.chat_completion");
    
    let _guard = span.enter();
    
    // 添加属性
    span.set_attribute("provider", client.current_provider().to_string());
    span.set_attribute("model", request.model.clone());
    span.set_attribute("message_count", request.messages.len() as u64);
    
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

#### 自定义跟踪

```rust
use tracing::{info_span, Instrument};

async fn custom_traced_request(
    client: &AiClient,
    request: ChatCompletionRequest,
) -> Result<ChatCompletionResponse, AiLibError> {
    let span = info_span!(
        "ai_request",
        provider = %client.current_provider(),
        model = %request.model,
        request_id = %uuid::Uuid::new_v4()
    );
    
    async move {
        info!("Starting AI request");
        
        let response = client.chat_completion(request).await?;
        
        info!(
            tokens_used = response.usage.total_tokens,
            "AI request completed successfully"
        );
        
        Ok(response)
    }
    .instrument(span)
    .await
}
```

### 结构化日志

#### 日志配置

```rust
use tracing::{info, error, warn};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

fn init_logging() {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "ai_lib=debug".into()),
        )
        .with(
            tracing_subscriber::fmt::layer()
                .with_target(false)
                .with_thread_ids(true)
                .with_thread_names(true)
        )
        .init();
}
```

#### 请求日志

```rust
use tracing::{info, error, warn};
use uuid::Uuid;

async fn logged_chat_completion(
    client: &AiClient,
    request: ChatCompletionRequest,
) -> Result<ChatCompletionResponse, AiLibError> {
    let request_id = Uuid::new_v4();
    
    info!(
        request_id = %request_id,
        provider = %client.current_provider(),
        model = %request.model,
        message_count = request.messages.len(),
        "Starting AI request"
    );
    
    let start_time = std::time::Instant::now();
    
    match client.chat_completion(request).await {
        Ok(response) => {
            let duration = start_time.elapsed();
            
            info!(
                request_id = %request_id,
                duration_ms = duration.as_millis(),
                tokens_used = response.usage.total_tokens,
                success = true,
                "AI request completed successfully"
            );
            
            Ok(response)
        }
        Err(error) => {
            let duration = start_time.elapsed();
            
            error!(
                request_id = %request_id,
                duration_ms = duration.as_millis(),
                error = %error,
                success = false,
                "AI request failed"
            );
            
            Err(error)
        }
    }
}
```

### 健康检查

#### 端点健康监控

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};
use std::sync::Arc;
use tokio::sync::RwLock;

pub struct HealthChecker {
    client: Arc<AiClient>,
    last_check: Arc<RwLock<Option<std::time::Instant>>>,
    is_healthy: Arc<RwLock<bool>>,
}

impl HealthChecker {
    pub fn new(client: Arc<AiClient>) -> Self {
        Self {
            client,
            last_check: Arc::new(RwLock::new(None)),
            is_healthy: Arc::new(RwLock::new(true)),
        }
    }
    
    pub async fn check_health(&self) -> bool {
        let request = ChatCompletionRequest::new(
            self.client.default_chat_model(),
            vec![Message::user(Content::new_text("ping"))]
        );
        
        let start_time = std::time::Instant::now();
        
        match self.client.chat_completion(request).await {
            Ok(_) => {
                let duration = start_time.elapsed();
                let is_healthy = duration.as_millis() < 5000; // 5秒超时
                
                *self.is_healthy.write().await = is_healthy;
                *self.last_check.write().await = Some(start_time);
                
                is_healthy
            }
            Err(_) => {
                *self.is_healthy.write().await = false;
                *self.last_check.write().await = Some(start_time);
                
                false
            }
        }
    }
    
    pub async fn is_healthy(&self) -> bool {
        *self.is_healthy.read().await
    }
}
```

#### 健康检查端点

```rust
use axum::{response::Json, routing::get, Router};
use serde_json::{json, Value};

async fn health_check_handler(health_checker: Arc<HealthChecker>) -> Json<Value> {
    let is_healthy = health_checker.is_healthy().await;
    
    Json(json!({
        "status": if is_healthy { "healthy" } else { "unhealthy" },
        "timestamp": chrono::Utc::now().to_rfc3339(),
        "service": "ai-lib"
    }))
}

fn create_health_router(health_checker: Arc<HealthChecker>) -> Router {
    Router::new()
        .route("/health", get(health_check_handler))
        .with_state(health_checker)
}
```

### 监控集成

#### Prometheus集成

```rust
use ai_lib::metrics::{Metrics, Timer};
use prometheus::{Counter, Histogram, Registry};

pub struct PrometheusMetrics {
    request_counter: Counter,
    request_duration: Histogram,
    error_counter: Counter,
    token_counter: Counter,
}

impl PrometheusMetrics {
    pub fn new(registry: &Registry) -> Self {
        let request_counter = Counter::new(
            "ai_requests_total",
            "Total number of AI requests"
        ).unwrap();
        
        let request_duration = Histogram::new(
            "ai_request_duration_seconds",
            "AI request duration in seconds"
        ).unwrap();
        
        let error_counter = Counter::new(
            "ai_errors_total",
            "Total number of AI errors"
        ).unwrap();
        
        let token_counter = Counter::new(
            "ai_tokens_used_total",
            "Total number of tokens used"
        ).unwrap();
        
        registry.register(Box::new(request_counter.clone())).unwrap();
        registry.register(Box::new(request_duration.clone())).unwrap();
        registry.register(Box::new(error_counter.clone())).unwrap();
        registry.register(Box::new(token_counter.clone())).unwrap();
        
        Self {
            request_counter,
            request_duration,
            error_counter,
            token_counter,
        }
    }
}

impl Metrics for PrometheusMetrics {
    async fn incr_counter(&self, name: &str, value: u64) {
        match name {
            "ai_requests_total" => self.request_counter.inc_by(value as f64),
            "ai_errors_total" => self.error_counter.inc_by(value as f64),
            "ai_tokens_used" => self.token_counter.inc_by(value as f64),
            _ => {} // 忽略未知指标
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

#### Grafana仪表板

```json
{
  "dashboard": {
    "title": "AI-Lib Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(ai_requests_total[5m])",
            "legendFormat": "Requests/sec"
          }
        ]
      },
      {
        "title": "Request Duration",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(ai_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(ai_request_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(ai_errors_total[5m])",
            "legendFormat": "Errors/sec"
          }
        ]
      },
      {
        "title": "Token Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(ai_tokens_used_total[5m])",
            "legendFormat": "Tokens/sec"
          }
        ]
      }
    ]
  }
}
```

### 告警配置

#### 告警规则

```yaml
groups:
  - name: ai-lib
    rules:
      - alert: HighErrorRate
        expr: rate(ai_errors_total[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "AI service error rate is {{ $value }} errors/sec"
      
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(ai_request_duration_seconds_bucket[5m])) > 5
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High latency detected"
          description: "95th percentile latency is {{ $value }}s"
      
      - alert: ServiceDown
        expr: up{job="ai-lib"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "AI service is down"
          description: "AI service has been down for more than 1 minute"
```

### 最佳实践

#### 指标命名

```rust
// 使用一致的命名约定
const METRICS: &[&str] = &[
    "ai_requests_total",
    "ai_request_duration_seconds",
    "ai_errors_total",
    "ai_tokens_used_total",
    "ai_provider_success_rate",
];
```

#### 标签使用

```rust
use ai_lib::metrics::{Metrics, Timer};

impl Metrics for CustomMetrics {
    async fn incr_counter(&self, name: &str, value: u64) {
        // 使用标签进行分类
        match name {
            "ai_requests_total" => {
                self.counter_with_labels("ai_requests_total", &[
                    ("provider", self.provider_name()),
                    ("model", self.model_name()),
                ]).inc_by(value as f64);
            }
            "ai_errors_total" => {
                self.counter_with_labels("ai_errors_total", &[
                    ("provider", self.provider_name()),
                    ("error_type", self.error_type()),
                ]).inc_by(value as f64);
            }
            _ => {}
        }
    }
}
```

#### 性能考虑

```rust
use std::sync::Arc;
use tokio::sync::RwLock;

// 使用异步指标收集避免阻塞
pub struct AsyncMetrics {
    metrics: Arc<RwLock<Vec<MetricEvent>>>,
}

impl AsyncMetrics {
    pub async fn collect_metrics(&self) -> Vec<MetricEvent> {
        let mut metrics = self.metrics.write().await;
        let events = metrics.clone();
        metrics.clear();
        events
    }
}
```

## 下一步

- 查看[高级示例](/docs/advanced-examples)了解实际应用
- 探索[可靠性功能](/docs/reliability-overview)了解生产级配置
- 学习[扩展SDK](/docs/extension)了解自定义实现
