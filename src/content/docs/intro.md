---
title: Introduction
group: Overview
order: 10
description: Overview of ai-lib (Rust unified AI SDK) goals and capabilities.
---

# Introduction

ai-lib is a production-grade Rust crate providing a unified, reliability-focused multi‑provider AI SDK. It eliminates the complexity of integrating with multiple AI providers by offering a single, consistent interface.

> Announcement: v0.5.0 released — Complete Starlight migration, premium Tailwind design, and Mermaid architecture diagrams. For advanced enterprise capabilities, explore [ai-lib-pro](/docs/enterprise-pro).

## Goals

- **Reduce integration cost** across 20+ AI providers
- **Improve success rate & tail latency** via built-in reliability primitives
- **Offer consistent streaming & function calling** semantics across all providers
- **Remain vendor-neutral and extensible** with pluggable transport and metrics

## Key Features

- **Unified API** for chat completions across all supported providers
- **Streaming support** with consistent delta handling (SSE + emulated fallback)
- **Function calling** with normalized tool schemas and policies
- **Multimodal content** support (text, images, audio) where providers support it
- **Reliability primitives**: retry with exponential backoff, circuit breaker, rate limiting
- **Model management**: performance-based selection, load balancing, health monitoring
- **Batch processing** with configurable concurrency limits
- **Observability hooks** for custom metrics and monitoring integration
- **Progressive configuration** from environment variables to explicit builder patterns

## Supported Providers

ai-lib supports 20+ AI providers including OpenAI, Groq, Anthropic, Gemini, Mistral, Cohere, Azure OpenAI, Ollama, DeepSeek, Qwen, Baidu Wenxin, Tencent Hunyuan, iFlytek Spark, Moonshot Kimi, HuggingFace, TogetherAI, xAI Grok, OpenRouter, Replicate, Perplexity, AI21, ZhipuAI, and MiniMax.

## Quick Start

```rust
use ai_lib::prelude::*;

#[tokio::main]
async fn main() -> Result<(), AiLibError> {
    let client = AiClient::new(Provider::Groq)?;
    let req = ChatCompletionRequest::new(
        client.default_chat_model(),
        vec![Message {
            role: Role::User,
            content: Content::new_text("Hello, world!".to_string()),
            function_call: None,
        }]
    );
    let resp = client.chat_completion(req).await?;
    println!("Answer: {}", resp.choices[0].message.content.as_text());
    Ok(())
}
```

Next: Read [Getting Started](/docs/getting-started), then see [Features & Optional Modules](/docs/features), and explore [Advanced Examples](/docs/advanced-examples).
