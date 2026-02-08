---
title: 竞争/对冲
group: 可靠性
order: 30
status: stable
---

# 竞争/对冲（稳定）

同时启动多个竞争者或带小延迟；第一个成功响应获胜并取消其余。

```rust
// let race = RacePolicy::new()
//   .contender("gpt-4o", Duration::from_millis(0))
//   .contender("claude-3-haiku", Duration::from_millis(120))
//   .cancel_others(true);
```

用于交互式延迟敏感流程（聊天UI）。成本随冗余令牌增加。

## 竞争策略实现

竞争策略是一种通过同时启动多个请求来减少延迟的技术。

### 基本配置

```rust
use ai_lib::reliability::RacePolicy;

let race = RacePolicy::new()
    .contender("gpt-4o", Duration::from_millis(0))
    .contender("claude-3-haiku", Duration::from_millis(120))
    .contender("mistral-medium", Duration::from_millis(240))
    .cancel_others(true)
    .timeout(Duration::from_secs(30));

let client = AiClientBuilder::new(Provider::OpenAI)
    .race(race)
    .build()?;
```

### 使用示例

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};

async fn race_chat(
    client: &AiClient,
    request: ChatCompletionRequest,
) -> Result<String, Box<dyn std::error::Error>> {
    let race_result = client.race_chat_completion(request).await?;
    
    match race_result {
        Ok(response) => Ok(response.first_text()?),
        Err(error) => Err(error.into()),
    }
}
```

## 下一步

- 学习[可靠性概述](/docs/reliability-overview)了解其他可靠性功能
- 查看[智能路由](/docs/reliability-routing)了解路由策略
- 探索[回退链](/docs/reliability-fallback)了解故障转移
