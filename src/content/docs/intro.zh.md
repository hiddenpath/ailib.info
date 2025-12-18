---
title: 介绍
group: 概述
order: 10
description: ai-lib（Rust统一AI SDK）的目标和功能概述。
---

# 介绍

ai-lib是一个生产级的Rust库，提供统一、注重可靠性的多提供商AI SDK。它通过提供单一、一致的接口，消除了与多个AI提供商集成的复杂性。

> 通知：v0.4.0 已发布 —— Trait Shift 1.0 演进，统一 `ChatProvider` 架构，以及增强的客户端能力。如需企业能力，请探索[ai-lib-pro](/docs/enterprise-pro)。

## 目标

- **降低集成成本**：支持20+个AI提供商
- **提高成功率和尾延迟**：通过内置的可靠性原语
- **提供一致的流式处理和函数调用**：跨所有提供商的语义
- **保持提供商中立和可扩展性**：支持可插拔的传输和指标

## 核心功能

- **统一API**：跨所有支持的提供商的聊天完成接口
- **流式支持**：一致的增量处理（SSE + 模拟回退）
- **函数调用**：标准化的工具模式和策略
- **多模态内容**：支持文本、图像、音频（在提供商支持的地方）
- **可靠性原语**：指数退避重试、熔断器、速率限制
- **模型管理**：基于性能的选择、负载均衡、健康监控
- **批处理**：可配置并发限制的批处理
- **可观测性钩子**：自定义指标和监控集成
- **渐进式配置**：从环境变量到显式构建器模式

## 支持的提供商

ai-lib支持20+个AI提供商，包括OpenAI、Groq、Anthropic、Gemini、Mistral、Cohere、Azure OpenAI、Ollama、DeepSeek、Qwen、百度文心、腾讯混元、科大讯飞星火、月之暗面Kimi、HuggingFace、TogetherAI、xAI Grok，以及 OpenRouter、Replicate、Perplexity、AI21、智谱AI、MiniMax。

## 快速开始

```rust
use ai_lib::prelude::*;

#[tokio::main]
async fn main() -> Result<(), AiLibError> {
    let client = AiClient::new(Provider::Groq)?;
    let req = ChatCompletionRequest::new(
        client.default_chat_model(),
        vec![Message {
            role: Role::User,
            content: Content::new_text("你好，世界！".to_string()),
            function_call: None,
        }]
    );
    let resp = client.chat_completion(req).await?;
    println!("回答: {}", resp.choices[0].message.content.as_text());
    Ok(())
}
```

下一步：阅读[快速开始](/docs/getting-started)，再查看[特性开关（Features）](/docs/features.zh)，最后探索[高级示例](/docs/advanced-examples)。
