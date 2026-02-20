---
title: Completaciones de chat
description: Guía para usar completaciones de chat entre proveedores con los tiempos de ejecución de AI-Lib.
---

# Completaciones de chat

Las completaciones de chat son la API principal para interactuar con los modelos de IA. Ambos tiempos de ejecución proporcionan una interfaz unificada que funciona con todos los 37 proveedores.

## Uso básico

### Rust

```rust
let client = AiClient::new("openai/gpt-4o").await?;

let response = client.chat()
    .user("Hello, world!")
    .execute()
    .await?;

println!("{}", response.content);
```

### Python

```python
client = await AiClient.create("openai/gpt-4o")

response = await client.chat() \
    .user("Hello, world!") \
    .execute()

print(response.content)
```

## Mensajes

### Mensajes del sistema

Configure el comportamiento del modelo:

```rust
// Rust
client.chat()
    .system("You are a helpful coding assistant. Always include code examples.")
    .user("Explain closures")
    .execute().await?;
```

```python
# Python
await client.chat() \
    .system("You are a helpful coding assistant.") \
    .user("Explain closures") \
    .execute()
```

### Conversaciones multironda

Pase el historial de conversación:

```rust
// Rust
use ai_lib_rust::{Message, MessageRole};

let messages = vec![
    Message::system("You are a tutor."),
    Message::user("What is recursion?"),
    Message::assistant("Recursion is when a function calls itself..."),
    Message::user("Can you show an example?"),
];

client.chat().messages(messages).execute().await?;
```

```python
# Python
from ai_lib_python import Message

messages = [
    Message.system("You are a tutor."),
    Message.user("What is recursion?"),
    Message.assistant("Recursion is when a function calls itself..."),
    Message.user("Can you show an example?"),
]

await client.chat().messages(messages).execute()
```

## Parámetros

| Parameter | Type | Description |
|-----------|------|-------------|
| `temperature` | float | Aleatoriedad (0.0 = determinístico, 2.0 = creativo) |
| `max_tokens` | int | Longitud máxima de la respuesta |
| `top_p` | float | Muestreo por núcleo (alternativa a temperature) |
| `stop` | string[] | Secuencias que detienen la generación |

```rust
// Rust
client.chat()
    .user("Write a poem")
    .temperature(0.9)
    .max_tokens(200)
    .top_p(0.95)
    .execute().await?;
```

## Streaming

Para salida en tiempo real, use streaming:

```rust
// Rust
let mut stream = client.chat()
    .user("Tell me a story")
    .stream()
    .execute_stream()
    .await?;

while let Some(event) = stream.next().await {
    if let StreamingEvent::ContentDelta { text, .. } = event? {
        print!("{text}");
        std::io::stdout().flush()?;
    }
}
```

```python
# Python
async for event in client.chat() \
    .user("Tell me a story") \
    .stream():
    if event.is_content_delta:
        print(event.as_content_delta.text, end="", flush=True)
```

## Estadísticas de respuesta

Rastree el uso para gestión de costos:

```rust
// Rust
let (response, stats) = client.chat()
    .user("Hello")
    .execute_with_stats()
    .await?;

println!("Prompt tokens: {}", stats.prompt_tokens);
println!("Completion tokens: {}", stats.completion_tokens);
println!("Latency: {}ms", stats.latency_ms);
```

```python
# Python
response, stats = await client.chat() \
    .user("Hello") \
    .execute_with_stats()

print(f"Tokens: {stats.total_tokens}")
print(f"Latency: {stats.latency_ms}ms")
```

## Cambio de proveedores

El mismo código funciona con todos los proveedores:

```rust
// Just change the model identifier
let client = AiClient::new("anthropic/claude-3-5-sonnet").await?;
let client = AiClient::new("deepseek/deepseek-chat").await?;
let client = AiClient::new("gemini/gemini-2.0-flash").await?;
```

El manifiesto del protocolo maneja las URLs de endpoints, autenticación, mapeo de parámetros y diferencias de formato de streaming automáticamente.
