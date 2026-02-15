---
title: Provider Manifests
description: How AI-Protocol provider manifests work — endpoint configuration, auth, parameter mapping, streaming, and error handling.
---

# Provider Manifests

Each AI provider in the ecosystem has a YAML manifest file (`v1/providers/<provider>.yaml`) that fully describes how to interact with its API.

## Supported Providers

Provider manifests are available in two formats: **v1** (legacy) and **v2-alpha**. The v2-alpha format uses the Ring 1/2/3 concentric structure (Core Skeleton → Capability Mapping → Advanced Extensions). **OpenAI, Anthropic, and Gemini** are available in both v1 and v2-alpha formats.

### Global Providers

OpenAI, Anthropic, Google Gemini, Groq, Mistral, Cohere, Perplexity, Together AI, DeepInfra, OpenRouter, Azure OpenAI, NVIDIA, Fireworks AI, Replicate, AI21 Labs, Cerebras, Lepton AI, Grok

### China Region Providers

DeepSeek, Qwen (Alibaba), Zhipu GLM, Doubao (ByteDance), Baidu ERNIE, iFlytek Spark, Tencent Hunyuan, SenseNova, Tiangong, Moonshot (Kimi), MiniMax, Baichuan, Yi (01.AI), SiliconFlow

## Manifest Structure

### Endpoint Configuration

```yaml
endpoint:
  base_url: "https://api.openai.com/v1"
  chat_path: "/chat/completions"
  protocol: "https"
  timeout_ms: 60000
```

### Authentication

Supports multiple auth types:

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

### Parameter Mappings

Maps standard parameter names to provider-specific fields:

```yaml
parameter_mappings:
  temperature: "temperature"
  max_tokens: "max_completion_tokens"  # OpenAI uses different name
  stream: "stream"
  tools: "tools"
  tool_choice: "tool_choice"
  response_format: "response_format"
```

### Streaming Configuration

Declares how to decode and interpret streaming responses:

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

### Error Classification

Maps HTTP responses to standard error types:

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

### Capabilities

Feature flags that runtimes check before making requests:

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

## How Runtimes Use Manifests

1. **Load** — Read YAML manifest (local, env var, or GitHub)
2. **Validate** — Check against JSON Schema
3. **Compile** — Convert user request using parameter mappings
4. **Execute** — Send HTTP request with correct auth/headers
5. **Decode** — Process response using streaming configuration
6. **Classify** — Handle errors using classification rules

## Next Steps

- **[Model Registry](/protocol/models/)** — How models are configured
- **[Contributing Providers](/protocol/contributing/)** — Add a new provider
