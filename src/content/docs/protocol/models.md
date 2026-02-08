---
title: Model Registry
description: How AI-Protocol's model registry maps model identifiers to provider configurations with capabilities and pricing.
---

# Model Registry

The model registry (`v1/models/*.yaml`) maps model identifiers to provider configurations, recording capabilities, context windows, and pricing for each model.

## Model File Structure

Models are organized by family (GPT, Claude, Gemini, etc.):

```
v1/models/
├── gpt.yaml          # OpenAI GPT models
├── claude.yaml        # Anthropic Claude models
├── gemini.yaml        # Google Gemini models
├── deepseek.yaml      # DeepSeek models
├── qwen.yaml          # Alibaba Qwen models
├── mistral.yaml       # Mistral models
├── llama.yaml         # Meta Llama models
└── ...                # 28+ model files
```

## Model Definition

Each model entry includes:

```yaml
models:
  gpt-4o:
    provider: openai
    model_id: "gpt-4o"
    context_window: 128000
    max_output_tokens: 16384
    capabilities:
      - chat
      - streaming
      - tools
      - vision
      - json_mode
    pricing:
      input_per_token: 0.0000025
      output_per_token: 0.00001
    release_date: "2024-05-13"
```

## Model Identifiers

Runtimes use a `provider/model` format to identify models:

```
anthropic/claude-3-5-sonnet
openai/gpt-4o
deepseek/deepseek-chat
gemini/gemini-2.0-flash
qwen/qwen-plus
```

The runtime splits this into:
1. **Provider ID** (`anthropic`) → loads provider manifest
2. **Model name** (`claude-3-5-sonnet`) → looks up in model registry

## Capabilities

Standard capability flags:

| Capability | Description |
|-----------|-------------|
| `chat` | Basic chat completions |
| `streaming` | Streaming responses |
| `tools` | Function/tool calling |
| `vision` | Image understanding |
| `audio` | Audio input/output |
| `reasoning` | Extended thinking (CoT) |
| `agentic` | Multi-step agent workflows |
| `json_mode` | Structured JSON output |

## Pricing

Per-token pricing enables cost estimation in runtimes:

```yaml
pricing:
  input_per_token: 0.000003      # $3 per 1M input tokens
  output_per_token: 0.000015     # $15 per 1M output tokens
  cached_input_per_token: 0.0000003  # Cached prompt discount
```

Both Rust and Python runtimes use this data for `CostEstimate` calculations.

## Verification

Models can include verification status for production deployments:

```yaml
verification:
  status: "verified"
  last_checked: "2025-01-15"
  verified_capabilities:
    - chat
    - streaming
    - tools
```

## Next Steps

- **[Contributing Providers](/docs/protocol/contributing/)** — Add new providers and models
- **[Quick Start](/docs/quickstart/)** — Start using models with the runtimes
