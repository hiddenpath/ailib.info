---
title: TypeScript AiClient API
description: Detailed API reference for the TypeScript AiClient.
---

# AiClient API

## Creating a Client

### Basic Creation

```typescript
import { AiClient } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('openai/gpt-4o');
```

### With Builder Pattern

```typescript
import { createClientBuilder } from '@hiddenpath/ai-lib-ts';

const client = await createClientBuilder()
  .withFallbacks(['anthropic/claude-3-5-sonnet', 'deepseek/deepseek-chat'])
  .withTimeout(30000)
  .withStrictStreaming(true)
  .build('openai/gpt-4o');
```

## ChatBuilder Methods

### messages(messages: Message[])

Set the conversation messages:

```typescript
const response = await client
  .chat([
    Message.system('You are helpful.'),
    Message.user('Hello!'),
  ])
  .execute();
```

### user(content: string)

Quick single user message:

```typescript
const response = await client
  .chat()
  .user('What is TypeScript?')
  .execute();
```

### temperature(value: number)

Set sampling temperature (0.0 - 2.0):

```typescript
const response = await client
  .chat([Message.user('Be creative')])
  .temperature(0.9)
  .execute();
```

### maxTokens(value: number)

Set maximum output tokens:

```typescript
const response = await client
  .chat([Message.user('Hi')])
  .maxTokens(500)
  .execute();
```

### tools(tools: Tool[])

Add tool definitions:

```typescript
const tool = Tool.define(
  'search',
  {
    type: 'object',
    properties: {
      query: { type: 'string' },
    },
    required: ['query'],
  },
  'Search the web'
);

const response = await client
  .chat([Message.user('Search for TypeScript')])
  .tools([tool])
  .execute();
```

### stream()

Enable streaming mode:

```typescript
const stream = client
  .chat([Message.user('Tell a story')])
  .stream()
  .executeStream();

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## Execution Methods

### execute()

Execute the request and return the response:

```typescript
const response = await client
  .chat([Message.user('Hello')])
  .execute();

console.log(response.content);
console.log(response.toolCalls);
console.log(response.usage);
```

### executeWithStats()

Execute and return response with timing stats:

```typescript
const { response, stats } = await client
  .chat([Message.user('Hi')])
  .executeWithStats();

console.log('Tokens:', stats.totalTokens);
console.log('Latency:', stats.latencyMs, 'ms');
console.log('Model:', stats.model);
```

### executeStream()

Execute as a stream:

```typescript
const stream = client
  .chat([Message.user('Write code')])
  .stream()
  .executeStream();

for await (const event of stream) {
  // Handle events
}
```

### executeStreamWithCancel()

Execute stream with cancellation support:

```typescript
const { stream, cancelHandle } = client
  .chat([Message.user('Long task')])
  .stream()
  .executeStreamWithCancel();

// Later, from another context:
// cancelHandle.cancel();

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## Response Object

```typescript
interface ChatResponse {
  content: string;
  toolCalls?: ParsedToolCall[];
  usage?: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  model: string;
  finishReason: TerminationReason;
}
```

## Error Handling

```typescript
import { AiLibError, StandardErrorCode, isRetryable, isFallbackable } from '@hiddenpath/ai-lib-ts';

try {
  const response = await client.chat([Message.user('Hi')]).execute();
} catch (e) {
  if (e instanceof AiLibError) {
    console.log('Error code:', e.code);
    console.log('Message:', e.message);
    console.log('Retryable:', isRetryable(e.code));
    console.log('Fallbackable:', isFallbackable(e.code));
  }
}
```

## Signals

Get runtime signals for monitoring:

```typescript
const signals = await client.signals();

console.log('Circuit breaker:', signals.circuitBreaker?.state);
console.log('Rate limiter:', signals.rateLimiter?.available);
console.log('Inflight:', signals.inflight?.inUse);
```
