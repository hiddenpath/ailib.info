---
title: Release v0.3.4
group: News
order: 0
status: stable
---

# ai-lib v0.3.4

Highlights:

- **Provider Failover Support**: New `with_failover(Vec<Provider>)` method enables automatic provider switching on retryable errors
- **Major Provider Expansion**: Added 6 new AI providers including OpenRouter, Replicate, ZhipuAI, MiniMax, Perplexity, and AI21
- **Enhanced Multimodal Content**: Convenient `Content::from_image_file()` and `Content::from_audio_file()` methods for automatic file processing
- **New Import System**: Complete module tree restructuring with `prelude` for better ergonomics and explicit top-level exports
- **Documentation Improvements**: Comprehensive module tree guide and updated examples using latest library standards

## New Features

### Provider Failover
```rust
use ai_lib::prelude::*;

let client = AiClient::new(Provider::OpenAI)?
    .with_failover(vec![Provider::Anthropic, Provider::Groq]);
```

### Multimodal Content Creation
```rust
use ai_lib::prelude::*;

// Image content from file
let image_content = Content::from_image_file("path/to/image.png");

// Audio content from file
let audio_content = Content::from_audio_file("path/to/audio.mp3");

// Mixed content message
let messages = vec![
    Message {
        role: Role::User,
        content: Content::new_text("Analyze this image"),
        function_call: None,
    },
    Message {
        role: Role::User,
        content: image_content,
        function_call: None,
    },
];
```

### New Import Patterns
```rust
// Recommended for applications
use ai_lib::prelude::*;

// Explicit control
use ai_lib::{AiClient, Provider, Content, Message, Role};
```

## New Providers

- **OpenRouter** (OpenAI-compatible): Unified gateway for multiple AI models
- **Replicate** (OpenAI-compatible): Access to various AI models
- **ZhipuAI** (OpenAI-compatible): GLM series models from China
- **MiniMax** (OpenAI-compatible): AI models from China
- **Perplexity** (Independent): Search-enhanced AI with custom API
- **AI21** (Independent): Jurassic series models

## Breaking Changes

- **Moved `Usage` and `UsageStatus`**: Now in `types::response` module (deprecated aliases in `types::common` will be removed before 1.0)
- **`provider::utils` module**: Now internal (`pub(crate)`) - use public `Content` methods instead

## Migration Guide

### Usage and UsageStatus
```rust
// Old (deprecated)
use ai_lib::types::common::{Usage, UsageStatus};

// New (recommended)
use ai_lib::{Usage, UsageStatus};
// or
use ai_lib::types::response::{Usage, UsageStatus};
```

### Provider Utils
```rust
// Old (no longer available)
use ai_lib::provider::utils::upload_file_with_transport;

// New (use Content methods)
let content = Content::from_image_file("path/to/image.png");
```

## Upgrade

```toml
[dependencies]
ai-lib = "0.3.4"
```

## Documentation

- [Module Tree and Import Patterns](https://docs.rs/ai-lib/0.3.4/ai_lib/) - Complete guide to the new import system
- [Application Import Patterns](/docs/import-patterns) - Recommended patterns for different use cases
- [API Reference](https://docs.rs/ai-lib/0.3.4) - Complete API documentation

## Compatibility

- **Additive release**: No breaking changes for existing code using public APIs
- **Deprecation timeline**: Deprecated items will be removed before 1.0
- **Migration support**: Comprehensive migration guide and examples provided


