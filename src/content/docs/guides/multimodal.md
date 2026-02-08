---
title: Multimodal
description: Using vision and multimodal capabilities with AI-Lib.
---

# Multimodal

AI-Lib supports multimodal inputs — text combined with images — through the same unified API.

## Supported Capabilities

| Capability | Providers |
|-----------|-----------|
| Vision (images) | OpenAI, Anthropic, Gemini, Qwen |
| Audio input | Limited (Gemini) |

## Sending Images

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

## Base64 Images

For local images, use base64 encoding:

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

## How It Works

1. The runtime constructs a multimodal message with mixed content blocks
2. The protocol manifest maps content blocks to the provider's format
3. Different providers use different structures:
   - **OpenAI**: `content` array with `type: "image_url"` objects
   - **Anthropic**: `content` array with `type: "image"` objects
   - **Gemini**: `parts` array with `inline_data` objects
4. The protocol handles all format differences automatically

## Provider Support

Check `capabilities.vision: true` in the provider manifest before sending images.

```rust
// The runtime checks capabilities before sending
// If vision is not supported, you'll get a clear error
```
