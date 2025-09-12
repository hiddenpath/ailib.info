---
title: 快速开始
group: 概述
order: 20
description: 在Rust中安装并运行你的第一个聊天调用。
---

# 快速开始

ai-lib为17+个AI提供商提供统一的Rust接口。本指南将在几分钟内让你上手。

## 添加依赖

将ai-lib添加到你的`Cargo.toml`中：

```toml
[dependencies]
ai-lib = "0.3.2"
tokio = { version = "1", features = ["full"] }
futures = "0.3"
```

## 快速开始

最简单的开始方式是进行一个简单的聊天请求：

```rust
use ai_lib::{AiClient, Provider, Message, Role, Content, ChatCompletionRequest};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 选择你的AI提供商
    let client = AiClient::new(Provider::Groq)?;

    // 创建聊天请求
    let req = ChatCompletionRequest::new(
        client.default_chat_model(),
        vec![Message {
            role: Role::User,
            content: Content::Text("用一句话解释transformer模型。".to_string()),
            function_call: None,
        }]
    );

    // 发送请求
    let resp = client.chat_completion(req).await?;

    // 获取响应文本
    println!("回答: {}", resp.choices[0].message.content.as_text());
    Ok(())
}
```

## 环境变量

设置你的API密钥作为环境变量：

```bash
# Groq
export GROQ_API_KEY=your_groq_api_key

# OpenAI
export OPENAI_API_KEY=your_openai_api_key

# Anthropic
export ANTHROPIC_API_KEY=your_anthropic_api_key

# 其他提供商，请查看[提供商](/docs/providers)页面的完整列表
```

## 流式示例

对于实时响应，使用流式处理：

```rust
use futures::StreamExt;

let mut stream = client.chat_completion_stream(req).await?;
while let Some(chunk) = stream.next().await {
    let c = chunk?;
    if let Some(delta) = c.choices[0].delta.content.clone() {
        print!("{delta}");
    }
}
```

## 函数调用

ai-lib支持统一接口的函数调用：

```rust
use ai_lib::{Tool, FunctionCallPolicy};

let tool = Tool::new_json(
    "get_weather",
    Some("获取当前天气信息"),
    serde_json::json!({
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "城市名称"}
        },
        "required": ["location"]
    })
);

let req = ChatCompletionRequest::new(model, messages)
    .with_functions(vec![tool])
    .with_function_call(FunctionCallPolicy::Auto);
```

## 代理配置（可选）

如需要，配置代理设置：

```bash
export AI_PROXY_URL=http://proxy.example.com:8080
```

或者通过编程方式设置：

```rust
use ai_lib::{AiClient, Provider, ConnectionOptions};

let client = AiClient::with_options(
    Provider::Groq,
    ConnectionOptions {
        proxy: Some("http://proxy.example.com:8080".into()),
        ..Default::default()
    }
)?;
```

## 企业级功能

对于生产环境和企业需求，请考虑[ai-lib-pro](/docs/enterprise-pro)：

- **高级路由**：策略驱动路由、健康监控、自动故障转移
- **企业可观测性**：结构化日志、指标、分布式追踪
- **成本管理**：集中化定价表和预算跟踪
- **配额管理**：租户/组织配额和速率限制
- **审计与合规**：全面的审计跟踪和脱敏处理
- **安全性**：信封加密和密钥管理
- **配置管理**：热重载配置管理

## 下一步

- **流式处理**：在[聊天与流式处理](/docs/chat)中学习实时响应
- **可靠性**：在[可靠性概述](/docs/reliability-overview)中探索重试、熔断器和回退策略
- **高级功能**：查看[高级示例](/docs/advanced-examples)
- **提供商详情**：在[提供商](/docs/providers)中查看所有支持的提供商
- **企业版**：探索[ai-lib-pro](/docs/enterprise-pro)的高级企业功能
