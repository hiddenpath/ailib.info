---
title: 发布 v0.4.0
group: 动态
order: 0
status: stable
---

# ai-lib v0.4.0

**发布日期：2025-12-04**

此版本标志着重大架构里程碑：**Trait Shift 1.0 演进**。核心调度机制已从基于枚举重新设计为基于 trait 的架构，提供更好的可扩展性和更清晰的抽象。

## 亮点

- **ChatProvider Trait**：所有提供商现在实现统一的 `ChatProvider` trait 以确保行为一致性
- **策略构建器**：通过 `with_failover_chain` 和 `with_round_robin_chain` 进行运行前路由组合
- **自定义提供商**：无需修改 `Provider` 枚举即可注入 OpenAI 兼容端点
- **改进的错误处理**：`AiClient::new` 现在返回 `Result<AiClient, AiLibError>` 以进行显式错误处理

## 破坏性变更

### AiClient::new 返回 Result

```rust
// ⛔️ 旧版（0.3.x）
let client = AiClient::new(Provider::Groq);

// ✅ 新版（0.4.0）
let client = AiClient::new(Provider::Groq)?;
```

### 基于策略的路由

```rust
// ⛔️ 旧版（0.3.x）- 基于哨兵的故障转移
let client = AiClient::new(Provider::OpenAI)
    .with_failover(vec![Provider::Anthropic, Provider::Groq]);

// ✅ 新版（0.4.0）- 策略构建器
let client = AiClientBuilder::new(Provider::OpenAI)
    .with_failover_chain(vec![Provider::Anthropic, Provider::Groq])?
    .build()?;
```

## 新功能

### 自定义提供商注入

```rust
use ai_lib::provider::builders::CustomProviderBuilder;

let custom = CustomProviderBuilder::new("my-gateway")
    .with_base_url("https://gateway.example.com/v1")
    .with_api_key_env("MY_GATEWAY_KEY")
    .with_default_chat_model("gpt-4")
    .build_provider()?;

let client = AiClientBuilder::new(Provider::OpenAI)
    .with_strategy(custom)
    .build()?;
```

### 轮询负载分配

```rust
let client = AiClientBuilder::new(Provider::OpenAI)
    .with_round_robin_chain(vec![Provider::Groq, Provider::Mistral])?
    .build()?;
```

## 升级

```toml
[dependencies]
ai-lib = "0.4.0"
tokio = { version = "1", features = ["full"] }
futures = "0.3"
```

## 文档

- [升级指南](/docs/UPGRADE_0.4.0.md) - 从 0.3.x 迁移到 0.4.0
- [API 参考](https://docs.rs/ai-lib/0.4.0) - 完整 API 文档
- [示例](https://github.com/hiddenpath/ai-lib/tree/main/examples) - 实用示例
