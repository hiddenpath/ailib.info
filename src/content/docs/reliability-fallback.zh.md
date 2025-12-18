---
title: 回退链
group: 可靠性
order: 20
status: stable
---

# 回退链（稳定）

定义模型/提供商的有序列表。在错误或策略匹配时，前进到下一个。伪代码：

```rust
// let chain = FallbackChain::new()
//     .primary("gpt-4o")
//     .on_timeout("claude-3-haiku")
//     .always("mistral-medium");
// let client = AiClientBuilder::new(Provider::OpenAI).fallback(chain).build()?;
```

第一个成功会短路链。与竞争结合以减少尾延迟。

## 策略构建器（OSS）

通过 `RoutingStrategyBuilder` 与厂商 Builder 组合故障转移链：

```rust
use ai_lib::provider::{RoutingStrategyBuilder, GroqBuilder, AnthropicBuilder, OpenAiBuilder};

let strategy = RoutingStrategyBuilder::new()
    .with_provider(GroqBuilder::new().build_provider()?)
    .with_provider(AnthropicBuilder::new().build_provider()?)
    .build_failover()?;

let client = OpenAiBuilder::new()
    .with_strategy(Box::new(strategy))
    .build()?;
```

> 注：带权重/成本与 SLO 感知策略在 `ai-lib-pro` 中提供。

## 回退链实现

回退链是一种重要的可靠性模式，当主提供商失败时自动切换到备用提供商。

### 基本配置

```rust
use ai_lib::reliability::FallbackChain;

let chain = FallbackChain::new()
    .primary("gpt-4o")
    .on_timeout("claude-3-haiku")
    .on_error("mistral-medium")
    .always("gpt-3.5-turbo");

let client = AiClientBuilder::new(Provider::OpenAI)
    .fallback(chain)
    .build()?;
```

### 条件回退

```rust
let chain = FallbackChain::new()
    .primary("gpt-4o")
    .on_condition(|error| matches!(error, AiLibError::RateLimitExceeded(_)))
    .fallback("claude-3-haiku")
    .on_condition(|error| matches!(error, AiLibError::TimeoutError(_)))
    .fallback("mistral-medium")
    .always("gpt-3.5-turbo");
```

### 使用示例

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};

async fn resilient_chat(
    client: &AiClient,
    request: ChatCompletionRequest,
) -> Result<String, Box<dyn std::error::Error>> {
    let mut last_error = None;
    
    for provider in client.fallback_chain() {
        match provider.chat_completion(request.clone()).await {
            Ok(response) => return Ok(response.first_text()?),
            Err(error) => {
                last_error = Some(error);
                continue;
            }
        }
    }
    
    Err(last_error.unwrap_or("All providers failed".into()))
}
```

## 下一步

- 学习[可靠性概述](/docs/reliability-overview)了解其他可靠性功能
- 查看[重试机制](/docs/reliability-retry)了解重试策略
- 探索[熔断器](/docs/reliability-circuit)了解故障保护
