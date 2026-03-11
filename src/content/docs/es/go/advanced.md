---
title: Características avanzadas (Go)
description: Embeddings, caché, procesamiento por lotes, plugins, guardrails, banderas de características, salida estructurada y códigos de error V2 en ai-lib-go v0.8.0.
---

# Características avanzadas

Más allá de la funcionalidad principal de chat, ai-lib-go proporciona varias capacidades avanzadas.

## Embeddings

Genere y trabaje con embeddings vectoriales:

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

Las operaciones vectoriales incluyen similitud coseno, distancia euclidiana y producto escalar.

## Caché de respuestas

Almacene en caché las respuestas para reducir costos y latencia:

```go
use ai_lib_go::cache::{CacheManager, MemoryCache};

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

## Procesamiento por lotes

Ejecute múltiples solicitudes eficientemente:

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

## Conteo de tokens

Estime el uso de tokens y costos:

```go
use ai_lib_go::tokens::{TokenCounter, ModelPricing};

let counter = TokenCounter::for_model("gpt-4o");
let count = counter.count("Hello, how are you?");
println!("Tokens: {count}");

let pricing = ModelPricing::from_registry("openai/gpt-4o")?;
let cost = pricing.estimate(prompt_tokens, completion_tokens);
println!("Estimated cost: ${cost:.4}");
```

## Sistema de plugins

Extienda el cliente con plugins personalizados:

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

## Guardrails

Filtrado de contenido y seguridad:

```go
use ai_lib_go::guardrails::{GuardrailsConfig, KeywordFilter};

let config = GuardrailsConfig::new()
    .add_filter(KeywordFilter::new(vec!["unsafe_word"]))
    .enable_pii_detection();
```

## Con puerta de características: Routing

Enrutamiento inteligente de modelos (habilitar con característica `routing_mvp`):

```go
use ai_lib_go::routing::{CustomModelManager, ModelArray, ModelSelectionStrategy};

let manager = CustomModelManager::new()
    .add_model("openai/gpt-4o", weight: 0.7)
    .add_model("anthropic/claude-3-5-sonnet", weight: 0.3)
    .strategy(ModelSelectionStrategy::Weighted);
```

## Con puerta de características: Interceptors

Interceptación de solicitudes/respuestas (habilitar con característica `interceptors`):

```go
use ai_lib_go::interceptors::{InterceptorPipeline, Interceptor};

let pipeline = InterceptorPipeline::new()
    .add(LoggingInterceptor)
    .add(MetricsInterceptor)
    .add(AuditInterceptor);
```
