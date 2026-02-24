---
title: マルチモーダル
description: AI-Lib でビジョンとマルチモーダル機能を使用する方法です。
---

# マルチモーダル

AI-Lib は、同じ統一 API でテキストと画像を組み合わせたマルチモーダル入力に対応しています。

## 対応機能

| Capability | Direction | Providers |
|-----------|-----------|-----------|
| Vision (images) | Input | OpenAI, Anthropic, Gemini, Qwen, DeepSeek |
| Image generation | Output | OpenAI (DALL-E), 一部のプロバイダー |
| Audio input | Input | Gemini, Qwen (omni_mode) |
| Audio output | Output | Qwen (omni_mode), 一部のプロバイダー |
| Video input | Input | Gemini |
| Omni mode | Input + Output | Qwen (テキスト＋音声同期表示) |

## 画像の送信

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

## Base64 画像

ローカル画像の場合は Base64 エンコーディングを使用してください：

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

## V2 マルチモーダル機能

V2 プロトコルは、リクエストを送信する前にプロバイダーの宣言に対してコンテンツを検証する `MultimodalCapabilities` モジュールを提供します。

### モダリティ検出

ランタイムはコンテンツブロック内のモダリティを自動的に検出します：

```rust
use ai_lib_rust::multimodal::{detect_modalities, Modality};

let modalities = detect_modalities(&content_blocks);
// Returns: {Text, Image} or {Text, Audio, Video} etc.
```

```python
from ai_lib_python.multimodal import detect_modalities, Modality

modalities = detect_modalities(content_blocks)
# Returns: {Modality.TEXT, Modality.IMAGE}
```

```typescript
// TypeScript
import { detectModalities, Modality } from '@hiddenpath/ai-lib-ts/multimodal';

const modalities = detectModalities(contentBlocks);
// Returns: Set { Modality.TEXT, Modality.IMAGE }
```

### フォーマット検証

ランタイムは、プロバイダーがサポートしているものに対してフォーマットを検証します：

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

### コンテンツ検証

リクエストを送信する前に、プロバイダーがコンテンツ内のすべてのモダリティをサポートしていることを検証します：

```rust
use ai_lib_rust::multimodal::validate_content_modalities;

match validate_content_modalities(&blocks, &caps) {
    Ok(()) => { /* all modalities supported */ }
    Err(unsupported) => {
        eprintln!("Provider doesn't support: {:?}", unsupported);
    }
}
```

```python
from ai_lib_python.multimodal import validate_content_modalities

# Validate content blocks against provider capabilities
```

```typescript
// TypeScript
import { validateContentModalities } from '@hiddenpath/ai-lib-ts/multimodal';

try {
  validateContentModalities(blocks, caps);
  // all modalities supported
} catch (unsupported) {
  console.error(`Provider doesn't support: ${unsupported}`);
}
```

## 仕組み

1. ランタイムが混合コンテンツブロックを含むマルチモーダルメッセージを構築します
2. **V2 検証**: `MultimodalCapabilities` は、すべてのコンテンツモダリティがプロバイダーでサポートされていることを確認します
3. プロトコルマニフェストがコンテンツブロックをプロバイダーのフォーマットにマッピングします
4. プロバイダーによって異なる構造を使用します：
   - **OpenAI**: `type: "image_url"` オブジェクトを含む `content` 配列
   - **Anthropic**: `type: "image"` オブジェクトを含む `content` 配列
   - **Gemini**: `inline_data` オブジェクトを含む `parts` 配列（動画の `parts` に対応）
5. プロトコルがすべてのフォーマットの違いを自動的に処理します

## プロバイダーのマルチモーダル対応マトリックス

V2 マニフェストは、各プロバイダーのマルチモーダル機能を明示的に宣言しています：

| Provider | Image In | Audio In | Video In | Image Out | Audio Out | Omni |
|----------|---------|---------|---------|----------|----------|------|
| OpenAI | ✅ png, jpg, gif, webp | — | — | ✅ | — | — |
| Anthropic | ✅ png, jpg, gif, webp | — | — | — | — | — |
| Gemini | ✅ png, jpg, gif, webp | ✅ wav, mp3, flac | ✅ mp4, avi | — | — | — |
| Qwen | ✅ png, jpg | ✅ wav, mp3 | — | — | ✅ | ✅ |
| DeepSeek | ✅ png, jpg | — | — | — | — | — |

完全な宣言については、V2 プロバイダーマニフェストの `multimodal.input` と `multimodal.output` セクションを確認してください。
