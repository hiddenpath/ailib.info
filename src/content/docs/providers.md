---
title: Supported Providers
group: Overview
order: 30
description: Complete list of supported AI providers and their capabilities.
---

# Supported Providers

ai-lib supports 20+ AI providers through a unified interface. Each provider is configured via environment variables and offers consistent API access. For enterprise environments requiring advanced provider management, routing, and analytics, see [ai-lib-pro](/docs/enterprise-pro).

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
| **OpenRouter** | ✅ | ✅ | Varies | Varies | OpenAI-compatible gateway, provider/model routing |
| **Replicate** | ✅ | ✅ | Varies | Varies | Hosted open-source models |

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
| **Perplexity** | ✅ | ✅ | Limited | ✅ | Search-augmented conversations |
| **AI21** | ✅ | ✅ | Limited | ✅ | Jurassic series |
| **ZhipuAI (GLM)** | ✅ | ✅ | ✅ | ✅ | Chinese GLM series |
| **MiniMax** | ✅ | ✅ | ✅ | ✅ | Chinese multimodal |

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
export OPENROUTER_API_KEY=your_openrouter_key
export REPLICATE_API_TOKEN=your_replicate_token
export PERPLEXITY_API_KEY=your_perplexity_key
export AI21_API_KEY=your_ai21_key
export ZHIPU_API_KEY=your_zhipu_key
export MINIMAX_API_KEY=your_minimax_key

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

// Use model arrays for load balancing (requires routing_mvp feature)
#[cfg(feature = "routing_mvp")]
{
    use ai_lib::{ModelArray, LoadBalancingStrategy};

    let array = ModelArray::new("production")
        .with_strategy(LoadBalancingStrategy::HealthBased)
        .add_endpoint(ModelEndpoint {
            name: "groq-1".into(),
            url: "https://api.groq.com".into(),
            weight: 1.0,
            healthy: true,
        });
}
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

## Enterprise Provider Management

For production environments with multiple providers, consider ai-lib-pro's advanced features:

- **Advanced Routing**: Intelligent load balancing across providers
- **Health Monitoring**: Real-time provider health and performance tracking
- **Cost Optimization**: Provider cost analysis and automatic cost-based routing
- **Failover Management**: Automatic failover with configurable policies
- **Usage Analytics**: Detailed provider usage patterns and optimization insights

## Provider Constants Reference

This section provides a complete reference of all supported providers, their enum constants, default models, and environment variable requirements. Use this as a quick reference when integrating ai-lib into your applications.

### Provider Enum Constants

All providers are defined in the `Provider` enum:

```rust
use ai_lib::Provider;

// Config-driven providers
Provider::Groq
Provider::XaiGrok
Provider::Ollama
Provider::DeepSeek
Provider::Anthropic
Provider::AzureOpenAI
Provider::HuggingFace
Provider::TogetherAI
Provider::OpenRouter
Provider::Replicate

// Chinese ecosystem providers
Provider::BaiduWenxin
Provider::TencentHunyuan
Provider::IflytekSpark
Provider::Moonshot
Provider::ZhipuAI
Provider::MiniMax

// Independent adapter providers
Provider::OpenAI
Provider::Qwen
Provider::Gemini
Provider::Mistral
Provider::Cohere
Provider::Perplexity
Provider::AI21
```

### Default Models

Each provider has a default chat model and optional multimodal model:

| Provider | Default Chat Model | Default Multimodal Model |
|----------|-------------------|-------------------------|
| `Groq` | `llama-3.1-8b-instant` | - |
| `XaiGrok` | `grok-beta` | - |
| `Ollama` | `llama3-8b` | - |
| `DeepSeek` | `deepseek-chat` | - |
| `Anthropic` | `claude-3-5-sonnet-20241022` | `claude-3-5-sonnet-20241022` |
| `AzureOpenAI` | `gpt-35-turbo` | `gpt-4o` |
| `HuggingFace` | `microsoft/DialoGPT-medium` | - |
| `TogetherAI` | `meta-llama/Llama-3-8b-chat-hf` | - |
| `OpenRouter` | `openai/gpt-3.5-turbo` | `openai/gpt-4o` |
| `Replicate` | `meta/llama-2-7b-chat` | `meta/llama-2-7b-chat` |
| `BaiduWenxin` | `ernie-3.5` | - |
| `TencentHunyuan` | `hunyuan-standard` | - |
| `IflytekSpark` | `spark-v3.0` | - |
| `Moonshot` | `moonshot-v1-8k` | - |
| `ZhipuAI` | `glm-4` | `glm-4v` |
| `MiniMax` | `abab6.5-chat` | `abab6.5-chat` |
| `OpenAI` | `gpt-3.5-turbo` | `gpt-4o` |
| `Qwen` | `qwen-turbo` | - |
| `Gemini` | `gemini-1.5-flash` | `gemini-1.5-flash` |
| `Mistral` | `mistral-small` | - |
| `Cohere` | `command-r` | `command-r-plus` |
| `Perplexity` | `llama-3.1-sonar-small-128k-online` | `llama-3.1-sonar-small-128k-online` |
| `AI21` | `j2-ultra` | `j2-ultra` |

### Environment Variables

Each provider requires specific environment variables for authentication:

| Provider | Environment Variable | Description |
|----------|---------------------|-------------|
| `Groq` | `GROQ_API_KEY` | Groq API key |
| `XaiGrok` | `GROK_API_KEY` | xAI Grok API key |
| `Ollama` | `OLLAMA_BASE_URL` | Ollama server URL (default: `http://localhost:11434`) |
| `DeepSeek` | `DEEPSEEK_API_KEY` | DeepSeek API key |
| `Anthropic` | `ANTHROPIC_API_KEY` | Anthropic API key |
| `AzureOpenAI` | `AZURE_OPENAI_API_KEY`<br>`AZURE_OPENAI_ENDPOINT` | Azure OpenAI API key and endpoint |
| `HuggingFace` | `HUGGINGFACE_API_KEY` | HuggingFace API token |
| `TogetherAI` | `TOGETHER_API_KEY` | TogetherAI API key |
| `OpenRouter` | `OPENROUTER_API_KEY` | OpenRouter API key |
| `Replicate` | `REPLICATE_API_TOKEN` | Replicate API token |
| `BaiduWenxin` | `BAIDU_WENXIN_API_KEY`<br>`BAIDU_WENXIN_SECRET_KEY` | Baidu Wenxin API credentials |
| `TencentHunyuan` | `TENCENT_HUNYUAN_SECRET_ID`<br>`TENCENT_HUNYUAN_SECRET_KEY` | Tencent Hunyuan credentials |
| `IflytekSpark` | `IFLYTEK_APP_ID`<br>`IFLYTEK_API_KEY` | iFlytek Spark credentials |
| `Moonshot` | `MOONSHOT_API_KEY` | Moonshot API key |
| `ZhipuAI` | `ZHIPU_API_KEY` | ZhipuAI API key |
| `MiniMax` | `MINIMAX_API_KEY` | MiniMax API key |
| `OpenAI` | `OPENAI_API_KEY` | OpenAI API key |
| `Qwen` | `DASHSCOPE_API_KEY` | Alibaba DashScope API key |
| `Gemini` | `GEMINI_API_KEY` | Google Gemini API key |
| `Mistral` | `MISTRAL_API_KEY` | Mistral API key |
| `Cohere` | `COHERE_API_KEY` | Cohere API key |
| `Perplexity` | `PERPLEXITY_API_KEY` | Perplexity API key |
| `AI21` | `AI21_API_KEY` | AI21 API key |

### Provider Capabilities Matrix

| Provider | Chat | Streaming | Multimodal | Function Calling | Notes |
|----------|------|-----------|------------|------------------|-------|
| `Groq` | ✅ | ✅ | ❌ | ✅ | Ultra-low latency, Llama models |
| `XaiGrok` | ✅ | ✅ | ❌ | ✅ | Real-time oriented |
| `Ollama` | ✅ | ✅ | Varies | Varies | Local/airgapped deployment |
| `DeepSeek` | ✅ | ✅ | ❌ | ✅ | Reasoning-focused models |
| `Anthropic` | ✅ | ✅ | ✅ | ✅ | Claude 3, strong reasoning |
| `AzureOpenAI` | ✅ | ✅ | ✅ | ✅ | Enterprise OpenAI with compliance |
| `HuggingFace` | ✅ | ✅ | Varies | Varies | Community models, varies by model |
| `TogetherAI` | ✅ | ✅ | Varies | Varies | Cost-efficient, open models |
| `OpenRouter` | ✅ | ✅ | Varies | Varies | OpenAI-compatible gateway, provider/model routing |
| `Replicate` | ✅ | ✅ | Varies | Varies | Hosted open-source models |
| `BaiduWenxin` | ✅ | ✅ | ✅ | ✅ | Enterprise Chinese AI |
| `TencentHunyuan` | ✅ | ✅ | ✅ | ✅ | Cloud integration |
| `IflytekSpark` | ✅ | ✅ | ✅ | ✅ | Voice + multimodal |
| `Moonshot` | ✅ | ✅ | ✅ | ✅ | Long context models |
| `ZhipuAI` | ✅ | ✅ | ✅ | ✅ | Chinese GLM series |
| `MiniMax` | ✅ | ✅ | ✅ | ✅ | Chinese multimodal |
| `OpenAI` | ✅ | ✅ | ✅ | ✅ | GPT-4, GPT-3.5, broad model set |
| `Qwen` | ✅ | ✅ | ✅ | ✅ | Alibaba's multilingual models |
| `Gemini` | ✅ | ✅ | ✅ | ✅ | Native multimodal, Gemini Pro |
| `Mistral` | ✅ | ✅ | Partial | ✅ | European models, lightweight |
| `Cohere` | ✅ | ✅ | Limited | ✅ | Command models, RAG optimized |
| `Perplexity` | ✅ | ✅ | Limited | ✅ | Search-augmented conversations |
| `AI21` | ✅ | ✅ | Limited | ✅ | Jurassic series |

## Feature Flags Reference

ai-lib uses Cargo feature flags to enable optional functionality. Use these flags in your `Cargo.toml`:

### Core Features

```toml
[dependencies.ai-lib]
version = "0.4.0"
features = [
    # Enable interceptor pipeline (retry, rate limiters, circuit breaker)
    "interceptors",
    # Enable unified reqwest client factory/shared transport settings
    "unified_transport",
    # Enable unified SSE parser for streaming
    "unified_sse",
    # Enable minimal cost accounting metrics
    "cost_metrics",
    # Enable strategy-based routing MVP
    "routing_mvp",
    # Enable observability interfaces (Tracer, AuditSink)
    "observability",
    # Enable config hot-reload traits
    "config_hot_reload",
]
```

### Convenience Aliases

```toml
# Enable streaming support (equivalent to "unified_sse")
features = ["streaming"]

# Enable transport layer (equivalent to "unified_transport")
features = ["transport"]

# Enable resilience features (equivalent to "interceptors")
features = ["resilience"]

# Enable hot reload (equivalent to "config_hot_reload")
features = ["hot_reload"]

# Enable all features
features = ["all"]
```

### Recommended Feature Combinations

| Use Case | Recommended Features |
|----------|---------------------|
| **Basic Chat** | None (default) |
| **Streaming** | `["streaming"]` |
| **Production App** | `["resilience", "transport", "streaming"]` |
| **Enterprise** | `["resilience", "transport", "streaming", "observability"]` |
| **Dynamic Config** | `["resilience", "transport", "streaming", "hot_reload"]` |
| **Everything** | `["all"]` |

### Feature Dependencies

- `streaming` → enables `unified_sse`
- `transport` → enables `unified_transport`
- `resilience` → enables `interceptors`
- `hot_reload` → enables `config_hot_reload`
- `all` → enables all core features

## Next Steps

- Learn about [Model Management](/docs/model-management) for advanced provider strategies
- Explore [Reliability Features](/docs/reliability-overview) for production deployments
- Check [Advanced Examples](/docs/advanced-examples) for provider-specific patterns
- Discover [ai-lib-pro](/docs/enterprise-pro) for enterprise-grade provider management
