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
│   ├── providers/            # 36 V1 provider manifests
│   │   ├── openai.yaml
│   │   ├── anthropic.yaml
│   │   └── ...
│   └── models/               # Model instance registry
├── v2/
│   └── providers/            # 6 V2 provider manifests
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

1. **Spec version** (`v1/spec.yaml`) — Schema structure version (currently v0.7.0)
2. **Protocol version** (in manifests) — Protocol features used (currently 0.7)
3. **Release version** (`package.json`) — SemVer for the specification package (v0.7.0)

## V2 Protocol Architecture

Protocol v0.7.0 delivers the full **V2 architecture** — a complete separation of concerns across layers, a concentric manifest model, and three new capability modules.

### Three-Layer Pyramid

- **L1 Core Protocol** — Message format, standard error codes (E1001–E9999), version declaration. All providers must implement this layer.
- **L2 Capability Extensions** — Streaming, vision, tools, MCP, Computer Use, multimodal. Each extension is controlled by feature flags; providers opt in per capability.
- **L3 Environment Profile** — API keys, endpoints, retry policies. Environment-specific configuration that can be overridden without changing provider logic.

### Concentric Circle Manifest Model

- **Ring 1 Core Skeleton** (required) — Minimal fields for a valid manifest: endpoint, auth, parameter mappings, model list
- **Ring 2 Capability Mapping** (conditional) — Streaming config, tools mapping, MCP integration, Computer Use actions — present when the provider supports them
- **Ring 3 Advanced Extensions** (optional) — Custom headers, rate limit headers, context management policies, advanced retry

### V2 Providers

Six providers are available in **V2 format**, each with full Ring 1/2/3 structure and MCP/CU/Multimodal declarations:

| Provider | API Style | MCP | Computer Use | Multimodal |
|----------|-----------|-----|-------------|------------|
| OpenAI | `OpenAiCompatible` | ✅ (tool_parameter) | ✅ (screen_based) | Vision, Audio |
| Anthropic | `AnthropicMessages` | ✅ (sdk_config) | ✅ (screen_based) | Vision |
| Gemini | `GeminiGenerate` | ✅ (sdk_config) | ✅ (tool_based) | Vision, Audio, Video |
| DeepSeek | `OpenAiCompatible` | — | — | Vision |
| Moonshot | `OpenAiCompatible` | — | — | Vision |
| Zhipu | `OpenAiCompatible` | — | — | Vision |

V2 manifests are fully backward compatible — V1 manifests continue to work and can be auto-promoted via `CapabilitiesV2.from_legacy()`.

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

A **compliance test suite** with 230+ tests ensures identical behavior across Rust and Python runtimes. The V2 integration tests validate the full chain: Manifest parsing → ProviderDriver selection → Capability Registry → MCP bridge → Computer Use safety → Multimodal validation.

## Next Steps

- **[Specification Details](/protocol/spec/)** — Core spec deep dive
- **[Provider Manifests](/protocol/providers/)** — How manifests work
- **[Model Registry](/protocol/models/)** — Model configuration
- **[Contributing Providers](/protocol/contributing/)** — Add a new provider
