---
title: Inicio r谩pido
description: Comience con AI-Lib en menos de 5 minutos 鈥?elija Rust o Python.
---

# Inicio r谩pido

Elija su tiempo de ejecuci贸n y comience a realizar llamadas de IA en minutos.

## Requisitos previos

- Una clave API de cualquier proveedor compatible (por ejemplo, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`)
- El repositorio AI-Protocol (se obtiene autom谩ticamente de GitHub si no es local)

## Rust

### 1. Agregue la dependencia

```toml
[dependencies]
ai-lib = "0.7"
tokio = { version = "1", features = ["full"] }
```

### 2. Configure su clave API

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 3. Escriba su primer programa

```rust
use ai_lib_rust::{AiClient, StreamingEvent};
use futures::StreamExt;

#[tokio::main]
async fn main() -> ai_lib_rust::Result<()> {
    // Create client 鈥?protocol manifest is loaded automatically
    let client = AiClient::new("anthropic/claude-3-5-sonnet").await?;

    // Streaming chat
    let mut stream = client.chat()
        .user("What is AI-Protocol?")
        .temperature(0.7)
        .max_tokens(500)
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

### 4. Ejecute

```bash
cargo run
```

## Python

### 1. Instale el paquete

```bash
pip install ai-lib-python>=1.0.0
```

### 2. Configure su clave API

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 3. Escriba su primer script

```python
import asyncio
from ai_lib_python import AiClient

async def main():
    # Create client 鈥?protocol manifest loaded automatically
    client = await AiClient.create("anthropic/claude-3-5-sonnet")

    # Streaming chat
    async for event in client.chat() \
        .user("What is AI-Protocol?") \
        .temperature(0.7) \
        .max_tokens(500) \
        .stream():
        if event.is_content_delta:
            print(event.as_content_delta.text, end="")
    print()

asyncio.run(main())
```

### 4. Ejecute

```bash
python main.py
```

## Cambio de proveedores

La magia de AI-Lib: cambie una cadena para cambiar de proveedor.

```rust
// Rust 鈥?just change the model ID
let client = AiClient::new("openai/gpt-4o").await?;
let client = AiClient::new("deepseek/deepseek-chat").await?;
let client = AiClient::new("gemini/gemini-2.0-flash").await?;
```

```python
# Python 鈥?same thing
client = await AiClient.create("openai/gpt-4o")
client = await AiClient.create("deepseek/deepseek-chat")
client = await AiClient.create("gemini/gemini-2.0-flash")
```

No se necesitan cambios de c贸digo. El manifiesto del protocolo maneja endpoint, autenticaci贸n, mapeo de par谩metros y formato de streaming para cada proveedor.

## Pr贸ximos pasos

- **[Arquitectura del ecosistema](/ecosystem/)** 鈥?C贸mo encajan las piezas
- **[Gu铆a de Chat Completions](/guides/chat/)** 鈥?Uso detallado de la API de chat
- **[Llamadas a funciones](/guides/tools/)** 鈥?Uso de herramientas y llamadas a funciones
- **[Detalles del SDK Rust](/rust/overview/)** 鈥?Profundice en Rust
- **[Detalles del SDK Python](/python/overview/)** 鈥?Profundice en Python
