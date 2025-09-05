---
title: 可靠性概述
group: 可靠性
order: 0
---

# 可靠性概述

可组合的原语提高成功概率并减少尾延迟。

章节：

- [重试](/docs/reliability-retry)
- [回退链](/docs/reliability-fallback)
- [竞争/对冲](/docs/reliability-race)
- [智能路由](/docs/reliability-routing)
- [速率限制](/docs/reliability-rate)
- [熔断器](/docs/reliability-circuit)

状态：重试/路由/竞争稳定；回退稳定；速率限制部分；熔断器部分。

## 可靠性原语

ai-lib提供了一套完整的可靠性原语，帮助构建健壮的生产级AI应用：

### 重试机制
- **指数退避**：智能重试间隔，避免雪崩效应
- **抖动**：随机化重试时间，减少竞争
- **错误分类**：区分可重试和永久错误
- **最大重试次数**：防止无限重试

### 回退策略
- **多提供商回退**：主提供商失败时自动切换
- **健康检查**：监控提供商状态
- **智能选择**：基于性能和成本选择最佳提供商

### 竞争/对冲
- **并行请求**：同时向多个提供商发送请求
- **快速响应**：使用最快完成的响应
- **取消机制**：取消较慢的请求以节省资源

### 智能路由
- **负载均衡**：在多个端点间分发请求
- **健康监控**：避免不健康的端点
- **性能优化**：基于延迟和吞吐量选择路由

### 速率限制
- **令牌桶算法**：平滑的请求速率控制
- **自适应调整**：根据提供商限制动态调整
- **队列管理**：优雅处理突发流量

### 熔断器
- **故障检测**：自动识别失败的端点
- **快速失败**：避免向已知失败的端点发送请求
- **自动恢复**：定期尝试恢复失败的端点

## 使用示例

### 基本重试

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};

let client = AiClient::new(Provider::OpenAI)?;
let req = ChatCompletionRequest::new(
    client.default_chat_model(),
    vec![Message::user(Content::new_text("你好"))]
);

// 自动重试，内置指数退避
let resp = client.chat_completion(req).await?;
```

### 错误处理

```rust
match client.chat_completion(req).await {
    Ok(response) => println!("成功: {}", response.first_text()?),
    Err(e) if e.is_retryable() => {
        // 可重试错误，实现自定义重试逻辑
        println!("可重试错误: {}", e);
    }
    Err(e) => {
        // 永久错误，记录并处理
        println!("永久错误: {}", e);
    }
}
```

### 多提供商回退

```rust
use ai_lib::{AiClient, Provider, ModelArray, LoadBalancingStrategy};

let mut array = ModelArray::new("production")
    .with_strategy(LoadBalancingStrategy::HealthBased);

// 添加多个提供商
array.add_endpoint(ModelEndpoint {
    name: "groq-1".into(),
    url: "https://api.groq.com".into(),
    weight: 1.0,
    healthy: true,
});

array.add_endpoint(ModelEndpoint {
    name: "openai-1".into(),
    url: "https://api.openai.com".into(),
    weight: 0.8,
    healthy: true,
});

let client = AiClient::with_model_array(array)?;
```

## 配置选项

### 重试配置

```rust
use ai_lib::{AiClient, Provider, ConnectionOptions};
use std::time::Duration;

let client = AiClient::with_options(
    Provider::OpenAI,
    ConnectionOptions {
        max_retries: Some(3),
        retry_delay: Some(Duration::from_millis(1000)),
        ..Default::default()
    }
)?;
```

### 超时配置

```rust
let client = AiClient::with_options(
    Provider::OpenAI,
    ConnectionOptions {
        timeout: Some(Duration::from_secs(30)),
        ..Default::default()
    }
)?;
```

### 代理配置

```rust
let client = AiClient::with_options(
    Provider::OpenAI,
    ConnectionOptions {
        proxy: Some("http://proxy:8080".into()),
        ..Default::default()
    }
)?;
```

## 监控和指标

ai-lib支持自定义指标集成：

```rust
use ai_lib::metrics::{Metrics, Timer};

struct CustomMetrics;

impl Metrics for CustomMetrics {
    async fn incr_counter(&self, name: &str, value: u64) {
        // 实现自定义指标收集
        println!("指标 {}: {}", name, value);
    }
    
    async fn start_timer(&self, name: &str) -> Option<Box<dyn Timer + Send>> {
        // 实现自定义计时器
        Some(Box::new(CustomTimer::new(name)))
    }
}

let client = AiClient::new_with_metrics(Provider::OpenAI, Arc::new(CustomMetrics))?;
```

## 最佳实践

1. **合理设置重试次数**：避免过度重试
2. **监控错误率**：及时发现和解决问题
3. **使用健康检查**：避免向不健康的端点发送请求
4. **实现熔断器**：防止级联故障
5. **监控延迟**：优化用户体验
6. **使用批处理**：提高吞吐量
7. **实现优雅降级**：在部分功能不可用时仍能提供服务

## 下一步

- 学习[重试机制](/docs/reliability-retry)的详细配置
- 了解[回退策略](/docs/reliability-fallback)的实现
- 探索[智能路由](/docs/reliability-routing)的高级功能
- 查看[高级示例](/docs/advanced-examples)中的实际应用
