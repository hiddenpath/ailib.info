---
title: Multimodal
description: Using vision, audio, video, and omni-mode multimodal capabilities with AI-Lib.
---

# Multimodal

AI-Lib supports multimodal inputs and outputs — text combined with images, audio, and video — through the same unified API. The V2 protocol provides comprehensive multimodal capabilities with format validation and provider-aware modality checking.

## Supported Capabilities

| Capability | Direction | Providers |
|-----------|-----------|-----------|
| Vision (images) | Input | OpenAI, Anthropic, Gemini, Qwen, DeepSeek |
| Image generation | Output | OpenAI (DALL-E), select providers |
| Audio input | Input | Gemini, Qwen (omni_mode) |
| Audio output | Output | Qwen (omni_mode), select providers |
| Video input | Input | Gemini |
| Omni mode | Input + Output | Qwen (simultaneous text + audio) |

## Sending Images

### Rust

```rust
use ai_lib::{AiClient, Message, ContentBlock};

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

## V2 Multimodal Capabilities

The V2 protocol provides a `MultimodalCapabilities` module that validates content against provider declarations before sending requests.

### Modality Detection

The runtime automatically detects modalities in your content blocks:

```rust
use ai_lib::multimodal::{detect_modalities, Modality};

let modalities = detect_modalities(&content_blocks);
// Returns: {Text, Image} or {Text, Audio, Video} etc.
```

```python
from ai_lib_python.multimodal import detect_modalities, Modality

modalities = detect_modalities(content_blocks)
# Returns: {Modality.TEXT, Modality.IMAGE}
```

### Format Validation

The runtime validates formats against what the provider supports:

```rust
use ai_lib::multimodal::MultimodalCapabilities;

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

### Content Validation

Before sending a request, validate that the provider supports all modalities in the content:

```rust
use ai_lib::multimodal::validate_content_modalities;

match validate_content_modalities(&blocks, &caps) {
    Ok(()) => { /* all modalities supported */ }
    Err(unsupported) => {
        eprintln!("Provider doesn't support: {:?}", unsupported);
    }
}
```

## How It Works

1. The runtime constructs a multimodal message with mixed content blocks
2. **V2 validation**: `MultimodalCapabilities` checks that all content modalities are supported by the provider
3. The protocol manifest maps content blocks to the provider's format
4. Different providers use different structures:
   - **OpenAI**: `content` array with `type: "image_url"` objects
   - **Anthropic**: `content` array with `type: "image"` objects
   - **Gemini**: `parts` array with `inline_data` objects (supports video `parts`)
5. The protocol handles all format differences automatically

## Provider Multimodal Matrix

The V2 manifest declares each provider's multimodal capabilities explicitly:

| Provider | Image In | Audio In | Video In | Image Out | Audio Out | Omni |
|----------|---------|---------|---------|----------|----------|------|
| OpenAI | ✅ png, jpg, gif, webp | — | — | ✅ | — | — |
| Anthropic | ✅ png, jpg, gif, webp | — | — | — | — | — |
| Gemini | ✅ png, jpg, gif, webp | ✅ wav, mp3, flac | ✅ mp4, avi | — | — | — |
| Qwen | ✅ png, jpg | ✅ wav, mp3 | — | — | ✅ | ✅ |
| DeepSeek | ✅ png, jpg | — | — | — | — | — |

Check `multimodal.input` and `multimodal.output` sections in the V2 provider manifest for the complete declaration.
