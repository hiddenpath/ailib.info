---
title: Specification Details
description: Deep dive into the AI-Protocol core specification — standard parameters, events, error classes, and retry policies.
---

# Core Specification

The core specification (`v1/spec.yaml`) defines the standard vocabulary that all provider manifests and runtimes share.

## Standard Parameters

These parameters have consistent meaning across all providers:

| Parameter | Type | Description |
|-----------|------|-------------|
| `temperature` | float | Randomness control (0.0 – 2.0) |
| `max_tokens` | integer | Maximum response tokens |
| `top_p` | float | Nucleus sampling threshold |
| `stream` | boolean | Enable streaming response |
| `stop` | string[] | Stop sequences |
| `tools` | object[] | Tool/function definitions |
| `tool_choice` | string/object | Tool selection mode |
| `response_format` | object | Structured output format |

Provider manifests map these standard names to provider-specific parameter names. For example, OpenAI uses `max_completion_tokens` while Anthropic uses `max_tokens`.

## Streaming Events

The specification defines unified streaming event types that runtimes emit:

| Event | Description |
|-------|-------------|
| `PartialContentDelta` | Text content fragment |
| `ThinkingDelta` | Reasoning/thinking block (extended thinking models) |
| `ToolCallStarted` | Function/tool invocation begins |
| `PartialToolCall` | Tool call argument streaming |
| `ToolCallEnded` | Tool invocation complete |
| `StreamEnd` | Response stream complete |
| `StreamError` | Stream-level error |
| `Metadata` | Usage statistics, model info |

Provider manifests declare JSONPath-based rules that map provider-specific events to these standard types.

## Error Classes (V2 Standard Codes)

V2 defines 13 standardized error codes. Provider-specific errors are mapped to these codes for consistent handling across runtimes:

| Code | Name | Category | Retryable | Fallbackable |
|------|------|----------|-----------|--------------|
| E1001 | `invalid_request` | Client | No | No |
| E1002 | `authentication` | Client | No | No |
| E1003 | `permission_denied` | Client | No | No |
| E1004 | `not_found` | Client | No | No |
| E1005 | `request_too_large` | Client | No | Yes |
| E2001 | `rate_limited` | Rate | Yes | Yes |
| E2002 | `quota_exhausted` | Quota | No | Yes |
| E3001 | `server_error` | Server | Yes | Yes |
| E3002 | `overloaded` | Server | Yes | Yes |
| E3003 | `timeout` | Server | Yes | Yes |
| E4001 | `conflict` | Conflict | No | No |
| E4002 | `cancelled` | Conflict | No | No |
| E9999 | `unknown` | Unknown | No | Yes |

- **Retryable** — Runtimes may retry the request (with backoff) for transient failures
- **Fallbackable** — Runtimes may try an alternative provider or model in a fallback chain

## Retry Policies

The spec defines standard retry strategies:

```yaml
retry_policy:
  strategy: "exponential_backoff"
  max_retries: 3
  initial_delay_ms: 1000
  max_delay_ms: 30000
  backoff_multiplier: 2.0
  retryable_errors:
    - "rate_limited"
    - "overloaded"
    - "server_error"
    - "timeout"
```

## Termination Reasons

Normalized finish reasons for response completion:

| Reason | Description |
|--------|-------------|
| `end_turn` | Natural completion |
| `max_tokens` | Token limit reached |
| `tool_use` | Model wants to call a tool |
| `stop_sequence` | Stop sequence encountered |
| `content_filter` | Filtered by content policy |

## API Families

Providers are categorized into API families to prevent request/response format confusion:

- `openai` — OpenAI-compatible APIs (also used by Groq, Together, DeepSeek, etc.)
- `anthropic` — Anthropic Messages API
- `gemini` — Google Gemini API
- `custom` — Provider-specific format

## Next Steps

- **[Provider Manifests](/protocol/providers/)** — How provider configs work
- **[Model Registry](/protocol/models/)** — Model configuration details
