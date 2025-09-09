---
title: 智能路由
group: 可靠性
order: 40
status: stable
---

# 智能路由（稳定）

基于多端点 `ModelArray` 与负载策略进行模型选择，内置最小健康检查与指标。

## 基本用法（routing_mvp）

```rust
use ai_lib::{AiClientBuilder, ChatCompletionRequest, Message, Provider, Role};
use ai_lib::types::common::Content;
use ai_lib::provider::models::{ModelArray, ModelEndpoint, LoadBalancingStrategy};

// 1) 构建 ModelArray（多端点）
let mut array = ModelArray::new("prod").with_strategy(LoadBalancingStrategy::RoundRobin);
array.add_endpoint(ModelEndpoint {
    name: "groq-70b".to_string(),
    model_name: "llama-3.3-70b-versatile".to_string(),
    url: "https://api.groq.com".to_string(),
    weight: 1.0,
    healthy: true,
    connection_count: 0,
});

// 2) 通过 Builder 注入路由数组
let client = AiClientBuilder::new(Provider::Groq)
    .with_routing_array(array)
    .build()?;

// 3) 使用占位模型 "__route__" 触发路由选择
let req = ChatCompletionRequest::new(
    "__route__".to_string(),
    vec![Message { role: Role::User, content: Content::new_text("打个招呼"), function_call: None }]
);
let resp = client.chat_completion(req).await?;
println!("已选择模型: {}", resp.model);
```

## 健康检查与指标

- 最小健康检查：选择端点时，客户端会在使用前探测 `{base_url}`（或 OpenAI 兼容路径 `{base_url}/models`）。
- 路由指标（启用 `routing_mvp` 时）：
  - `routing_mvp.request`
  - `routing_mvp.selected`
  - `routing_mvp.health_fail`
  - `routing_mvp.fallback_default`
  - `routing_mvp.no_endpoint`
  - `routing_mvp.missing_array`

## 说明

- 当前为 MVP 形态：支持轮询/权重/最小健康检查；高级自适应策略与反馈闭环可在企业版演进。

## 下一步

- 学习[可靠性概述](/docs/reliability-overview)了解其他可靠性功能
- 查看[竞争策略](/docs/reliability-race)了解延迟优化
- 探索[回退链](/docs/reliability-fallback)了解故障转移
