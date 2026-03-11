---
title: 高度な機能（Go）
description: ai-lib-go v0.8.0 における埋め込み、キャッシュ、バッチ、プラグイン、ガードレール、フィーチャーフラグ、構造化出力、V2 エラーコード。
---

# 高度な機能

コアチャット機能に加え、ai-lib-go はいくつかの高度な機能を提供します。

## 埋め込み

ベクトル埋め込みの生成と操作：

```go
use ai_lib_go::embeddings::{EmbeddingClient, cosine_similarity};

let client = EmbeddingClient::builder()
    .model("openai/text-embedding-3-small")
    .build()
    .await?;

let embeddings = client.embed(vec![
    "Go programming language",
    "Python programming language",
    "Cooking recipes",
]).await?;

let sim = cosine_similarity(&embeddings[0], &embeddings[1]);
println!("Go vs Python similarity: {sim:.3}");
```

ベクトル操作にはコサイン類似度、ユークリッド距離、ドット積が含まれます。

## レスポンスキャッシュ

コストとレイテンシを削減するためのレスポンスキャッシュ：

```go
use ai_lib_go::cache::{CacheManager, MemoryCache};

let cache = CacheManager::new(MemoryCache::new())
    .with_ttl(Duration::from_secs(3600));

let client = AiClient::builder()
    .model("openai/gpt-4o")
    .cache(cache)
    .build()
    .await?;

// 最初の呼び出しはプロバイダーにヒット
let r1 = client.chat().user("What is 2+2?").execute().await?;

// 2 回目の同一呼び出しはキャッシュから返却
let r2 = client.chat().user("What is 2+2?").execute().await?;
```

## バッチ処理

複数リクエストを効率的に実行：

```go
use ai_lib_go::batch::{BatchCollector, BatchExecutor};

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

## トークンカウント

トークン使用量とコストの見積もり：

```go
use ai_lib_go::tokens::{TokenCounter, ModelPricing};

let counter = TokenCounter::for_model("gpt-4o");
let count = counter.count("Hello, how are you?");
println!("Tokens: {count}");

let pricing = ModelPricing::from_registry("openai/gpt-4o")?;
let cost = pricing.estimate(prompt_tokens, completion_tokens);
println!("Estimated cost: ${cost:.4}");
```

## プラグインシステム

カスタムプラグインでクライアントを拡張：

```go
use ai_lib_go::plugins::{Plugin, PluginRegistry};

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

## ガードレール

コンテンツフィルタリングとセーフティ：

```go
use ai_lib_go::guardrails::{GuardrailsConfig, KeywordFilter};

let config = GuardrailsConfig::new()
    .add_filter(KeywordFilter::new(vec!["unsafe_word"]))
    .enable_pii_detection();
```

## フィーチャーゲート：ルーティング

スマートモデルルーティング（`routing_mvp` フィーチャーで有効化）：

```go
use ai_lib_go::routing::{CustomModelManager, ModelArray, ModelSelectionStrategy};

let manager = CustomModelManager::new()
    .add_model("openai/gpt-4o", weight: 0.7)
    .add_model("anthropic/claude-3-5-sonnet", weight: 0.3)
    .strategy(ModelSelectionStrategy::Weighted);
```

## フィーチャーゲート：インターセプター

リクエスト/レスポンスのインターセプション（`interceptors` フィーチャーで有効化）：

```go
use ai_lib_go::interceptors::{InterceptorPipeline, Interceptor};

let pipeline = InterceptorPipeline::new()
    .add(LoggingInterceptor)
    .add(MetricsInterceptor)
    .add(AuditInterceptor);
```
