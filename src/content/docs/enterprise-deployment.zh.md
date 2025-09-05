---
title: 部署与安全
group: 企业
order: 20
status: partial
---

# 部署与安全

无状态核心：将crate嵌入到你的异步服务中并水平扩展。使用环境隔离来管理提供商密钥。

## 安全实践

- **密钥管理**：进程启动时加载密钥；永不记录
- **计划中**：密钥轮换钩子
- **计划中**：每个请求的审计元数据

## 自托管

运行时嵌入或服务包装。最小依赖保持占用空间小。

## 企业级部署架构

### 容器化部署

```dockerfile
# Dockerfile示例
FROM rust:1.70-slim as builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates
COPY --from=builder /app/target/release/ai-service /usr/local/bin/
EXPOSE 8080
CMD ["ai-service"]
```

### Kubernetes部署

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-service
  template:
    metadata:
      labels:
        app: ai-service
    spec:
      containers:
      - name: ai-service
        image: ai-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-secrets
              key: openai-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Helm Chart配置

```yaml
# values.yaml
replicaCount: 3

image:
  repository: ai-service
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8080

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

secrets:
  openai_key: ""
  anthropic_key: ""
  groq_key: ""

config:
  max_retries: 3
  timeout: 30s
  pool_size: 16
```

## 安全配置

### 密钥管理

```rust
use ai_lib::{AiClient, Provider, ConnectionOptions};
use std::env;

// 从环境变量或密钥管理系统加载
let openai_key = env::var("OPENAI_API_KEY")
    .or_else(|_| load_from_vault("openai-key"))?;

let client = AiClient::with_options(
    Provider::OpenAI,
    ConnectionOptions {
        api_key: Some(openai_key),
        ..Default::default()
    }
)?;
```

### 网络安全

```rust
// 代理配置
let client = AiClient::with_options(
    Provider::OpenAI,
    ConnectionOptions {
        proxy: Some("http://corporate-proxy:8080".into()),
        disable_proxy: false,
        ..Default::default()
    }
)?;
```

### 审计日志

```rust
use ai_lib::metrics::{Metrics, Timer};

struct AuditMetrics {
    logger: Logger,
}

impl Metrics for AuditMetrics {
    async fn incr_counter(&self, name: &str, value: u64) {
        self.logger.info("metric", |log| {
            log.field("name", name)
               .field("value", value)
        });
    }
    
    async fn start_timer(&self, name: &str) -> Option<Box<dyn Timer + Send>> {
        Some(Box::new(AuditTimer::new(name, &self.logger)))
    }
}
```

## 高可用性配置

### 负载均衡

```rust
use ai_lib::{ModelArray, LoadBalancingStrategy, ModelEndpoint};

let mut array = ModelArray::new("production")
    .with_strategy(LoadBalancingStrategy::HealthBased);

// 多个区域端点
array.add_endpoint(ModelEndpoint {
    name: "us-east-1".into(),
    url: "https://api-east.openai.com".into(),
    weight: 1.0,
    healthy: true,
});

array.add_endpoint(ModelEndpoint {
    name: "us-west-1".into(),
    url: "https://api-west.openai.com".into(),
    weight: 0.8,
    healthy: true,
});
```

### 健康检查

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};

async fn health_check(client: &AiClient) -> bool {
    let req = ChatCompletionRequest::new(
        client.default_chat_model(),
        vec![Message::user(Content::new_text("ping"))]
    );
    
    match client.chat_completion(req).await {
        Ok(_) => true,
        Err(_) => false,
    }
}
```

## 监控和可观测性

### Prometheus指标

```rust
use ai_lib::metrics::{Metrics, Timer};
use prometheus::{Counter, Histogram, Registry};

struct PrometheusMetrics {
    request_counter: Counter,
    request_duration: Histogram,
}

impl Metrics for PrometheusMetrics {
    async fn incr_counter(&self, name: &str, value: u64) {
        self.request_counter.inc_by(value as f64);
    }
    
    async fn start_timer(&self, name: &str) -> Option<Box<dyn Timer + Send>> {
        Some(Box::new(PrometheusTimer::new(
            self.request_duration.clone()
        )))
    }
}
```

### 日志配置

```rust
use tracing::{info, error, warn};

// 结构化日志
info!(
    provider = ?client.current_provider(),
    model = %req.model,
    "Processing chat completion request"
);

// 错误日志
match client.chat_completion(req).await {
    Ok(response) => {
        info!(
            tokens = response.usage.total_tokens,
            "Request completed successfully"
        );
    }
    Err(e) => {
        error!(
            error = %e,
            "Request failed"
        );
    }
}
```

## 性能优化

### 连接池配置

```rust
let client = AiClient::with_options(
    Provider::OpenAI,
    ConnectionOptions {
        pool_size: Some(32),
        idle_timeout: Some(Duration::from_secs(60)),
        ..Default::default()
    }
)?;
```

### 缓存策略

```rust
use std::collections::HashMap;
use tokio::sync::RwLock;

struct ResponseCache {
    cache: RwLock<HashMap<String, String>>,
    ttl: Duration,
}

impl ResponseCache {
    async fn get(&self, key: &str) -> Option<String> {
        self.cache.read().await.get(key).cloned()
    }
    
    async fn set(&self, key: String, value: String) {
        self.cache.write().await.insert(key, value);
    }
}
```

## 灾难恢复

### 备份策略

```rust
// 配置备份
let backup_config = BackupConfig {
    enabled: true,
    interval: Duration::from_hours(24),
    retention_days: 30,
    storage: S3Storage::new("ai-service-backups"),
};
```

### 故障转移

```rust
// 多提供商故障转移
let fallback_chain = vec![
    Provider::OpenAI,
    Provider::Anthropic,
    Provider::Groq,
];

for provider in fallback_chain {
    match AiClient::new(provider) {
        Ok(client) => {
            if let Ok(response) = client.chat_completion(req.clone()).await {
                return Ok(response);
            }
        }
        Err(_) => continue,
    }
}
```

## 合规性

### 数据保护

```rust
// 敏感数据脱敏
fn sanitize_log(log: &str) -> String {
    log.replace("sk-", "sk-***")
       .replace("Bearer ", "Bearer ***")
}
```

### 审计跟踪

```rust
struct AuditLogger {
    logger: Logger,
}

impl AuditLogger {
    fn log_request(&self, req: &ChatCompletionRequest, user_id: &str) {
        self.logger.info("ai_request", |log| {
            log.field("user_id", user_id)
               .field("model", &req.model)
               .field("message_count", req.messages.len())
               .field("timestamp", chrono::Utc::now());
        });
    }
}
```

## 下一步

- 了解[企业支持](/docs/enterprise-support)的服务选项
- 查看[可观测性](/docs/observability)的监控配置
- 探索[可靠性功能](/docs/reliability-overview)的生产级设置
