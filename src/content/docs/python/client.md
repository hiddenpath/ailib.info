---
title: AiClient API (Python)
description: Detailed guide to using AiClient, ChatRequestBuilder, and response types in ai-lib-python.
---

# AiClient API

## Creating a Client

### From Model Identifier

```python
from ai_lib_python import AiClient

client = await AiClient.create("anthropic/claude-3-5-sonnet")
```

### With Builder

```python
client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .protocol_dir("./ai-protocol") \
    .timeout(60) \
    .build()
```

### With Resilience

```python
from ai_lib_python.resilience import ResilientConfig

config = ResilientConfig(
    max_retries=3,
    rate_limit_rps=10,
    circuit_breaker_threshold=5,
    max_inflight=50,
)

client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .resilience(config) \
    .build()
```

## ChatRequestBuilder

Fluent API for building requests:

```python
response = await client.chat() \
    .system("You are a helpful assistant") \
    .user("Hello!") \
    .messages([Message.user("Follow-up")]) \
    .temperature(0.7) \
    .max_tokens(1000) \
    .top_p(0.9) \
    .tools([tool_definition]) \
    .execute()
```

## Response Types

### ChatResponse

```python
class ChatResponse:
    content: str              # Response text
    tool_calls: list[ToolCall]  # Function calls
    finish_reason: str        # Completion reason
    usage: Usage              # Token counts
```

### StreamingEvent

```python
class StreamingEvent:
    # Type checks
    is_content_delta: bool
    is_tool_call_started: bool
    is_partial_tool_call: bool
    is_stream_end: bool

    # Type-safe accessors
    as_content_delta -> ContentDelta
    as_tool_call_started -> ToolCallStarted
    as_partial_tool_call -> PartialToolCall
    as_stream_end -> StreamEnd
```

### CallStats

```python
class CallStats:
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    model: str
    provider: str
```

## Execution Modes

### Non-Streaming

```python
# Simple response
response = await client.chat().user("Hello").execute()

# With statistics
response, stats = await client.chat().user("Hello").execute_with_stats()
```

### Streaming

```python
async for event in client.chat().user("Hello").stream():
    if event.is_content_delta:
        print(event.as_content_delta.text, end="")
```

### Cancellable Stream

```python
from ai_lib_python import CancelToken

token = CancelToken()

async for event in client.chat().user("Long task...").stream(cancel_token=token):
    if event.is_content_delta:
        print(event.as_content_delta.text, end="")
    if should_cancel:
        token.cancel()
        break
```

## Error Handling

```python
from ai_lib_python.errors import (
    AiLibError, ProtocolError, TransportError, RemoteError
)

try:
    response = await client.chat().user("Hello").execute()
except RemoteError as e:
    print(f"Provider error: {e.error_type}")  # Standard error class
    print(f"HTTP status: {e.status_code}")
except TransportError as e:
    print(f"Network error: {e}")
except ProtocolError as e:
    print(f"Protocol error: {e}")
except AiLibError as e:
    print(f"Other error: {e}")
```

## Next Steps

- **[Streaming Pipeline](/docs/python/streaming/)** — Pipeline internals
- **[Resilience](/docs/python/resilience/)** — Reliability patterns
- **[Advanced Features](/docs/python/advanced/)** — Telemetry, routing, plugins
