---
title: 重试
group: 可靠性
order: 10
status: stable
---

# 重试（稳定）

指数退避加抖动是预期方法；检查当前crate版本以获取暴露的配置API。典型的Rust模式（如果尚未稳定则为伪代码）：

```rust
// let policy = RetryPolicy { attempts: 3, base_delay: Duration::from_millis(200), max_delay: Duration::from_secs(2) };
// let client = AiClientBuilder::new(Provider::OpenAI).retry(policy).build()?;
```

通常重试的错误：网络/瞬态传输问题、HTTP 5xx、带重试头的速率限制。使用幂等键保护副作用工具执行或在模型推理后执行。

## 重试策略

重试是处理瞬态错误的重要机制，通过指数退避和抖动来避免雪崩效应。

### 基本配置

```rust
use ai_lib::reliability::RetryPolicy;

let policy = RetryPolicy {
    attempts: 3,
    base_delay: Duration::from_millis(200),
    max_delay: Duration::from_secs(2),
    jitter: true,
    backoff_multiplier: 2.0,
};

let client = AiClientBuilder::new(Provider::OpenAI)
    .retry(policy)
    .build()?;
```

### 高级配置

```rust
let policy = RetryPolicy {
    attempts: 5,
    base_delay: Duration::from_millis(100),
    max_delay: Duration::from_secs(10),
    jitter: true,
    backoff_multiplier: 1.5,
    retryable_errors: vec![
        "NetworkError",
        "TimeoutError",
        "RateLimitExceeded",
        "ServerError",
    ],
    non_retryable_errors: vec![
        "AuthenticationError",
        "InvalidRequest",
    ],
};
```

### 使用示例

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};

async fn retry_chat(
    client: &AiClient,
    request: ChatCompletionRequest,
) -> Result<String, Box<dyn std::error::Error>> {
    let mut last_error = None;
    
    for attempt in 1..=client.retry_policy().attempts {
        match client.chat_completion(request.clone()).await {
            Ok(response) => return Ok(response.first_text()?),
            Err(error) => {
                last_error = Some(error);
                
                if !client.retry_policy().should_retry(&error) {
                    break;
                }
                
                if attempt < client.retry_policy().attempts {
                    let delay = client.retry_policy().calculate_delay(attempt);
                    tokio::time::sleep(delay).await;
                }
            }
        }
    }
    
    Err(last_error.unwrap_or("All retry attempts failed".into()))
}
```

## 下一步

- 学习[可靠性概述](/docs/reliability-overview)了解其他可靠性功能
- 查看[回退链](/docs/reliability-fallback)了解故障转移
- 探索[熔断器](/docs/reliability-circuit)了解故障保护
