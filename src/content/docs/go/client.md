---
title: AiClient (Go)
description: Reference for the Go AiClient interface.
---

# AiClient

The `AiClient` is the primary entrypoint for using `ai-lib-go`. It manages the underlying `net/http` client, manifest parsing, error mapping, and streaming pipelines.

## Instantiation

```go
aiClient, err := client.NewAiClient(ctx, providerName, options)
```

- `providerName`: The exact name of the provider manifest (e.g. `openai`, `anthropic`, `gemini`).
- `options`: Optional arguments such as custom manifest paths, HTTP client overrides, or explicit API keys (though environment variables are preferred).

## Context Integration

Unlike other runtimes, the Go SDK heavily leverages `context.Context` for resilience and lifecycle management:

```go
ctx, cancel := context.WithTimeout(context.Background(), 10 * time.Second)
defer cancel()

// If the HTTP request or stream takes longer than 10 seconds, it will automatically cancel.
stream := aiClient.Chat().Model("gpt-4o").User("List 5 colors").Stream(ctx)
```

## Supported Endpoints

Currently, the `Chat()` and `Embeddings()` builders are available. Multimodal, MCP, and Computer Use support are tracking for the `v0.1.0` release.
