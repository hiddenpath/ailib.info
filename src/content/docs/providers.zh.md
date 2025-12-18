---
title: 支持的提供商
group: 概述
order: 30
description: 支持的AI提供商及其功能的完整列表。
---

# 支持的提供商

ai-lib通过统一接口支持20+个AI提供商。每个提供商都通过环境变量配置，并提供一致的API访问。

## 提供商分类

### 配置驱动提供商
这些提供商使用统一的配置系统，便于设置并实现最佳性能：

| 提供商 | 聊天 | 流式 | 多模态 | 函数调用 | 备注 |
|--------|------|------|--------|----------|------|
| **Groq** | ✅ | ✅ | ❌ | ✅ | 超低延迟，Llama模型 |
| **Anthropic** | ✅ | ✅ | ✅ | ✅ | Claude 3，强推理能力 |
| **Azure OpenAI** | ✅ | ✅ | ✅ | ✅ | 企业级OpenAI，合规性 |
| **HuggingFace** | ✅ | ✅ | 变化 | 变化 | 社区模型，因模型而异 |
| **TogetherAI** | ✅ | ✅ | 变化 | 变化 | 成本效益，开源模型 |
| **DeepSeek** | ✅ | ✅ | ❌ | ✅ | 推理导向模型 |
| **Ollama** | ✅ | ✅ | 变化 | 变化 | 本地/隔离部署 |
| **xAI Grok** | ✅ | ✅ | ❌ | ✅ | 实时导向 |
| **OpenRouter** | ✅ | ✅ | 变化 | 变化 | 统一网关，支持多提供商模型路由 |
| **Replicate** | ✅ | ✅ | 变化 | 变化 | 托管开源模型网关 |

### 中文生态提供商
专门针对中文语言和企业需求：

| 提供商 | 聊天 | 流式 | 多模态 | 函数调用 | 备注 |
|--------|------|------|--------|----------|------|
| **百度文心** | ✅ | ✅ | ✅ | ✅ | 企业级中文AI |
| **腾讯混元** | ✅ | ✅ | ✅ | ✅ | 云集成 |
| **科大讯飞星火** | ✅ | ✅ | ✅ | ✅ | 语音+多模态 |
| **月之暗面Kimi** | ✅ | ✅ | ✅ | ✅ | 长上下文模型 |

### 独立适配器
这些提供商具有自定义集成逻辑，采用高性能直接HTTP客户端实现：

| 提供商 | 聊天 | 流式 | 多模态 | 函数调用 | 备注 |
|--------|------|------|--------|----------|------|
| **OpenAI** | ✅ | ✅ | ✅ | ✅ | GPT-4、GPT-3.5，广泛模型集 |
| **Google Gemini** | ✅ | ✅ | ✅ | ✅ | 原生多模态，Gemini Pro |
| **Mistral** | ✅ | ✅ | 部分 | ✅ | 欧洲模型，轻量级 |
| **Cohere** | ✅ | ✅ | 有限 | ✅ | Command模型，RAG优化 |
| **Qwen** | ✅ | ✅ | ✅ | ✅ | 阿里巴巴的多语言模型 |
| **Perplexity** | ✅ | ✅ | 有限 | ✅ | 搜索增强对话 |
| **AI21** | ✅ | ✅ | 有限 | ✅ | Jurassic 系列 |
| **智谱AI (GLM)** | ✅ | ✅ | ✅ | ✅ | 国产 GLM 系列 |
| **MiniMax** | ✅ | ✅ | ✅ | ✅ | 国产多模态 |

## 环境变量

为每个提供商配置API密钥：

```bash
# 核心提供商
export OPENAI_API_KEY=your_openai_key
export GROQ_API_KEY=your_groq_key
export ANTHROPIC_API_KEY=your_anthropic_key
export GEMINI_API_KEY=your_gemini_key

# 中文提供商
export BAIDU_API_KEY=your_baidu_key
export TENCENT_SECRET_ID=your_tencent_id
export TENCENT_SECRET_KEY=your_tencent_key
export IFlytek_APP_ID=your_iflytek_id
export IFlytek_API_KEY=your_iflytek_key
export MOONSHOT_API_KEY=your_moonshot_key

# 其他提供商
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

# Ollama（本地）
export OLLAMA_BASE_URL=http://localhost:11434
```

## 提供商选择

根据你的需求选择提供商：

```rust
use ai_lib::{AiClient, Provider};

// 速度和成本效率
let groq = AiClient::new(Provider::Groq)?;

// 推理和质量
let anthropic = AiClient::new(Provider::Anthropic)?;

// 多模态能力
let gemini = AiClient::new(Provider::Gemini)?;

// 本地/私有部署
let ollama = AiClient::new(Provider::Ollama)?;
```

## 模型管理

每个提供商提供不同能力的模型：

```rust
// 获取提供商的默认模型
let default_model = client.default_chat_model();

// 检查模型能力
let capabilities = client.model_capabilities(&model_name);

// 使用模型数组进行负载均衡
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

## 网关型提供商

网关型提供商通过统一接口提供多个AI模型的访问，简化了多提供商管理：

### OpenRouter
- **特点**：统一网关，支持20+个AI提供商
- **模型命名**：使用`provider/model`格式（如`openai/gpt-4o`、`anthropic/claude-3-5-sonnet`）
- **优势**：统一API、成本优化、模型比较
- **使用示例**：
```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};

let client = AiClient::new(Provider::OpenRouter)?;
let req = ChatCompletionRequest::new(
    "openai/gpt-4o-mini".to_string(), // 注意使用provider前缀
    vec![Message::user(Content::new_text("你好！"))]
);
```

### Replicate
- **特点**：托管开源模型平台
- **模型命名**：使用`provider/model`格式（如`meta/llama-2-7b-chat`）
- **优势**：开源模型、按需计费、易于部署
- **使用示例**：
```rust
let client = AiClient::new(Provider::Replicate)?;
let req = ChatCompletionRequest::new(
    "meta/llama-2-7b-chat".to_string(), // 使用provider前缀
    vec![Message::user(Content::new_text("解释Rust所有权"))]
);
```

### 网关使用注意事项
- **模型命名**：网关平台需要使用`provider/model`格式，而直接提供商使用原始模型名
- **API密钥**：网关通常只需要一个API密钥，无需管理多个提供商密钥
- **延迟**：网关会增加一个网络跳转，可能略微增加延迟
- **成本**：网关可能提供统一的计费和管理界面

## 提供商特定说明

### Groq
- **最适合**：速度和成本效率
- **模型**：Llama 3、Mixtral变体
- **延迟**：超低（典型<100ms）
- **限制**：无多模态支持

### Anthropic
- **最适合**：推理和复杂任务
- **模型**：Claude 3 Opus、Sonnet、Haiku
- **优势**：长上下文、工具使用、安全性
- **用例**：研究、分析、复杂推理

### OpenAI
- **最适合**：通用目的，广泛能力
- **模型**：GPT-4、GPT-3.5、DALL-E
- **优势**：多模态、函数调用、可靠性
- **用例**：通用AI应用

### Gemini
- **最适合**：多模态应用
- **模型**：Gemini Pro、Gemini Ultra
- **优势**：原生图像/音频处理
- **用例**：内容分析、多模态AI

## 提供商常量参考

本节提供了所有支持提供商的完整参考，包括枚举常量、默认模型和环境变量要求。在将ai-lib集成到应用程序时，请使用此作为快速参考。

### 提供商枚举常量

所有提供商都在`Provider`枚举中定义：

```rust
use ai_lib::Provider;

// 配置驱动提供商
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

// 中文生态提供商
Provider::BaiduWenxin
Provider::TencentHunyuan
Provider::IflytekSpark
Provider::Moonshot
Provider::ZhipuAI
Provider::MiniMax

// 独立适配器提供商
Provider::OpenAI
Provider::Qwen
Provider::Gemini
Provider::Mistral
Provider::Cohere
Provider::Perplexity
Provider::AI21
```

### 默认模型

每个提供商都有默认聊天模型和可选的多模态模型：

| 提供商 | 默认聊天模型 | 默认多模态模型 |
|--------|-------------|----------------|
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

### 环境变量

每个提供商都需要特定的环境变量进行身份验证：

| 提供商 | 环境变量 | 描述 |
|--------|---------|------|
| `Groq` | `GROQ_API_KEY` | Groq API密钥 |
| `XaiGrok` | `GROK_API_KEY` | xAI Grok API密钥 |
| `Ollama` | `OLLAMA_BASE_URL` | Ollama服务器URL（默认：`http://localhost:11434`） |
| `DeepSeek` | `DEEPSEEK_API_KEY` | DeepSeek API密钥 |
| `Anthropic` | `ANTHROPIC_API_KEY` | Anthropic API密钥 |
| `AzureOpenAI` | `AZURE_OPENAI_API_KEY`<br>`AZURE_OPENAI_ENDPOINT` | Azure OpenAI API密钥和端点 |
| `HuggingFace` | `HUGGINGFACE_API_KEY` | HuggingFace API令牌 |
| `TogetherAI` | `TOGETHER_API_KEY` | TogetherAI API密钥 |
| `OpenRouter` | `OPENROUTER_API_KEY` | OpenRouter API密钥 |
| `Replicate` | `REPLICATE_API_TOKEN` | Replicate API令牌 |
| `BaiduWenxin` | `BAIDU_WENXIN_API_KEY`<br>`BAIDU_WENXIN_SECRET_KEY` | 百度文心API凭据 |
| `TencentHunyuan` | `TENCENT_HUNYUAN_SECRET_ID`<br>`TENCENT_HUNYUAN_SECRET_KEY` | 腾讯混元凭据 |
| `IflytekSpark` | `IFLYTEK_APP_ID`<br>`IFLYTEK_API_KEY` | 科大讯飞星火凭据 |
| `Moonshot` | `MOONSHOT_API_KEY` | 月之暗面API密钥 |
| `ZhipuAI` | `ZHIPU_API_KEY` | 智谱AI API密钥 |
| `MiniMax` | `MINIMAX_API_KEY` | MiniMax API密钥 |
| `OpenAI` | `OPENAI_API_KEY` | OpenAI API密钥 |
| `Qwen` | `DASHSCOPE_API_KEY` | 阿里巴巴DashScope API密钥 |
| `Gemini` | `GEMINI_API_KEY` | Google Gemini API密钥 |
| `Mistral` | `MISTRAL_API_KEY` | Mistral API密钥 |
| `Cohere` | `COHERE_API_KEY` | Cohere API密钥 |
| `Perplexity` | `PERPLEXITY_API_KEY` | Perplexity API密钥 |
| `AI21` | `AI21_API_KEY` | AI21 API密钥 |

### 提供商功能矩阵

| 提供商 | 聊天 | 流式传输 | 多模态 | 函数调用 | 备注 |
|--------|------|----------|--------|----------|------|
| `Groq` | ✅ | ✅ | ❌ | ✅ | 超低延迟，Llama模型 |
| `XaiGrok` | ✅ | ✅ | ❌ | ✅ | 实时导向 |
| `Ollama` | ✅ | ✅ | 因模型而异 | 因模型而异 | 本地/隔离部署 |
| `DeepSeek` | ✅ | ✅ | ❌ | ✅ | 推理导向模型 |
| `Anthropic` | ✅ | ✅ | ✅ | ✅ | Claude 3，强推理能力 |
| `AzureOpenAI` | ✅ | ✅ | ✅ | ✅ | 企业级OpenAI，合规性 |
| `HuggingFace` | ✅ | ✅ | 因模型而异 | 因模型而异 | 社区模型，因模型而异 |
| `TogetherAI` | ✅ | ✅ | 因模型而异 | 因模型而异 | 成本效益，开源模型 |
| `OpenRouter` | ✅ | ✅ | 因模型而异 | 因模型而异 | OpenAI兼容网关，提供商/模型路由 |
| `Replicate` | ✅ | ✅ | 因模型而异 | 因模型而异 | 托管开源模型 |
| `BaiduWenxin` | ✅ | ✅ | ✅ | ✅ | 企业级中文AI |
| `TencentHunyuan` | ✅ | ✅ | ✅ | ✅ | 云集成 |
| `IflytekSpark` | ✅ | ✅ | ✅ | ✅ | 语音+多模态 |
| `Moonshot` | ✅ | ✅ | ✅ | ✅ | 长上下文模型 |
| `ZhipuAI` | ✅ | ✅ | ✅ | ✅ | 中文GLM系列 |
| `MiniMax` | ✅ | ✅ | ✅ | ✅ | 中文多模态 |
| `OpenAI` | ✅ | ✅ | ✅ | ✅ | GPT-4、GPT-3.5，广泛模型集 |
| `Qwen` | ✅ | ✅ | ✅ | ✅ | 阿里巴巴多语言模型 |
| `Gemini` | ✅ | ✅ | ✅ | ✅ | 原生多模态，Gemini Pro |
| `Mistral` | ✅ | ✅ | 部分 | ✅ | 欧洲模型，轻量级 |
| `Cohere` | ✅ | ✅ | 有限 | ✅ | Command模型，RAG优化 |
| `Perplexity` | ✅ | ✅ | 有限 | ✅ | 搜索增强对话 |
| `AI21` | ✅ | ✅ | 有限 | ✅ | Jurassic系列 |

## 特性标志参考

ai-lib使用Cargo特性标志来启用可选功能。在`Cargo.toml`中使用这些标志：

### 核心特性

```toml
[dependencies.ai-lib]
version = "0.4.0"
features = [
    # 启用拦截器管道（重试、速率限制器、断路器布线）
    "interceptors",
    # 启用统一的reqwest客户端工厂/共享传输设置
    "unified_transport",
    # 启用统一的SSE解析器用于流式传输
    "unified_sse",
    # 启用最小成本核算指标
    "cost_metrics",
    # 启用基于策略的路由MVP
    "routing_mvp",
    # 启用可观测性接口（Tracer、AuditSink）
    "observability",
    # 启用配置热重载traits
    "config_hot_reload",
]
```

### 便捷别名

```toml
# 启用流式传输支持（相当于"unified_sse"）
features = ["streaming"]

# 启用传输层（相当于"unified_transport"）
features = ["transport"]

# 启用弹性功能（相当于"interceptors"）
features = ["resilience"]

# 启用热重载（相当于"config_hot_reload"）
features = ["hot_reload"]

# 启用所有功能
features = ["all"]
```

### 推荐的特性组合

| 用例 | 推荐特性 |
|------|---------|
| **基础聊天** | 无（默认） |
| **流式传输** | `["streaming"]` |
| **生产应用** | `["resilience", "transport", "streaming"]` |
| **企业级** | `["resilience", "transport", "streaming", "observability"]` |
| **动态配置** | `["resilience", "transport", "streaming", "hot_reload"]` |
| **全部功能** | `["all"]` |

### 特性依赖关系

- `streaming` → 启用 `unified_sse`
- `transport` → 启用 `unified_transport`
- `resilience` → 启用 `interceptors`
- `hot_reload` → 启用 `config_hot_reload`
- `all` → 启用所有核心特性

## 下一步

- 学习[模型管理](/docs/model-management)了解高级提供商策略
- 探索[可靠性功能](/docs/reliability-overview)进行生产部署
- 查看[高级示例](/docs/advanced-examples)了解提供商特定模式
- 发现[ai-lib-pro](/docs/enterprise-pro)获取企业级提供商管理
