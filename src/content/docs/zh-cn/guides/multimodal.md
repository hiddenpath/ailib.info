---
title: 多模态
description: 使用 AI-Lib 的视觉与多模态能力。
---

# 多模态

AI-Lib 支持多模态输入 — 文本与图像组合 — 通过相同的统一 API。

## 支持的能力

| Capability | Direction | Providers |
|-----------|-----------|-----------|
| Vision（图像） | Input | OpenAI, Anthropic, Gemini, Qwen, DeepSeek |
| Image generation | Output | OpenAI (DALL-E), 部分提供商 |
| Audio input | Input | Gemini, Qwen (omni_mode) |
| Audio output | Output | Qwen (omni_mode), 部分提供商 |
| Video input | Input | Gemini |
| Omni mode | Input + Output | Qwen (文本+音频同步) |

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

## V2 多模态能力

V2 协议提供了 `MultimodalCapabilities` 模块，在发送请求前根据提供商声明验证内容。

### 模态检测

运行时自动检测内容块中的模态：

```rust
use ai_lib_rust::multimodal::{detect_modalities, Modality};

let modalities = detect_modalities(&content_blocks);
// 返回: {Text, Image} 或 {Text, Audio, Video} 等
```

```python
from ai_lib_python.multimodal import detect_modalities, Modality

modalities = detect_modalities(content_blocks)
# 返回: {Modality.TEXT, Modality.IMAGE}
```

```typescript
// TypeScript
import { detectModalities, Modality } from '@hiddenpath/ai-lib-ts/multimodal';

const modalities = detectModalities(contentBlocks);
// 返回: Set { Modality.TEXT, Modality.IMAGE }
```

### 格式验证

运行时根据提供商的支持验证格式：

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

### 内容验证

发送请求前，验证提供商是否支持内容中的所有模态：

```rust
use ai_lib_rust::multimodal::validate_content_modalities;

match validate_content_modalities(&blocks, &caps) {
    Ok(()) => { /* 所有模态均支持 */ }
    Err(unsupported) => {
        eprintln!("提供商不支持: {:?}", unsupported);
    }
}
```

```python
from ai_lib_python.multimodal import validate_content_modalities

# 根据提供商能力验证内容块
```

```typescript
// TypeScript
import { validateContentModalities } from '@hiddenpath/ai-lib-ts/multimodal';

try {
  validateContentModalities(blocks, caps);
  // 所有模态均支持
} catch (unsupported) {
  console.error(`提供商不支持: ${unsupported}`);
}
```

## 工作原理

1. 运行时构建包含混合内容块的多模态消息
2. **V2 验证**：`MultimodalCapabilities` 检查提供商是否支持所有内容的模态
3. 协议清单将内容块映射到提供商格式
4. 不同提供商使用不同结构：
   - **OpenAI**：带 `type: "image_url"` 对象的 `content` 数组
   - **Anthropic**：带 `type: "image"` 对象的 `content` 数组
   - **Gemini**：带 `inline_data` 对象的 `parts` 数组（支持视频 `parts`）
5. 协议自动处理所有格式差异

## 提供商多模态支持矩阵

V2 清单在配置中显式声明了每个提供商的多模态功能：

| Provider | Image In | Audio In | Video In | Image Out | Audio Out | Omni |
|----------|---------|---------|---------|----------|----------|------|
| OpenAI | ✅ png, jpg, gif, webp | — | — | ✅ | — | — |
| Anthropic | ✅ png, jpg, gif, webp | — | — | — | — | — |
| Gemini | ✅ png, jpg, gif, webp | ✅ wav, mp3, flac | ✅ mp4, avi | — | — | — |
| Qwen | ✅ png, jpg | ✅ wav, mp3 | — | — | ✅ | ✅ |
| DeepSeek | ✅ png, jpg | — | — | — | — | — |

请查看 V2 提供商清单中的 `multimodal.input` 和 `multimodal.output` 部分获取完整声明。
