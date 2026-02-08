---
title: 回退链
group: 可靠性
order: 20
status: stable
---

# 回退链（稳定）

定义有序的故障转移序列，在失败时自动前进到下一个提供商。第一个成功会短路整个链。

## 策略构建器（OSS）

在构建时组合确定性的故障转移链：

```rust
use ai_lib::{AiClientBuilder, Provider};

#[tokio::main]
async fn main() -> Result<(), AiLibError> {
    // 主 → 备 → 第三优先级故障转移链
    let client = AiClientBuilder::new(Provider::OpenAI)
        .with_failover_chain(vec![Provider::Anthropic, Provider::Groq])?
        .build()?;

    let request = ChatCompletionRequest::new(
        "gpt-4".to_string(),
        vec![Message::user("解释量子计算")]
    );

    // 自动尝试 OpenAI，然后 Anthropic，最后 Groq（如果失败）
    let response = client.chat_completion(request).await?;
    println!("响应: {}", response.choices[0].message.content.as_text());
    Ok(())
}
```

## 行为特性

- **有序执行**：按照指定顺序尝试提供商
- **短路机制**：第一个成功的响应立即返回
- **错误传递**：仅在链中所有提供商都失败时才返回错误
- **健康验证**：不健康的提供商会被自动跳过

## 高级用法

与自定义提供商结合以实现完全控制：

```rust
use ai_lib::provider::builders::CustomProviderBuilder;

// 混合标准提供商与自定义端点
let custom = CustomProviderBuilder::new("backup-gateway")
    .with_base_url("https://backup.ai.gateway/v1")
    .with_api_key_env("BACKUP_API_KEY")
    .build_provider()?;

let client = AiClientBuilder::new(Provider::OpenAI)
    .with_strategy(custom)
    .with_failover_chain(vec![Provider::Anthropic])?
    .build()?;
```

> 注：带权重/成本与 SLO 感知策略在 `ai-lib-pro` 中提供。

## 下一步

- 学习[可靠性概述](/docs/reliability-overview)了解其他可靠性功能
- 查看[重试机制](/docs/reliability-retry)了解重试策略
- 探索[熔断器](/docs/reliability-circuit)了解故障保护
