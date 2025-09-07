---
title: Supported Providers
group: Overview
order: 30
description: Complete list of supported AI providers and their capabilities.
---

# Supported Providers

ai-lib supports 17+ AI providers through a unified interface. Each provider is configured via environment variables and offers consistent API access.

## Provider Categories

### Config-Driven Providers
These providers use a unified configuration system for easy setup and optimal performance:

| Provider | Chat | Streaming | Multimodal | Function Calls | Notes |
|----------|------|-----------|------------|----------------|-------|
| **Groq** | ✅ | ✅ | ❌ | ✅ | Ultra-low latency, Llama models |
| **Anthropic** | ✅ | ✅ | ✅ | ✅ | Claude 3, strong reasoning |
| **Azure OpenAI** | ✅ | ✅ | ✅ | ✅ | Enterprise OpenAI with compliance |
| **HuggingFace** | ✅ | ✅ | Varies | Varies | Community models, varies by model |
| **TogetherAI** | ✅ | ✅ | Varies | Varies | Cost-efficient, open models |
| **DeepSeek** | ✅ | ✅ | ❌ | ✅ | Reasoning-focused models |
| **Ollama** | ✅ | ✅ | Varies | Varies | Local/airgapped deployment |
| **xAI Grok** | ✅ | ✅ | ❌ | ✅ | Real-time oriented |

### Chinese Ecosystem Providers
Specialized for Chinese language and enterprise needs:

| Provider | Chat | Streaming | Multimodal | Function Calls | Notes |
|----------|------|-----------|------------|----------------|-------|
| **Baidu Wenxin** | ✅ | ✅ | ✅ | ✅ | Enterprise Chinese AI |
| **Tencent Hunyuan** | ✅ | ✅ | ✅ | ✅ | Cloud integration |
| **iFlytek Spark** | ✅ | ✅ | ✅ | ✅ | Voice + multimodal |
| **Moonshot Kimi** | ✅ | ✅ | ✅ | ✅ | Long context models |

### Independent Adapters
These providers have custom integration logic with high-performance direct HTTP client implementation:

| Provider | Chat | Streaming | Multimodal | Function Calls | Notes |
|----------|------|-----------|------------|----------------|-------|
| **OpenAI** | ✅ | ✅ | ✅ | ✅ | GPT-4, GPT-3.5, broad model set |
| **Google Gemini** | ✅ | ✅ | ✅ | ✅ | Native multimodal, Gemini Pro |
| **Mistral** | ✅ | ✅ | Partial | ✅ | European models, lightweight |
| **Cohere** | ✅ | ✅ | Limited | ✅ | Command models, RAG optimized |
| **Qwen** | ✅ | ✅ | ✅ | ✅ | Alibaba's multilingual models |

## Environment Variables

Configure API keys for each provider:

```bash
# Core providers
export OPENAI_API_KEY=your_openai_key
export GROQ_API_KEY=your_groq_key
export ANTHROPIC_API_KEY=your_anthropic_key
export GEMINI_API_KEY=your_gemini_key

# Chinese providers
export BAIDU_API_KEY=your_baidu_key
export TENCENT_SECRET_ID=your_tencent_id
export TENCENT_SECRET_KEY=your_tencent_key
export IFlytek_APP_ID=your_iflytek_id
export IFlytek_API_KEY=your_iflytek_key
export MOONSHOT_API_KEY=your_moonshot_key

# Other providers
export MISTRAL_API_KEY=your_mistral_key
export COHERE_API_KEY=your_cohere_key
export HUGGINGFACE_API_KEY=your_hf_key
export TOGETHERAI_API_KEY=your_together_key
export DEEPSEEK_API_KEY=your_deepseek_key
export QWEN_API_KEY=your_qwen_key
export XAI_API_KEY=your_xai_key

# Ollama (local)
export OLLAMA_BASE_URL=http://localhost:11434
```

## Provider Selection

Choose providers based on your needs:

```rust
use ai_lib::{AiClient, Provider};

// For speed and cost efficiency
let groq = AiClient::new(Provider::Groq)?;

// For reasoning and quality
let anthropic = AiClient::new(Provider::Anthropic)?;

// For multimodal capabilities
let gemini = AiClient::new(Provider::Gemini)?;

// For local/private deployment
let ollama = AiClient::new(Provider::Ollama)?;
```

## Model Management

Each provider offers different models with varying capabilities:

```rust
// Get default model for provider
let default_model = client.default_chat_model();

// Check model capabilities
let capabilities = client.model_capabilities(&model_name);

// Use model arrays for load balancing
use ai_lib::{ModelArray, LoadBalancingStrategy};

let array = ModelArray::new("production")
    .with_strategy(LoadBalancingStrategy::HealthBased)
    .add_endpoint(ModelEndpoint {
        name: "groq-1".into(),
        url: "https://api.groq.com".into(),
        weight: 1.0,
        healthy: true,
    });
```

## Provider-Specific Notes

### Groq
- **Best for**: Speed and cost efficiency
- **Models**: Llama 3, Mixtral variants
- **Latency**: Ultra-low (sub-100ms typical)
- **Limitations**: No multimodal support

### Anthropic
- **Best for**: Reasoning and complex tasks
- **Models**: Claude 3 Opus, Sonnet, Haiku
- **Strengths**: Long context, tool use, safety
- **Use cases**: Research, analysis, complex reasoning

### OpenAI
- **Best for**: General purpose, broad capabilities
- **Models**: GPT-4, GPT-3.5, DALL-E
- **Strengths**: Multimodal, function calling, reliability
- **Use cases**: General AI applications

### Gemini
- **Best for**: Multimodal applications
- **Models**: Gemini Pro, Gemini Ultra
- **Strengths**: Native image/audio processing
- **Use cases**: Content analysis, multimodal AI

## Next Steps

- Learn about [Model Management](/docs/model-management) for advanced provider strategies
- Explore [Reliability Features](/docs/reliability-overview) for production deployments
- Check [Advanced Examples](/docs/advanced-examples) for provider-specific patterns
