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
│   ├── spec.yaml            # V1 core specification
│   ├── providers/            # V1 provider manifests
│   │   ├── openai.yaml
│   │   ├── anthropic.yaml
│   │   └── ...
│   └── models/               # Model instance registry
├── v2/
│   └── providers/            # V2 provider manifests (P0 generative set)
│       ├── openai.yaml       # Ring 1/2/3 + MCP/CU/MM declarations
│       ├── anthropic.yaml
│       ├── gemini.yaml
│       ├── deepseek.yaml
│       ├── moonshot.yaml
│       └── zhipu.yaml
├── v2-alpha/
│   └── spec.yaml             # V2 specification (3 layers + 3 modules)
├── schemas/
│   ├── v1.json               # V1 schema
│   ├── v2/
│   │   ├── provider.json     # V2 provider manifest schema
│   │   ├── provider-contract.json  # ProviderContract schema
│   │   ├── mcp.json          # MCP integration schema
│   │   ├── computer-use.json # Computer Use schema
│   │   ├── multimodal.json   # Extended multimodal schema
│   │   └── context-policy.json # Context management schema
│   └── spec.json
├── docs/
│   ├── V2_ARCHITECTURE.md    # V2 architecture document (v1.0)
│   └── V2_MIGRATION_GUIDE.md # V1 → V2 migration guide
├── dist/                     # Pre-compiled JSON (generated)
├── scripts/                  # Build & validation tools
└── work/                     # Working documents & research
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
protocol_version: "0.7"
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

1. **Spec version** (`v1/spec.yaml`) — Schema structure version.
2. **Protocol version** (in manifests) — Protocol features used by each manifest (`1.x` / `2.x`).
3. **Release version** (`package.json`) — SemVer for the specification package (current: **v0.8.1**).

## V2 Protocol Architecture

Protocol evolution through **v0.8.1** delivers the full **V2 architecture** plus execution governance gates for release readiness.

### Three-Layer Pyramid

- **L1 Core Protocol** — Message format, standard error codes (E1001–E9999), version declaration. All providers must implement this layer.
- **L2 Capability Extensions** — Streaming, vision, tools, MCP, Computer Use, multimodal. Each extension is controlled by feature flags; providers opt in per capability.
- **L3 Environment Profile** — API keys, endpoints, retry policies. Environment-specific configuration that can be overridden without changing provider logic.

### Concentric Circle Manifest Model

- **Ring 1 Core Skeleton** (required) — Minimal fields for a valid manifest: endpoint, auth, parameter mappings, model list
- **Ring 2 Capability Mapping** (conditional) — Streaming config, tools mapping, MCP integration, Computer Use actions — present when the provider supports them
- **Ring 3 Advanced Extensions** (optional) — Custom headers, rate limit headers, context management policies, advanced retry

### V2 Providers

The P0 generative provider set is available in **V2 manifests**, with Ring 1/2/3 structure and multimodal declarations:

| Provider | API Style | Multimodal Focus |
|----------|-----------|------------------|
| OpenAI | `OpenAiCompatible` | text/vision/audio |
| Anthropic | `AnthropicMessages` | text/vision |
| Google Gemini | `GeminiGenerate` | text/vision/audio/video-in |
| DeepSeek | `OpenAiCompatible` | text/vision |
| Qwen | `OpenAiCompatible` | text/vision/audio-in |
| Doubao | `OpenAiCompatible` | text/vision |

V2 manifests remain backward-compatible with V1 loading paths in runtimes, while governance gates ensure staged release safety.

### ProviderContract

V2 introduces the **ProviderContract** schema — a formal declaration of each provider's API characteristics:

- **API Style** — `OpenAiCompatible`, `AnthropicMessages`, `GeminiGenerate`, or `Custom`
- **Capability Matrix** — Which capabilities the provider supports and their configuration
- **Action Mapping** — How standard actions map to provider-specific API calls
- **Degradation Strategy** — Fallback behavior when capabilities are unavailable

### V2 Schema Suite

Six JSON schemas validate the V2 protocol:

| Schema | Purpose |
|--------|---------|
| `provider.json` | V2 provider manifest structure |
| `provider-contract.json` | ProviderContract capability declaration |
| `mcp.json` | MCP client/server/transport configuration |
| `computer-use.json` | Computer Use actions, safety, provider mapping |
| `multimodal.json` | Input/output modalities, formats, omni-mode |
| `context-policy.json` | Context window management strategies |

### Standard Error Codes

V2 defines 13 standardized error codes (E1001–E9999) across 5 categories: client errors (E1xxx), rate/quota (E2xxx), server (E3xxx), conflict/cancel (E4xxx), and unknown (E9999). See the [specification](/protocol/spec/) for the full code list.

### CLI Tool

The `ai-protocol-cli` Rust binary provides developer utilities for working with manifests:

```bash
ai-protocol-cli validate <path>        # Validate all manifests (53/53 passing)
ai-protocol-cli info <provider>         # Show provider capabilities and config
ai-protocol-cli list                    # List all 37 providers with versions
ai-protocol-cli check-compat <manifest> # Check runtime feature compatibility
```

### Cross-Runtime Consistency

A cross-runtime **compliance suite** now validates Rust, Python, and TypeScript runtimes across protocol loading, error classification, retry decisions, message building, stream decoding, event mapping, and tool accumulation.

## Execution Governance

Release execution is guarded by script-based gates:

- `npm run drift:check`
- `npm run gate:manifest-consumption`
- `npm run gate:compliance-matrix`
- `npm run gate:fullchain`
- `npm run release:gate`

Each gate supports `--report-only` mode for advisory rollout before strict blocking enforcement.

## Next Steps

- **[Specification Details](/protocol/spec/)** — Core spec deep dive
- **[Provider Manifests](/protocol/providers/)** — How manifests work
- **[Model Registry](/protocol/models/)** — Model configuration
- **[Contributing Providers](/protocol/contributing/)** — Add a new provider
