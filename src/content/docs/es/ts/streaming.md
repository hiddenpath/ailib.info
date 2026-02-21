---
title: TypeScript Streaming
description: How streaming works in ai-lib-ts.
---

# Streaming Pipeline

## Overview

ai-lib-ts provides streaming-first support with Server-Sent Events (SSE) and typed streaming events.

## Basic Streaming

```typescript
import { AiClient, Message } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('openai/gpt-4o');

const stream = client
  .chat([Message.user('Tell me a story')])
  .stream()
  .executeStream();

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## Streaming Events

| Event | Description | Key Fields |
|-------|-------------|------------|
| `PartialContentDelta` | Incremental text | `content` |
| `ToolCallStarted` | Tool call initiated | `toolCallId`, `name` |
| `PartialToolCall` | Incremental tool args | `toolCallId`, `arguments` |
| `StreamEnd` | Stream completed | `finishReason` |

## Event Handling

```typescript
import { StreamingEvent } from '@hiddenpath/ai-lib-ts';

for await (const event of stream) {
  switch (event.event_type) {
    case 'PartialContentDelta':
      process.stdout.write(event.content);
      break;
    
    case 'ToolCallStarted':
      console.log(`\nCalling tool: ${event.name}`);
      break;
    
    case 'PartialToolCall':
      process.stdout.write(event.arguments);
      break;
    
    case 'StreamEnd':
      console.log(`\nFinished: ${event.finishReason}`);
      break;
  }
}
```

## Stream Cancellation

```typescript
const { stream, cancelHandle } = client
  .chat([Message.user('Write a very long story...')])
  .stream()
  .executeStreamWithCancel();

// Set a timeout to cancel after 10 seconds
setTimeout(() => {
  cancelHandle.cancel();
  console.log('Stream cancelled');
}, 10000);

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## Pipeline Architecture

The streaming pipeline processes events through stages:

```
SSE Stream → Decoder → Selector → EventMapper → Emitter
```

### Decoder

Parses raw SSE data into structured events:

```typescript
// Automatically selects decoder based on provider
// OpenAI format, Anthropic format, etc.
```

### Selector

Filters events by type:

```typescript
// Only content events
// Only tool events
// All events
```

### EventMapper

Transforms provider-specific events to standard types:

```typescript
// Provider format → Standard StreamingEvent
```

### Manual Pipeline Creation

```typescript
import { Pipeline, HttpTransport } from '@hiddenpath/ai-lib-ts';

const pipeline = Pipeline.fromManifest(manifest);

const stream = transport.executeStream(request);
for await (const event of stream) {
  const mapped = pipeline.map(event);
  // Handle mapped event
}
```

## AbortSignal Support

```typescript
const controller = new AbortController();

// Cancel after 5 seconds
setTimeout(() => controller.abort(), 5000);

const stream = client
  .chat([Message.user('Long task')])
  .stream()
  .executeStream({ signal: controller.signal });
```

## Best Practices

1. **Always handle errors in streams**
```typescript
try {
  for await (const event of stream) {
    // Handle event
  }
} catch (e) {
  console.error('Stream error:', e);
}
```

2. **Use cancellation for user-initiated stops**
```typescript
// UI: user clicks "Stop" button
cancelHandle.cancel();
```

3. **Buffer for rate limiting**
```typescript
let buffer = '';
for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    buffer += event.content;
  }
}
```
