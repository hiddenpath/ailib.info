---
title: 部署与安全
group: 企业
order: 20
status: partial
---

# 部署与安全

ai-lib 提供无状态核心，可嵌入到异步服务中并水平扩展。对于具有高级安全和合规要求的企业部署，请参阅 [ai-lib-pro](/zh/docs/enterprise-pro) 了解增强功能。

## 安全实践

### 基础安全 (ai-lib)
- API密钥在进程启动时加载；从不记录
- 提供商密钥的环境变量隔离
- 企业网络的代理支持
- 默认不记录内容

### 企业安全 (ai-lib-pro)
- **密钥管理**：与HashiCorp Vault、AWS Secrets Manager集成
- **密钥轮换**：零停机时间的自动密钥轮换
- **审计日志**：所有请求的全面审计跟踪
- **RBAC**：基于角色的访问控制，具有细粒度权限
- **合规性**：GDPR、SOC2、HIPAA合规框架
- **加密**：敏感数据的端到端加密

## 部署选项

### 基础部署
运行时嵌入或服务包装。最小依赖保持占用空间小。

### 企业部署 (ai-lib-pro)
具有安全性和合规性的企业级部署配置。

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

## 企业架构

### 高可用性设置
- **负载均衡**：负载均衡器后的多个实例
- **健康检查**：自动健康监控和故障转移
- **熔断器**：自动故障检测和恢复
- **监控**：全面的指标和告警

### 安全架构
- **网络隔离**：VPC和防火墙配置
- **访问控制**：多层身份验证和授权
- **数据保护**：静态和传输中的加密
- **合规监控**：实时合规检查

## 性能优化

### 连接池
高效的资源管理，支持高并发和连接复用。

### 缓存策略
- 重复查询的响应缓存
- 模型响应缓存
- 提供商健康状态缓存
- 配置缓存

## 监控和可观测性

### 基础监控 (ai-lib)
- 自定义指标集成
- 请求/响应计时
- 错误率跟踪
- 提供商健康监控

### 企业监控 (ai-lib-pro)
- **实时仪表板API**：提供REST端点的实时系统指标、用户分析和成本跟踪
- **结构化事件分析**：丰富的元数据收集，包括用户上下文、性能数据和成本信息
- **高级健康监控**：多维度评分，自动告警生成和组件状态跟踪
- **分布式追踪**：跨服务的完整请求追踪，具有相关ID和性能瓶颈识别
- **自定义KPI**：业务特定指标，具有灵活标记和实时聚合功能

## 下一步

- 探索 [ai-lib-pro](/zh/docs/enterprise-pro) 了解高级企业功能
- 查看[安全与合规](/zh/docs/enterprise-pro#企业安全与合规)了解详细安全功能
- 检查[成本管理](/zh/docs/enterprise-pro#高级定价与成本管理)了解企业成本控制
- 联系[企业支持](/zh/docs/enterprise-support)获取部署协助
