---
title: Streaming Pipeline (Python)
description: How the streaming pipeline works in ai-lib-python — decoders, selectors, accumulators, and event mappers.
---

# Streaming Pipeline

The Python SDK implements the same operator-based pipeline architecture as the Rust runtime, adapted for Python's async ecosystem.

## Pipeline Stages

```
Raw Bytes → Decoder → Selector → Accumulator → FanOut → EventMapper → StreamingEvent
```

### 1. Decoder

Converts HTTP response bytes to JSON frames:

| Decoder Class | Provider Format |
|--------------|----------------|
| `SseDecoder` | Standard SSE (OpenAI, Groq, etc.) |
| `JsonLinesDecoder` | Newline-delimited JSON |
| `AnthropicSseDecoder` | Anthropic's custom SSE |

The decoder is selected based on the manifest's `streaming.decoder.format`.

### 2. Selector

Filters JSON frames using JSONPath expressions from the manifest:

```python
# Internally, the pipeline creates selectors from manifest rules:
# match: "$.choices[0].delta.content" → emit: "PartialContentDelta"
```

Uses `jsonpath-ng` for JSONPath expression evaluation.

### 3. Accumulator

Assembles partial tool calls into complete invocations:

```python
# Provider streams:
#   {"tool_calls": [{"index": 0, "function": {"arguments": '{"ci'}}]}
#   {"tool_calls": [{"index": 0, "function": {"arguments": 'ty":"T'}}]}
#   {"tool_calls": [{"index": 0, "function": {"arguments": 'okyo"}'}}]}
# Accumulator produces complete: {"city": "Tokyo"}
```

### 4. FanOut

For multi-candidate responses (`n > 1`), expands into per-candidate streams.

### 5. EventMapper

Three mapper implementations:

| Mapper | Description |
|--------|-------------|
| `ProtocolEventMapper` | Uses manifest's event_map rules (JSONPath → event type) |
| `DefaultEventMapper` | Fallback for OpenAI-compatible providers |
| `AnthropicEventMapper` | Handles Anthropic's unique event structure |

## Async Iteration

The pipeline exposes events as an async iterator:

```python
async for event in client.chat().user("Hello").stream():
    if event.is_content_delta:
        text = event.as_content_delta.text
        print(text, end="")
    elif event.is_tool_call_started:
        call = event.as_tool_call_started
        print(f"\nTool: {call.name}")
    elif event.is_stream_end:
        end = event.as_stream_end
        print(f"\nFinish: {end.finish_reason}")
```

## Cancellation

Streams support graceful cancellation:

```python
from ai_lib_python import CancelToken

token = CancelToken()

async for event in client.chat().user("...").stream(cancel_token=token):
    # Cancel after receiving enough content
    if total_chars > 1000:
        token.cancel()
        break
```

## Next Steps

- **[Resilience](/docs/python/resilience/)** — Reliability patterns
- **[Advanced Features](/docs/python/advanced/)** — Telemetry, routing, plugins
