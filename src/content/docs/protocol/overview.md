---
title: AI-Protocol Overview
description: Understanding the AI-Protocol specification — the provider-agnostic foundation of the AI-Lib ecosystem.
---

# AI-Protocol Overview

AI-Protocol is a **provider-agnostic specification** that standardizes interactions with AI models. It separates what runtimes need to know about a provider (configuration) from how they execute requests (code).

## Core Philosophy

> **All logic is operators, all configuration is protocol.**

Every piece of provider-specific behavior — endpoints, authentication, parameter names, streaming formats, error codes — is declared in YAML configuration files. Runtime implementations contain **zero hardcoded provider logic**.

## What's in the Repository

```
ai-protocol/
├── v1/
│   ├── spec.yaml          # Core specification (v1.1)
│   ├── providers/          # 30+ provider manifests
│   │   ├── openai.yaml
│   │   ├── anthropic.yaml
│   │   ├── gemini.yaml
│   │   ├── deepseek.yaml
│   │   └── ...
│   └── models/             # Model instance registry
│       ├── gpt.yaml
│       ├── claude.yaml
│       └── ...
├── schemas/                # JSON Schema validation
│   ├── v1.json
│   └── spec.json
├── dist/                   # Pre-compiled JSON (generated)
├── scripts/                # Build & validation tools
└── examples/               # Usage examples
```

## Provider Manifests

Each provider has a YAML manifest declaring everything a runtime needs:

| Section | Purpose |
|---------|---------|
| `endpoint` | Base URL, chat path, protocol |
| `auth` | Authentication type, token env var, headers |
| `parameter_mappings` | Standard → provider-specific parameter names |
| `streaming` | Decoder format (SSE/NDJSON), event mapping rules (JSONPath) |
| `error_classification` | HTTP status → standard error types |
| `retry_policy` | Strategy, delays, retry conditions |
| `rate_limit_headers` | Header names for rate limit information |
| `capabilities` | Feature flags (streaming, tools, vision, reasoning) |

### Example: Anthropic Provider

```yaml
id: anthropic
protocol_version: "1.5"
endpoint:
  base_url: "https://api.anthropic.com/v1"
  chat_path: "/messages"
auth:
  type: bearer
  token_env: "ANTHROPIC_API_KEY"
  headers:
    anthropic-version: "2023-06-01"
parameter_mappings:
  temperature: "temperature"
  max_tokens: "max_tokens"
  stream: "stream"
  tools: "tools"
streaming:
  decoder:
    format: "anthropic_sse"
  event_map:
    - match: "$.type == 'content_block_delta'"
      emit: "PartialContentDelta"
      extract:
        content: "$.delta.text"
    - match: "$.type == 'message_stop'"
      emit: "StreamEnd"
error_classification:
  by_http_status:
    "429": "rate_limited"
    "401": "authentication"
    "529": "overloaded"
capabilities:
  streaming: true
  tools: true
  vision: true
  reasoning: true
```

## Model Registry

Models are registered with provider references, capabilities, and pricing:

```yaml
models:
  claude-3-5-sonnet:
    provider: anthropic
    model_id: "claude-3-5-sonnet-20241022"
    context_window: 200000
    capabilities: [chat, vision, tools, streaming, reasoning]
    pricing:
      input_per_token: 0.000003
      output_per_token: 0.000015
```

## Validation

All manifests are validated against JSON Schema (2020-12) using AJV. CI pipelines enforce correctness:

```bash
npm run validate    # Validate all configurations
npm run build       # Compile YAML → JSON
```

## Versioning

AI-Protocol uses layered versioning:

1. **Spec version** (`v1/spec.yaml`) — Schema structure version (currently 1.1)
2. **Protocol version** (in manifests) — Protocol features used (currently 1.5)
3. **Release version** (`package.json`) — SemVer for the specification package

## Next Steps

- **[Specification Details](/protocol/spec/)** — Core spec deep dive
- **[Provider Manifests](/protocol/providers/)** — How manifests work
- **[Model Registry](/protocol/models/)** — Model configuration
- **[Contributing Providers](/protocol/contributing/)** — Add a new provider
