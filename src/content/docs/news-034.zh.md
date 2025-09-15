---
title: 发布 v0.3.4
group: 新闻
order: 0
status: stable
---

# ai-lib v0.3.4

亮点：

- **提供商故障转移支持**：新的 `with_failover(Vec<Provider>)` 方法支持在可重试错误时自动切换提供商
- **提供商大幅扩展**：新增 6 个 AI 提供商，包括 OpenRouter、Replicate、智谱AI、MiniMax、Perplexity 和 AI21
- **增强多模态内容**：便捷的 `Content::from_image_file()` 和 `Content::from_audio_file()` 方法，支持自动文件处理
- **新导入系统**：完整的模块树重构，提供 `prelude` 以获得更好的易用性和显式顶层导出
- **文档改进**：全面的模块树指南和更新示例，使用最新的库标准

## 新功能

### 提供商故障转移
```rust
use ai_lib::prelude::*;

let client = AiClient::new(Provider::OpenAI)?
    .with_failover(vec![Provider::Anthropic, Provider::Groq]);
```

### 多模态内容创建
```rust
use ai_lib::prelude::*;

// 从文件创建图像内容
let image_content = Content::from_image_file("path/to/image.png");

// 从文件创建音频内容
let audio_content = Content::from_audio_file("path/to/audio.mp3");

// 混合内容消息
let messages = vec![
    Message {
        role: Role::User,
        content: Content::new_text("请分析这张图片"),
        function_call: None,
    },
    Message {
        role: Role::User,
        content: image_content,
        function_call: None,
    },
];
```

### 新导入模式
```rust
// 推荐用于应用程序
use ai_lib::prelude::*;

// 显式控制
use ai_lib::{AiClient, Provider, Content, Message, Role};
```

## 新提供商

- **OpenRouter**（OpenAI 兼容）：多个 AI 模型的统一网关
- **Replicate**（OpenAI 兼容）：访问各种 AI 模型
- **智谱AI**（OpenAI 兼容）：来自中国的 GLM 系列模型
- **MiniMax**（OpenAI 兼容）：来自中国的 AI 模型
- **Perplexity**（独立）：具有自定义 API 的搜索增强 AI
- **AI21**（独立）：Jurassic 系列模型

## 破坏性变更

- **移动 `Usage` 和 `UsageStatus`**：现在在 `types::response` 模块中（`types::common` 中的弃用别名将在 1.0 之前移除）
- **`provider::utils` 模块**：现在是内部模块（`pub(crate)`）- 请使用公共 `Content` 方法代替

## 迁移指南

### Usage 和 UsageStatus
```rust
// 旧方式（已弃用）
use ai_lib::types::common::{Usage, UsageStatus};

// 新方式（推荐）
use ai_lib::{Usage, UsageStatus};
// 或者
use ai_lib::types::response::{Usage, UsageStatus};
```

### Provider Utils
```rust
// 旧方式（不再可用）
use ai_lib::provider::utils::upload_file_with_transport;

// 新方式（使用 Content 方法）
let content = Content::from_image_file("path/to/image.png");
```

## 升级

```toml
[dependencies]
ai-lib = "0.3.4"
```

## 文档

- [模块树和导入模式](https://docs.rs/ai-lib/0.3.4/ai_lib/) - 新导入系统的完整指南
- [应用引入方式](/zh/docs/import-patterns) - 不同用例的推荐模式
- [API 参考](https://docs.rs/ai-lib/0.3.4) - 完整 API 文档

## 兼容性

- **增量发布**：使用公共 API 的现有代码无破坏性变更
- **弃用时间表**：弃用项目将在 1.0 之前移除
- **迁移支持**：提供全面的迁移指南和示例
