---
title: Advanced Features (Rust)
description: Embeddings, caching, batching, plugins, guardrails, feature flags, structured output, and V2 error codes in ai-lib-rust v0.8.0.
---

# Advanced Features

Beyond core chat functionality, ai-lib-rust provides several advanced capabilities.

## Embeddings

Generate and work with vector embeddings:

```rust
use ai_lib_rust::embeddings::{EmbeddingClient, cosine_similarity};

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

Vector operations include cosine similarity, Euclidean distance, and dot product.

## Response Caching

Cache responses to reduce costs and latency:

```rust
use ai_lib_rust::cache::{CacheManager, MemoryCache};

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

## Batch Processing

Execute multiple requests efficiently:

```rust
use ai_lib_rust::batch::{BatchCollector, BatchExecutor};

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

## Token Counting

Estimate token usage and costs:

```rust
use ai_lib_rust::tokens::{TokenCounter, ModelPricing};

let counter = TokenCounter::for_model("gpt-4o");
let count = counter.count("Hello, how are you?");
println!("Tokens: {count}");

let pricing = ModelPricing::from_registry("openai/gpt-4o")?;
let cost = pricing.estimate(prompt_tokens, completion_tokens);
println!("Estimated cost: ${cost:.4}");
```

## Plugin System

Extend the client with custom plugins:

```rust
use ai_lib_rust::plugins::{Plugin, PluginRegistry};

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

Content filtering and safety:

```rust
use ai_lib_rust::guardrails::{GuardrailsConfig, KeywordFilter};

let config = GuardrailsConfig::new()
    .add_filter(KeywordFilter::new(vec!["unsafe_word"]))
    .enable_pii_detection();
```

## Feature-Gated: Routing

Smart model routing (enable with `routing_mvp` feature):

```rust
use ai_lib_rust::routing::{CustomModelManager, ModelArray, ModelSelectionStrategy};

let manager = CustomModelManager::new()
    .add_model("openai/gpt-4o", weight: 0.7)
    .add_model("anthropic/claude-3-5-sonnet", weight: 0.3)
    .strategy(ModelSelectionStrategy::Weighted);
```

## Feature-Gated: Interceptors

Request/response interception (enable with `interceptors` feature):

```rust
use ai_lib_rust::interceptors::{InterceptorPipeline, Interceptor};

let pipeline = InterceptorPipeline::new()
    .add(LoggingInterceptor)
    .add(MetricsInterceptor)
    .add(AuditInterceptor);
```
