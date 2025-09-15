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

## 基础故障转移（OSS）

`AiClient::with_failover(Vec<Provider>)` 提供轻量的提供商级故障转移：当出现可重试错误（网络、超时、限流、5xx）时，按顺序尝试备用 Provider。与 `routing_mvp` 配合时，已选择的模型会在故障转移过程中被保留。

```rust
use ai_lib::{AiClient, Provider};

let client = AiClient::new(Provider::OpenAI)?
    .with_failover(vec![Provider::Anthropic, Provider::Groq]);
```

> 注：高级带权重/成本与 SLO 感知的策略在 `ai-lib-pro` 中提供。

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
