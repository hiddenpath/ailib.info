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
| **OpenRouter** | ✅ | ✅ | 变化 | 变化 | OpenAI 兼容网关，provider/model 路由 |
| **Replicate** | ✅ | ✅ | 变化 | 变化 | 托管开源模型 |

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

## 下一步

- 学习[模型管理](/docs/model-management)了解高级提供商策略
- 探索[可靠性功能](/docs/reliability-overview)进行生产部署
- 查看[高级示例](/docs/advanced-examples)了解提供商特定模式
