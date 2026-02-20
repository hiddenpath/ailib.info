---
title: マルチモーダル
description: AI-Lib でビジョンとマルチモーダル機能を使用する方法です。
---

# マルチモーダル

AI-Lib は、同じ統一 API でテキストと画像を組み合わせたマルチモーダル入力に対応しています。

## 対応機能

| Capability | Providers |
|-----------|-----------|
| Vision (images) | OpenAI, Anthropic, Gemini, Qwen |
| Audio input | Limited (Gemini) |

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

## 仕組み

1. ランタイムが混合コンテンツブロックを含むマルチモーダルメッセージを構築します
2. プロトコルマニフェストがコンテンツブロックをプロバイダーのフォーマットにマッピングします
3. プロバイダーによって異なる構造を使用します：
   - **OpenAI**: `type: "image_url"` オブジェクトを含む `content` 配列
   - **Anthropic**: `type: "image"` オブジェクトを含む `content` 配列
   - **Gemini**: `inline_data` オブジェクトを含む `parts` 配列
4. プロトコルがすべてのフォーマットの違いを自動的に処理します

## プロバイダー対応

画像を送信する前に、プロバイダーマニフェストで `capabilities.vision: true` を確認してください。

```rust
// The runtime checks capabilities before sending
// If vision is not supported, you'll get a clear error
```
