---
title: 多模态
description: 使用 AI-Lib 的视觉与多模态能力。
---

# 多模态

AI-Lib 支持多模态输入 — 文本与图像组合 — 通过相同的统一 API。

## 支持的能力

| Capability | Providers |
|-----------|-----------|
| Vision（图像） | OpenAI, Anthropic, Gemini, Qwen |
| Audio input | 有限（Gemini） |

## 发送图像

### Rust

```rust
use ai_lib_rust::{AiClient, Message, ContentBlock};

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

## Base64 图像

对于本地图像，使用 base64 编码：

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

## 工作原理

1. 运行时构建包含混合内容块的多模态消息
2. 协议清单将内容块映射到提供商格式
3. 不同提供商使用不同结构：
   - **OpenAI**：带 `type: "image_url"` 对象的 `content` 数组
   - **Anthropic**：带 `type: "image"` 对象的 `content` 数组
   - **Gemini**：带 `inline_data` 对象的 `parts` 数组
4. 协议自动处理所有格式差异

## 提供商支持

发送图像前请在提供商清单中检查 `capabilities.vision: true`。

```rust
// The runtime checks capabilities before sending
// If vision is not supported, you'll get a clear error
```
