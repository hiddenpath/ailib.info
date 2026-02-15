---
title: 供应商清单
description: AI-Protocol 供应商清单工作原理 —— 端点配置、认证、参数映射、流式与错误处理。
---

# 供应商清单

生态系统中每个 AI 供应商都有一个 YAML 清单文件（`v1/providers/<provider>.yaml`），完整描述如何与其 API 交互。

## 支持的供应商

供应商清单提供两种格式：**v1**（旧版）和 **v2-alpha**。v2-alpha 格式使用 Ring 1/2/3 同心结构（核心骨架 → 能力映射 → 高级扩展）。**OpenAI、Anthropic 和 Gemini** 同时提供 v1 和 v2-alpha 格式。

### 全球供应商

OpenAI、Anthropic、Google Gemini、Groq、Mistral、Cohere、Perplexity、Together AI、DeepInfra、OpenRouter、Azure OpenAI、NVIDIA、Fireworks AI、Replicate、AI21 Labs、Cerebras、Lepton AI、Grok

### 中国区供应商

DeepSeek、Qwen（阿里巴巴）、智谱 GLM、豆包（字节跳动）、百度文心一言、讯飞星火、腾讯混元、SenseNova、天工、月之暗面（Kimi）、MiniMax、百川、Yi（01.AI）、SiliconFlow

## 清单结构

### 端点配置

```yaml
endpoint:
  base_url: "https://api.openai.com/v1"
  chat_path: "/chat/completions"
  protocol: "https"
  timeout_ms: 60000
```

### 认证

支持多种认证类型：

```yaml
# Bearer token (most common)
auth:
  type: bearer
  token_env: "OPENAI_API_KEY"

# API key in header
auth:
  type: api_key
  header: "x-api-key"
  token_env: "ANTHROPIC_API_KEY"

# Custom headers
auth:
  type: bearer
  token_env: "ANTHROPIC_API_KEY"
  headers:
    anthropic-version: "2023-06-01"
```

### 参数映射

将标准参数名映射到供应商特定字段：

```yaml
parameter_mappings:
  temperature: "temperature"
  max_tokens: "max_completion_tokens"  # OpenAI uses different name
  stream: "stream"
  tools: "tools"
  tool_choice: "tool_choice"
  response_format: "response_format"
```

### 流式配置

声明如何解码和解释流式响应：

```yaml
streaming:
  decoder:
    format: "sse"              # "sse", "ndjson", or "anthropic_sse"
    done_signal: "[DONE]"      # Stream termination marker
  event_map:
    - match: "$.choices[0].delta.content"
      emit: "PartialContentDelta"
      extract:
        content: "$.choices[0].delta.content"
    - match: "$.choices[0].delta.tool_calls"
      emit: "PartialToolCall"
      extract:
        tool_calls: "$.choices[0].delta.tool_calls"
    - match: "$.choices[0].finish_reason"
      emit: "StreamEnd"
      extract:
        finish_reason: "$.choices[0].finish_reason"
```

### 错误分类

将 HTTP 响应映射到标准错误类型：

```yaml
error_classification:
  by_http_status:
    "400": "invalid_request"
    "401": "authentication"
    "403": "permission"
    "404": "not_found"
    "429": "rate_limited"
    "500": "server_error"
    "503": "overloaded"
  by_error_code:
    "context_length_exceeded": "context_length"
    "content_filter": "content_filter"
```

### 能力

运行时在发起请求前检查的特性标志：

```yaml
capabilities:
  streaming: true
  tools: true
  vision: true
  audio: false
  reasoning: true
  agentic: true
  json_mode: true
```

## 运行时如何使用清单

1. **加载** — 读取 YAML 清单（本地、环境变量或 GitHub）
2. **验证** — 对照 JSON Schema 检查
3. **编译** — 使用参数映射转换用户请求
4. **执行** — 使用正确认证/头部发送 HTTP 请求
5. **解码** — 使用流式配置处理响应
6. **分类** — 使用分类规则处理错误

## 下一步

- **[模型注册表](/protocol/models/)** — 模型配置方式
- **[贡献供应商](/protocol/contributing/)** — 添加新供应商
