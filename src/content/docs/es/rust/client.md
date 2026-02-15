---
title: API AiClient (Rust)
description: Guía detallada para usar AiClient, ChatRequestBuilder y tipos de respuesta en ai-lib-rust v0.7.1.
---

# API AiClient

## Crear un cliente

### A partir del identificador de modelo

```rust
// Automatic protocol loading
let client = AiClient::new("anthropic/claude-3-5-sonnet").await?;
```

### Con el constructor

```rust
let client = AiClient::builder()
    .model("openai/gpt-4o")
    .protocol_dir("./ai-protocol")
    .timeout(Duration::from_secs(60))
    .build()
    .await?;
```

## ChatRequestBuilder

El patrón builder proporciona una API fluida:

```rust
let response = client.chat()
    // Messages
    .system("You are a helpful assistant")
    .user("Hello!")
    .messages(vec![Message::user("Follow-up")])

    // Parameters
    .temperature(0.7)
    .max_tokens(1000)
    .top_p(0.9)
    .stop(vec!["END".into()])

    // Tools
    .tools(vec![weather_tool])
    .tool_choice("auto")

    // Execution
    .execute()
    .await?;
```

## Tipos de respuesta

### ChatResponse

```rust
pub struct ChatResponse {
    pub content: String,         // Response text
    pub tool_calls: Vec<ToolCall>, // Function calls (if any)
    pub finish_reason: String,    // Why the response ended
    pub usage: Usage,             // Token usage
}
```

### StreamingEvent

```rust
pub enum StreamingEvent {
    ContentDelta { text: String, index: usize },
    ThinkingDelta { text: String },
    ToolCallStarted { id: String, name: String, index: usize },
    PartialToolCall { id: String, arguments: String, index: usize },
    ToolCallEnded { id: String, index: usize },
    StreamEnd { finish_reason: Option<String>, usage: Option<Usage> },
    Metadata { model: Option<String>, usage: Option<Usage> },
}
```

### CallStats

```rust
pub struct CallStats {
    pub total_tokens: u32,
    pub prompt_tokens: u32,
    pub completion_tokens: u32,
    pub latency_ms: u64,
    pub model: String,
    pub provider: String,
}
```

## Modos de ejecución

### No streaming

```rust
// Simple response
let response = client.chat().user("Hello").execute().await?;

// Response with statistics
let (response, stats) = client.chat().user("Hello").execute_with_stats().await?;
```

### Streaming

```rust
let mut stream = client.chat()
    .user("Hello")
    .stream()
    .execute_stream()
    .await?;

while let Some(event) = stream.next().await {
    // Handle each StreamingEvent
}
```

### Cancelación del flujo

```rust
let (mut stream, cancel_handle) = client.chat()
    .user("Long task...")
    .stream()
    .execute_stream_cancellable()
    .await?;

// Cancel from another task
tokio::spawn(async move {
    tokio::time::sleep(Duration::from_secs(5)).await;
    cancel_handle.cancel();
});
```

## Manejo de errores

```rust
use ai_lib::{Error, ErrorContext};

match client.chat().user("Hello").execute().await {
    Ok(response) => println!("{}", response.content),
    Err(Error::Protocol(e)) => eprintln!("Protocol error: {e}"),
    Err(Error::Transport(e)) => eprintln!("HTTP error: {e}"),
    Err(Error::Remote(e)) => {
        eprintln!("Provider error: {}", e.error_type);
        // e.error_type is one of the 13 standard error classes
    }
    Err(e) => eprintln!("Other error: {e}"),
}
```

Todos los errores incluyen códigos de error estándar V2 a través de `ErrorContext`. Use `error.context().standard_code` para acceder a la enumeración `StandardErrorCode` (E1001–E9999) para un manejo programático.

## Operaciones por lotes

Ejecute varias solicitudes de chat en paralelo:

```rust
// Execute multiple chat requests in parallel
let results = client.chat_batch(requests, 5).await; // concurrency limit = 5

// Smart batching with automatic concurrency tuning
let results = client.chat_batch_smart(requests).await;
```

## Validación de solicitudes

Valide una solicitud contra el manifiesto del protocolo antes de enviarla:

```rust
// Validate a request against the protocol manifest before sending
client.validate_request(&request)?;
```

## Retroalimentación y observabilidad

Reporte eventos de retroalimentación para RLHF y monitoreo, e inspeccione el estado de resiliencia:

```rust
// Report feedback events for RLHF / monitoring
client.report_feedback(FeedbackEvent::Rating(RatingFeedback {
    request_id: "req-123".into(),
    rating: 5,
    max_rating: 5,
    category: None,
    comment: Some("Great response".into()),
    timestamp: chrono::Utc::now(),
})).await?;

// Get current resilience state
let signals = client.signals().await;
println!("Circuit: {:?}", signals.circuit_breaker);
```

## Configuración del constructor

Use `AiClientBuilder` para configuración avanzada:

```rust
let client = AiClientBuilder::new()
    .protocol_path("path/to/protocols".into())
    .hot_reload(true)
    .with_fallbacks(vec!["openai/gpt-4o".into()])
    .feedback_sink(my_sink)
    .max_inflight(10)
    .circuit_breaker_default()
    .rate_limit_rps(5.0)
    .base_url_override("https://my-proxy.example.com")
    .build("anthropic/claude-3-5-sonnet")
    .await?;
```

## Próximos pasos

- **[Canalización de streaming](/rust/streaming/)** — Cómo la canalización procesa los flujos
- **[Resiliencia](/rust/resilience/)** — Patrones de confiabilidad
- **[Características avanzadas](/rust/advanced/)** — Embeddings, caché, plugins
