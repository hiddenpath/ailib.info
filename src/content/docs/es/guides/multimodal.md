---
title: Multimodal
description: Uso de capacidades de visión y multimodales con AI-Lib.
---

# Multimodal

AI-Lib soporta entradas multimodales — texto combinado con imágenes — a través de la misma API unificada.

## Capacidades compatibles

| Capability | Direction | Providers |
|-----------|-----------|-----------|
| Vision (imágenes) | Input | OpenAI, Anthropic, Gemini, Qwen, DeepSeek |
| Generación de imágenes | Output | OpenAI (DALL-E), algunos proveedores |
| Entrada de audio | Input | Gemini, Qwen (modo omni) |
| Salida de audio | Output | Qwen (modo omni), algunos proveedores |
| Entrada de video | Input | Gemini |
| Modo Omni | Input + Output | Qwen (texto y audio al unísono) |

## Enviar imágenes

### Rust

```rust
use ai_lib_rust::{AiClient, Message, ContentBlock};

let client = AiClient::new("openai/gpt-4o").await?;

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

### TypeScript

```typescript
import { AiClient, Message, ContentBlock } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('openai/gpt-4o');

const message = Message.userWithContent([
    ContentBlock.text("What's in this image?"),
    ContentBlock.imageUrl('https://example.com/photo.jpg'),
]);

const response = await client
  .chat()
  .messages([message])
  .execute();

console.log(response.content);
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

### TypeScript

```typescript
import { readFileSync } from 'fs';

const imageBuffer = readFileSync('photo.jpg');
const imageData = imageBuffer.toString('base64');

const message = Message.userWithContent([
    ContentBlock.text('Describe this'),
    ContentBlock.imageBase64(imageData, 'image/jpeg'),
]);
```

## Capacidades Multimodales V2

El protocolo V2 proporciona el módulo `MultimodalCapabilities` para validar el contenido contra las declaraciones del proveedor antes de enviar solicitudes.

### Detección de Modales

El tiempo de ejecución detecta automáticamente los modales en los bloques de contenido:

```rust
use ai_lib_rust::multimodal::{detect_modalities, Modality};

let modalities = detect_modalities(&content_blocks);
// Devuelve: {Text, Image} o {Text, Audio, Video} etc.
```

```python
from ai_lib_python.multimodal import detect_modalities, Modality

modalities = detect_modalities(content_blocks)
# Devuelve: {Modality.TEXT, Modality.IMAGE}
```

```typescript
// TypeScript
import { detectModalities, Modality } from '@hiddenpath/ai-lib-ts/multimodal';

const modalities = detectModalities(contentBlocks);
// Devuelve: Set { Modality.TEXT, Modality.IMAGE }
```

### Validación de Formato

El tiempo de ejecución valida el formato contra lo que soporta el proveedor:

```rust
use ai_lib_rust::multimodal::MultimodalCapabilities;

let caps = MultimodalCapabilities::from_config(&manifest.multimodal);
assert!(caps.validate_image_format("png"));
assert!(caps.validate_audio_format("wav"));
```

```python
from ai_lib_python.multimodal import MultimodalCapabilities

caps = MultimodalCapabilities.from_config(manifest_multimodal)
assert caps.validate_image_format("png")
assert caps.validate_audio_format("wav")
```

```typescript
// TypeScript
import { MultimodalCapabilities } from '@hiddenpath/ai-lib-ts/multimodal';

const caps = MultimodalCapabilities.fromConfig(manifestMultimodal);
console.assert(caps.validateImageFormat('png'));
console.assert(caps.validateAudioFormat('wav'));
```

### Validación de Contenido

Valida que el proveedor soporte todos los modales en el contenido antes de enviar la solicitud:

```rust
use ai_lib_rust::multimodal::validate_content_modalities;

match validate_content_modalities(&blocks, &caps) {
    Ok(()) => { /* todos los modales son soportados */ }
    Err(unsupported) => {
        eprintln!("El proveedor no soporta: {:?}", unsupported);
    }
}
```

```python
from ai_lib_python.multimodal import validate_content_modalities

# Validar bloques de contenido contra las capacidades del proveedor
```

```typescript
// TypeScript
import { validateContentModalities } from '@hiddenpath/ai-lib-ts/multimodal';

try {
  validateContentModalities(blocks, caps);
  // todos los modales son soportados
} catch (unsupported) {
  console.error(`El proveedor no soporta: ${unsupported}`);
}
```

## Cómo funciona

1. El tiempo de ejecución construye un mensaje multimodal con bloques de contenido mixtos
2. **Validación V2**: `MultimodalCapabilities` comprueba que todos los modales de contenido sean soportados por el proveedor
3. El manifiesto del protocolo mapea los bloques de contenido al formato del proveedor
4. Diferentes proveedores usan estructuras diferentes:
   - **OpenAI**: Array `content` con objetos `type: "image_url"`
   - **Anthropic**: Array `content` con objetos `type: "image"`
   - **Gemini**: Array `parts` con objetos `inline_data` (soporta `parts` de video)
5. El protocolo maneja todas las diferencias de formato automáticamente

## Matriz de Soporte Multimodal por Proveedor

El manifiesto V2 declara explícitamente las características multimodales para cada proveedor:

| Proveedor | Image In | Audio In | Video In | Image Out | Audio Out | Omni |
|----------|---------|---------|---------|----------|----------|------|
| OpenAI | ✅ png, jpg, gif, webp | — | — | ✅ | — | — |
| Anthropic | ✅ png, jpg, gif, webp | — | — | — | — | — |
| Gemini | ✅ png, jpg, gif, webp | ✅ wav, mp3, flac | ✅ mp4, avi | — | — | — |
| Qwen | ✅ png, jpg | ✅ wav, mp3 | — | — | ✅ | ✅ |
| DeepSeek | ✅ png, jpg | — | — | — | — | — |

Por favor, revise las secciones `multimodal.input` y `multimodal.output` en los manifiestos de los proveedores V2 para la declaración completa.
