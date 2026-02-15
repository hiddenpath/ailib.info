---
title: Multimodal
description: Uso de capacidades de visión y multimodales con AI-Lib.
---

# Multimodal

AI-Lib soporta entradas multimodales — texto combinado con imágenes — a través de la misma API unificada.

## Capacidades compatibles

| Capability | Providers |
|-----------|-----------|
| Vision (imágenes) | OpenAI, Anthropic, Gemini, Qwen |
| Entrada de audio | Limitado (Gemini) |

## Enviar imágenes

### Rust

```rust
use ai_lib::{AiClient, Message, ContentBlock};

let client = AiClient::from_model("openai/gpt-4o").await?;

let message = Message::user_with_content(vec![
    ContentBlock::Text("What's in this image?".into()),
    ContentBlock::ImageUrl {
        url: "https://example.com/photo.jpg".into(),
    },
]);

let response = client.chat()
    .messages(vec![message])
    .execute()
    .await?;

println!("{}", response.content);
```

### Python

```python
from ai_lib_python import AiClient, Message, ContentBlock

client = await AiClient.create("openai/gpt-4o")

message = Message.user_with_content([
    ContentBlock.text("What's in this image?"),
    ContentBlock.image_url("https://example.com/photo.jpg"),
])

response = await client.chat() \
    .messages([message]) \
    .execute()

print(response.content)
```

## Imágenes en Base64

Para imágenes locales, use codificación base64:

### Rust

```rust
let image_data = std::fs::read("photo.jpg")?;
let base64 = base64::engine::general_purpose::STANDARD.encode(&image_data);

let message = Message::user_with_content(vec![
    ContentBlock::Text("Describe this".into()),
    ContentBlock::ImageBase64 {
        data: base64,
        media_type: "image/jpeg".into(),
    },
]);
```

### Python

```python
import base64

with open("photo.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

message = Message.user_with_content([
    ContentBlock.text("Describe this"),
    ContentBlock.image_base64(image_data, "image/jpeg"),
])
```

## Cómo funciona

1. El tiempo de ejecución construye un mensaje multimodal con bloques de contenido mixtos
2. El manifiesto del protocolo mapea los bloques de contenido al formato del proveedor
3. Diferentes proveedores usan estructuras diferentes:
   - **OpenAI**: Array `content` con objetos `type: "image_url"`
   - **Anthropic**: Array `content` con objetos `type: "image"`
   - **Gemini**: Array `parts` con objetos `inline_data`
4. El protocolo maneja todas las diferencias de formato automáticamente

## Soporte por proveedor

Verifique `capabilities.vision: true` en el manifiesto del proveedor antes de enviar imágenes.

```rust
// The runtime checks capabilities before sending
// If vision is not supported, you'll get a clear error
```
