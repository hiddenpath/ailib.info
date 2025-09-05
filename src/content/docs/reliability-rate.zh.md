---
title: 速率限制
group: 可靠性
order: 50
status: partial
---

# 速率限制（部分实现）

每个提供商键的令牌桶（内存中）概念用于平滑突发。

```rust
// let limiter = RateLimit::per_minute(3000).burst(600);
// let client = AiClientBuilder::new(Provider::OpenAI).rate_limit(limiter).build()?;
```

自适应并发已实现。分布式状态计划在未来的版本中发布。

## 速率限制实现

速率限制是控制API调用频率的重要机制，防止超出提供商限制。

### 基本配置

```rust
use ai_lib::reliability::RateLimit;

let limiter = RateLimit::per_minute(3000)
    .burst(600)
    .per_second(50);

let client = AiClientBuilder::new(Provider::OpenAI)
    .rate_limit(limiter)
    .build()?;
```

### 高级配置

```rust
let limiter = RateLimit::new()
    .requests_per_minute(3000)
    .burst_capacity(600)
    .requests_per_second(50)
    .tokens_per_minute(150000)
    .adaptive_concurrency(true)
    .distributed_state(false); // 计划中

let client = AiClientBuilder::new(Provider::OpenAI)
    .rate_limit(limiter)
    .build()?;
```

### 使用示例

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};

async fn rate_limited_chat(
    client: &AiClient,
    request: ChatCompletionRequest,
) -> Result<String, Box<dyn std::error::Error>> {
    // 检查速率限制
    if !client.rate_limiter().can_proceed() {
        return Err("Rate limit exceeded".into());
    }
    
    // 执行请求
    let response = client.chat_completion(request).await?;
    
    // 更新速率限制器
    client.rate_limiter().record_request().await;
    
    Ok(response.first_text()?)
}
```

## 下一步

- 学习[可靠性概述](/docs/reliability-overview)了解其他可靠性功能
- 查看[重试机制](/docs/reliability-retry)了解重试策略
- 探索[熔断器](/docs/reliability-circuit)了解故障保护
