---
title: 高级功能（Rust）
description: ai-lib-rust v0.7.1 中的 embeddings、缓存、批处理、插件、guardrails、功能标志、结构化输出及 V2 错误码。
---

# 高级功能

除核心聊天功能外，ai-lib-rust 还提供多项高级能力。

## Embeddings

生成并处理向量 embedding：

```rust
use ai_lib::embeddings::{EmbeddingClient, cosine_similarity};

let client = EmbeddingClient::builder()
    .model("openai/text-embedding-3-small")
    .build()
    .await?;

let embeddings = client.embed(vec![
    "Rust programming language",
    "Python programming language",
    "Cooking recipes",
]).await?;

let sim = cosine_similarity(&embeddings[0], &embeddings[1]);
println!("Rust vs Python similarity: {sim:.3}");
```

向量操作包括余弦相似度、欧几里得距离和点积。

## 响应缓存

缓存响应以降低成本和延迟：

```rust
use ai_lib::cache::{CacheManager, MemoryCache};

let cache = CacheManager::new(MemoryCache::new())
    .with_ttl(Duration::from_secs(3600));

let client = AiClient::builder()
    .model("openai/gpt-4o")
    .cache(cache)
    .build()
    .await?;

// First call hits the provider
let r1 = client.chat().user("What is 2+2?").execute().await?;

// Second identical call returns cached response
let r2 = client.chat().user("What is 2+2?").execute().await?;
```

## 批处理

高效执行多个请求：

```rust
use ai_lib::batch::{BatchCollector, BatchExecutor};

let mut collector = BatchCollector::new();
collector.add(client.chat().user("Question 1"));
collector.add(client.chat().user("Question 2"));
collector.add(client.chat().user("Question 3"));

let executor = BatchExecutor::new()
    .concurrency(5)
    .timeout(Duration::from_secs(30));

let results = executor.execute(collector).await;
for result in results {
    match result {
        Ok(response) => println!("{}", response.content),
        Err(e) => eprintln!("Error: {e}"),
    }
}
```

## Token 计数

估算 token 使用量与成本：

```rust
use ai_lib::tokens::{TokenCounter, ModelPricing};

let counter = TokenCounter::for_model("gpt-4o");
let count = counter.count("Hello, how are you?");
println!("Tokens: {count}");

let pricing = ModelPricing::from_registry("openai/gpt-4o")?;
let cost = pricing.estimate(prompt_tokens, completion_tokens);
println!("Estimated cost: ${cost:.4}");
```

## 插件系统

使用自定义插件扩展客户端：

```rust
use ai_lib::plugins::{Plugin, PluginRegistry};

struct LoggingPlugin;

impl Plugin for LoggingPlugin {
    fn name(&self) -> &str { "logging" }

    fn on_request(&self, request: &mut Request) {
        tracing::info!("Sending request to {}", request.model);
    }

    fn on_response(&self, response: &Response) {
        tracing::info!("Got {} tokens", response.usage.total_tokens);
    }
}

let mut registry = PluginRegistry::new();
registry.register(LoggingPlugin);
```

## Guardrails

内容过滤与安全：

```rust
use ai_lib::guardrails::{GuardrailsConfig, KeywordFilter};

let config = GuardrailsConfig::new()
    .add_filter(KeywordFilter::new(vec!["unsafe_word"]))
    .enable_pii_detection();
```

## 功能门控：Routing

智能模型路由（使用 `routing_mvp` 功能启用）：

```rust
use ai_lib::routing::{CustomModelManager, ModelArray, ModelSelectionStrategy};

let manager = CustomModelManager::new()
    .add_model("openai/gpt-4o", weight: 0.7)
    .add_model("anthropic/claude-3-5-sonnet", weight: 0.3)
    .strategy(ModelSelectionStrategy::Weighted);
```

## 功能门控：Interceptors

请求/响应拦截（使用 `interceptors` 功能启用）：

```rust
use ai_lib::interceptors::{InterceptorPipeline, Interceptor};

let pipeline = InterceptorPipeline::new()
    .add(LoggingInterceptor)
    .add(MetricsInterceptor)
    .add(AuditInterceptor);
```
