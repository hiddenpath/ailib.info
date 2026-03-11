---
title: TypeScript Overview
description: Understanding the ai-lib-ts architecture and core concepts.
---

# TypeScript Overview

## What is ai-lib-ts?

ai-lib-ts is the official TypeScript/Node.js runtime for AI-Protocol. It provides a unified interface for interacting with AI models across different providers without hardcoding provider-specific logic.

## Design Philosophy

| Principle             | Description                                                                     |
| --------------------- | ------------------------------------------------------------------------------- |
| **Protocol-Driven**   | All behavior is configured through protocol manifests, not code                 |
| **Provider-Agnostic** | Unified interface across OpenAI, Anthropic, Google, DeepSeek, and 30+ providers |
| **Streaming-First**   | Native support for Server-Sent Events (SSE) streaming                           |
| **Type-Safe**         | Strongly typed request/response handling with comprehensive error types         |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Application                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      AiClient                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ ChatBuilder │  │ Embeddings  │  │   Tools     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Pipeline                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Decoder  │→ │ Selector │→ │  Mapper  │→ │ Emitter  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    HttpTransport                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Retry   │  │ Circuit  │  │  Rate    │  │ Backpres │   │
│  │  Policy  │  │ Breaker  │  │ Limiter  │  │   sure   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Protocol Loader                            │
│              (V1 + V2 Manifest Support)                      │
└─────────────────────────────────────────────────────────────┘
```

## Core Modules

### AiClient

The main entry point for AI interactions:

```typescript
import { AiClient, Message } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('anthropic/claude-3-5-sonnet');
const response = await client.chat([Message.user('Hello')]).execute();
```

### Message Types

Support for system, user, and assistant messages with multimodal content:

```typescript
import { Message, ContentBlock } from '@hiddenpath/ai-lib-ts';

const msg = Message.user([
  ContentBlock.text('What is in this image?'),
  ContentBlock.image('https://example.com/image.png'),
]);
```

### Streaming Events

Real-time streaming with typed events:

| Event                 | Description                     |
| --------------------- | ------------------------------- |
| `PartialContentDelta` | Incremental text content        |
| `PartialToolCall`     | Incremental tool call arguments |
| `ToolCallStarted`     | Tool call initiated             |
| `StreamEnd`           | Stream completed                |

### Resilience

Built-in resilience patterns:

- **RetryPolicy**: Exponential backoff retry
- **CircuitBreaker**: Prevent cascading failures
- **RateLimiter**: Token bucket rate limiting
- **Backpressure**: Concurrent request limiting

### Routing

Smart model selection:

- **ModelManager**: Manage multiple model clients
- **CostBasedSelector**: Select by cost efficiency
- **QualityBasedSelector**: Select by quality score
- **FallbackChain**: Failover across models

### Extras

Additional capabilities:

- **EmbeddingClient**: Vector embeddings
- **SttClient**: Speech-to-text
- **TtsClient**: Text-to-speech
- **RerankerClient**: Document reranking
- **McpToolBridge**: MCP protocol integration

## Error Handling

Standardized error codes for consistent error handling:

```typescript
import { AiLibError, StandardErrorCode, isRetryable } from '@hiddenpath/ai-lib-ts';

try {
  const response = await client.chat([Message.user('Hi')]).execute();
} catch (e) {
  if (e instanceof AiLibError) {
    console.log('Code:', e.code);
    console.log('Retryable:', isRetryable(e.code));
  }
}
```

## Next Steps

- **[Quick Start](/ts/quickstart/)** — Get started quickly
- **[AiClient API](/ts/client/)** — Detailed API reference
- **[Resilience](/ts/resilience/)** — Production-ready patterns
