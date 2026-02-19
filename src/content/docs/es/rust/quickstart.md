---
title: Inicio rápido Rust
description: Comience con ai-lib-rust en minutos.
---

# Inicio rápido Rust

## Instalación

Agregue a su `Cargo.toml`:

```toml
[dependencies]
ai-lib-rust = { version = "0.8", features = ["full"] }
tokio = { version = "1", features = ["full"] }
futures = "0.3"
```

Use la característica `full` para habilitar todas las capacidades (embeddings, batch, guardrails, tokens, telemetry, routing_mvp, interceptors). O especifique solo las características que necesita, ej. `features = ["embeddings", "batch"]`.

## Configurar clave API

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

## Chat básico

```rust
use ai_lib_rust::{AiClient, Message};

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
    let client = AiClient::new("deepseek/deepseek-chat").await?;

    let response = client.chat()
        .user("Explain quantum computing in simple terms")
        .temperature(0.7)
        .max_tokens(500)
        .execute()
        .await?;

    println!("{}", response.content);
    Ok(())
}
```

## Streaming

```rust
use ai_lib_rust::{AiClient, StreamingEvent};
use futures::StreamExt;

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
    let client = AiClient::new("deepseek/deepseek-chat").await?;

    let mut stream = client.chat()
        .user("Write a haiku about Rust")
        .stream()
        .execute_stream()
        .await?;

    while let Some(event) = stream.next().await {
        match event? {
            StreamingEvent::ContentDelta { text, .. } => print!("{text}"),
            StreamingEvent::StreamEnd { .. } => println!(),
            _ => {}
        }
    }
    Ok(())
}
```

## Llamadas a herramientas

```rust
use ai_lib_rust::{AiClient, ToolDefinition, StreamingEvent};
use serde_json::json;
use futures::StreamExt;

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
    let client = AiClient::new("openai/gpt-4o").await?;

    let weather_tool = ToolDefinition {
        name: "get_weather".into(),
        description: Some("Get current weather".into()),
        parameters: json!({
            "type": "object",
            "properties": {
                "city": { "type": "string" }
            },
            "required": ["city"]
        }),
    };

    let mut stream = client.chat()
        .user("What's the weather in Tokyo?")
        .tools(vec![weather_tool])
        .stream()
        .execute_stream()
        .await?;

    while let Some(event) = stream.next().await {
        match event? {
            StreamingEvent::ToolCallStarted { name, .. } =>
                println!("Calling: {name}"),
            StreamingEvent::PartialToolCall { arguments, .. } =>
                print!("{arguments}"),
            StreamingEvent::ContentDelta { text, .. } =>
                print!("{text}"),
            _ => {}
        }
    }
    Ok(())
}
```

## Conversación multironda

```rust
use ai_lib_rust::{AiClient, Message, MessageRole};

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
    let client = AiClient::new("anthropic/claude-3-5-sonnet").await?;

    let messages = vec![
        Message::system("You are a helpful coding assistant."),
        Message::user("What is a closure in Rust?"),
    ];

    let response = client.chat()
        .messages(messages)
        .execute()
        .await?;

    println!("{}", response.content);
    Ok(())
}
```

## Con estadísticas

```rust
let (response, stats) = client.chat()
    .user("Hello!")
    .execute_with_stats()
    .await?;

println!("Content: {}", response.content);
println!("Total tokens: {}", stats.total_tokens);
println!("Latency: {}ms", stats.latency_ms);
```

## Próximos pasos

- **[API AiClient](/rust/client/)** — Referencia detallada de la API
- **[Canalización de streaming](/rust/streaming/)** — Cómo funciona el streaming
- **[Resiliencia](/rust/resilience/)** — Circuit breaker, limitación de velocidad
- **[Características avanzadas](/rust/advanced/)** — Embeddings, caché, plugins
