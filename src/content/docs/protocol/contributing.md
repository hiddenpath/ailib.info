---
title: Contributing Providers
description: Step-by-step guide to adding a new AI provider to the AI-Protocol specification.
---

# Contributing a Provider

Adding a new AI provider to AI-Protocol makes it instantly available across all runtimes (Rust, Python, and any future implementations).

## Steps

> **V2-alpha format**: The protocol v0.7.0 release introduces the v2-alpha provider format with the Ring 1/2/3 manifest structure. New providers can optionally target v2-alpha for standardized error codes, feature flags, and capability extensions. See the [Protocol Overview](/protocol/overview/) for V2 architecture details.

### 1. Research the Provider API

Document the following about the provider:

- Base URL and chat endpoint path
- Authentication method (Bearer token, API key header, etc.)
- Request parameter format
- Streaming response format (SSE, NDJSON, custom)
- Error response structure
- Available models and their capabilities

### 2. Create the Provider Manifest

Create `v1/providers/<provider-id>.yaml`:

```yaml
id: <provider-id>
name: "<Provider Name>"
protocol_version: "1.5"

endpoint:
  base_url: "https://api.example.com/v1"
  chat_path: "/chat/completions"

auth:
  type: bearer
  token_env: "<PROVIDER_ID>_API_KEY"

parameter_mappings:
  temperature: "temperature"
  max_tokens: "max_tokens"
  stream: "stream"
  tools: "tools"

streaming:
  decoder:
    format: "sse"
    done_signal: "[DONE]"
  event_map:
    - match: "$.choices[0].delta.content"
      emit: "PartialContentDelta"
      extract:
        content: "$.choices[0].delta.content"

error_classification:
  by_http_status:
    "401": "authentication"
    "429": "rate_limited"
    "500": "server_error"

capabilities:
  streaming: true
  tools: true
  vision: false
```

### 3. Add Models

Create or update `v1/models/<family>.yaml`:

```yaml
models:
  example-model:
    provider: <provider-id>
    model_id: "example-model-v1"
    context_window: 128000
    capabilities: [chat, streaming, tools]
    pricing:
      input_per_token: 0.000001
      output_per_token: 0.000002
```

### 4. Validate

```bash
npm run validate
```

This checks your manifest against the JSON Schema and reports any errors.

### 5. Build

```bash
npm run build
```

This compiles your YAML to JSON in the `dist/` directory.

### 6. Submit a Pull Request

- Fork the repository
- Create a branch
- Add your provider manifest and model entries
- Ensure validation passes
- Submit a PR with documentation about the provider

## Validation Rules

The JSON Schema enforces:

- Required fields (`id`, `endpoint`, `auth`, `parameter_mappings`)
- Valid formats for URLs, environment variable names
- Correct structure for streaming configuration
- Valid error classification types
- Capability flags as booleans

## Tips

- Use the **OpenAI-compatible format** if the provider follows the OpenAI API structure — many providers do (Groq, Together AI, DeepSeek)
- Test streaming configuration carefully — this is where most provider differences exist
- Include `capabilities` flags accurately — runtimes use them for pre-flight validation
