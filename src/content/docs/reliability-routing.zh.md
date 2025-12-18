---
title: 智能路由
group: 可靠性
order: 40
status: stable
---

# 智能路由（稳定）

使用策略构建器组合路由策略，实现负载均衡、故障转移和智能提供商选择。

## 策略构建器（routing_mvp）

在运行时之前预先组合路由策略：

```rust
use ai_lib::{AiClientBuilder, ChatCompletionRequest, Message, Provider, Role, Content};

#[tokio::main]
async fn main() -> Result<(), AiLibError> {
    // 跨提供商的轮询负载分配
    let client = AiClientBuilder::new(Provider::OpenAI)
        .with_round_robin_chain(vec![Provider::Groq, Provider::Mistral])?
        .build()?;

    let req = ChatCompletionRequest::new(
        "gpt-4".to_string(), // 模型由选定的提供商解析
        vec![Message {
            role: Role::User,
            content: Content::Text("解释量子计算".to_string()),
            function_call: None
        }]
    );

    let resp = client.chat_completion(req).await?;
    println!("响应来自: {}", resp.model);
    Ok(())
}
```

## 故障转移链

创建有序的故障转移序列以实现高可用性：

```rust
use ai_lib::{AiClientBuilder, Provider};

// 主 → 备 → 第三优先级故障转移链
let client = AiClientBuilder::new(Provider::OpenAI)
    .with_failover_chain(vec![Provider::Anthropic, Provider::Groq])?
    .build()?;

// 如果 OpenAI 失败，自动尝试 Anthropic，然后是 Groq
let resp = client.chat_completion(request).await?;
```

## 健康检查与指标

策略构建器包含内置的健康验证：

- **端点健康**：在选择前使用基础 URL 探测验证提供商端点
- **自动回退**：发生故障时无缝切换到健康的提供商
- **连接池化**：跨提供商链的智能连接管理

### 路由指标（routing_mvp 特性）

启用时收集全面的路由遥测数据：

- `routing_mvp.request` - 路由请求总数
- `routing_mvp.selected` - 成功提供商选择
- `routing_mvp.health_fail` - 健康检查失败
- `routing_mvp.fallback_default` - 回退到默认提供商
- `routing_mvp.no_endpoint` - 无可用健康端点
- `routing_mvp.strategy_fail` - 策略组合失败

## 高级用法

### 自定义提供商注入

将策略构建器与自定义 OpenAI 兼容提供商结合：

```rust
use ai_lib::provider::builders::CustomProviderBuilder;

let custom_provider = CustomProviderBuilder::new("my-gateway")
    .with_base_url("https://custom.ai.gateway/v1")
    .with_api_key_env("CUSTOM_GATEWAY_KEY")
    .with_default_chat_model("gpt-4-turbo")
    .build_provider()?;

let client = AiClientBuilder::new(Provider::OpenAI)
    .with_strategy(custom_provider)
    .build()?;
```

## 说明

- 策略构建器在客户端构建时组合路由逻辑，而非运行时
- 链中的所有提供商必须健康才能获得最佳性能
- 高级路由策略（成本感知、延迟基础）可在 ai-lib-pro 中使用

## 下一步

- 学习[可靠性概述](/docs/reliability-overview)了解其他可靠性功能
- 查看[竞争策略](/docs/reliability-race)了解延迟优化
- 探索[回退链](/docs/reliability-fallback)了解故障转移
