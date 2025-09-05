---
title: 智能路由
group: 可靠性
order: 40
status: stable
---

# 智能路由（稳定）

基于能力元数据（速度层、质量层、成本）和策略目标选择提供商/模型。

```rust
// let routing = RoutingPolicy::balanced()
//    .allow(["gpt-4o","claude-3-haiku","mistral-medium"]);
// let client = AiClientBuilder::new(Provider::OpenAI).routing(routing).build()?;
```

计划中：反馈循环摄取延迟/质量指标以自适应选择。

## 智能路由实现

智能路由根据请求特性和提供商能力自动选择最佳提供商。

### 基本配置

```rust
use ai_lib::reliability::RoutingPolicy;

let routing = RoutingPolicy::balanced()
    .allow(["gpt-4o", "claude-3-haiku", "mistral-medium"])
    .prefer_fast_for_simple_requests(true)
    .prefer_quality_for_complex_requests(true)
    .cost_aware(true);

let client = AiClientBuilder::new(Provider::OpenAI)
    .routing(routing)
    .build()?;
```

### 高级配置

```rust
let routing = RoutingPolicy::new()
    .add_provider("gpt-4o", ProviderCapability {
        speed_tier: SpeedTier::Fast,
        quality_tier: QualityTier::High,
        cost_per_token: 0.03,
        max_tokens: 128000,
    })
    .add_provider("claude-3-haiku", ProviderCapability {
        speed_tier: SpeedTier::VeryFast,
        quality_tier: QualityTier::Medium,
        cost_per_token: 0.01,
        max_tokens: 200000,
    })
    .routing_strategy(RoutingStrategy::Adaptive)
    .feedback_enabled(true); // 计划中

let client = AiClientBuilder::new(Provider::OpenAI)
    .routing(routing)
    .build()?;
```

### 使用示例

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};

async fn intelligent_chat(
    client: &AiClient,
    request: ChatCompletionRequest,
) -> Result<String, Box<dyn std::error::Error>> {
    // 智能路由会自动选择最佳提供商
    let response = client.chat_completion(request).await?;
    
    // 记录路由决策用于反馈
    client.record_routing_decision(
        response.provider_used(),
        response.latency(),
        response.quality_score(),
    ).await;
    
    Ok(response.first_text()?)
}
```

## 下一步

- 学习[可靠性概述](/docs/reliability-overview)了解其他可靠性功能
- 查看[竞争策略](/docs/reliability-race)了解延迟优化
- 探索[回退链](/docs/reliability-fallback)了解故障转移
