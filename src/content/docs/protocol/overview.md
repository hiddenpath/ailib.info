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
│   ├── spec.yaml          # Core specification (v0.5.0)
│   ├── providers/          # 35+ provider manifests
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
protocol_version: "0.5"
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

1. **Spec version** (`v1/spec.yaml`) — Schema structure version (currently v0.5.0)
2. **Protocol version** (in manifests) — Protocol features used (currently 0.5)
3. **Release version** (`package.json`) — SemVer for the specification package (v0.5.0)

## V2 Protocol Architecture

Protocol v0.5.0 introduces the **V2 architecture** — a clean separation of concerns across layers and a concentric manifest model.

### Three-Layer Pyramid

- **L1 Core Protocol** — Message format, standard error codes (E1001–E9999), version declaration. All providers must implement this layer.
- **L2 Capability Extensions** — Streaming, vision, tools. Each extension is controlled by feature flags; providers opt in per capability.
- **L3 Environment Profile** — API keys, endpoints, retry policies. Environment-specific configuration that can be overridden without changing provider logic.

### Concentric Circle Manifest Model

- **Ring 1 Core Skeleton** (required) — Minimal fields for a valid manifest: endpoint, auth, parameter mappings
- **Ring 2 Capability Mapping** (conditional) — Streaming config, tools mapping, vision params — present when the provider supports them
- **Ring 3 Advanced Extensions** (optional) — Custom headers, rate limit headers, advanced retry policies

### V2-Alpha Providers

OpenAI, Anthropic, and Gemini are already available in **v2-alpha** format. These manifests use the Ring 1/2/3 structure and can be used alongside v1 manifests.

### Standard Error Codes

V2 defines 13 standardized error codes (E1001–E9999) across 5 categories: client errors (E1xxx), rate/quota (E2xxx), server (E3xxx), conflict/cancel (E4xxx), and unknown (E9999). See the [specification](/protocol/spec/) for the full code list.

### Cross-Runtime Consistency

A **compliance test suite** ensures identical behavior across Rust and Python runtimes. All V2 providers pass the same test matrix in both implementations.

## Next Steps

- **[Specification Details](/protocol/spec/)** — Core spec deep dive
- **[Provider Manifests](/protocol/providers/)** — How manifests work
- **[Model Registry](/protocol/models/)** — Model configuration
- **[Contributing Providers](/protocol/contributing/)** — Add a new provider
