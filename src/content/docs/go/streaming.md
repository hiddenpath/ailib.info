---
title: Streaming Pipeline (Go)
description: Deep dive into the operator-based streaming pipeline in ai-lib-go v0.5.0.
---

# Streaming Pipeline

The streaming pipeline is the core of ai-lib-go. It processes provider responses through composable operators, each driven by protocol configuration.

## Pipeline Architecture

```
Raw Bytes → Decoder → Selector → Accumulator → FanOut → EventMapper → StreamingEvent
```

Each operator is a stage in the pipeline:

### 1. Decoder

Converts raw byte streams into JSON frames.

| Format          | Description                             |
| --------------- | --------------------------------------- |
| `sse`           | Server-Sent Events (OpenAI, Groq, etc.) |
| `ndjson`        | Newline-delimited JSON                  |
| `anthropic_sse` | Anthropic's custom SSE format           |

The decoder format is specified in the provider manifest:

```yaml
streaming:
  decoder:
    format: 'sse'
    done_signal: '[DONE]'
```

### 2. Selector

Filters JSON frames using JSONPath expressions defined in the manifest's `event_map`:

```yaml
event_map:
  - match: '$.choices[0].delta.content'
    emit: 'PartialContentDelta'
```

### 3. Accumulator

Statefully assembles partial tool calls. When a provider streams tool call arguments in chunks, the accumulator collects them into complete tool calls:

```
PartialToolCall("get_we") → PartialToolCall("ather") → PartialToolCall("(\"Tokyo\")")
```

### 4. FanOut

Handles multi-candidate responses (when `n > 1`). Expands candidates into separate event streams.

### 5. EventMapper

The final stage — converts processed frames into unified `StreamingEvent` types.

## Protocol-Driven Construction

The pipeline is built automatically from the provider manifest. No manual configuration needed:

```go
// The pipeline is constructed internally based on the protocol manifest
stream, err := aiClient.Chat().
    User("Hello").
    ExecuteStream(ctx)
if err != nil {
    panic(err)
}
defer stream.Close()

for stream.Next() {
    event := stream.Event()
    // Process event
}
```

The runtime reads the `streaming` section of the manifest and wires up the appropriate decoder, selector rules, and event mapper.

## Retry and Fallback Operators

The pipeline also includes resilience operators:

- **Retry** — Retries failed streams based on the manifest's retry policy
- **Fallback** — Falls back to alternative providers/models on failure

## Next Steps

- **[Resilience](/go/resilience/)** — Circuit breaker, rate limiter
- **[Advanced Features](/go/advanced/)** — Embeddings, cache, batch
