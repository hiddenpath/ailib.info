---
title: TypeScript Quick Start
description: Get up and running with ai-lib-ts in minutes.
---

# TypeScript Quick Start

## Installation

```bash
npm install @hiddenpath/ai-lib-ts

# or
yarn add @hiddenpath/ai-lib-ts

# or
pnpm add @hiddenpath/ai-lib-ts
```

## Configuration

The library automatically looks for protocol manifests in these locations:
1. `node_modules/ai-protocol/dist` or `node_modules/@hiddenpath/ai-protocol/dist`
2. `../ai-protocol/dist` or `./protocols`

### Provider API Keys

Set API keys via environment variables `<PROVIDER_ID>_API_KEY`:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="..."
```

## Basic Chat

```typescript
import { AiClient, Message } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('deepseek/deepseek-chat');

const response = await client
  .chat([
    Message.system('You are a helpful assistant.'),
    Message.user('Explain quantum computing in simple terms'),
  ])
  .temperature(0.7)
  .maxTokens(500)
  .execute();

console.log(response.content);
```

## Streaming

```typescript
import { AiClient, Message } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('anthropic/claude-3-5-sonnet');

const stream = client
  .chat([
    Message.system('You are a helpful assistant.'),
    Message.user('Tell me a short story.'),
  ])
  .stream()
  .executeStream();

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## Tool Calling

```typescript
import { AiClient, Message, Tool } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('openai/gpt-4o');

const weatherTool = Tool.define(
  'get_weather',
  {
    type: 'object',
    properties: {
    location: { type: 'string', description: 'City name' },
  },
  required: ['location'],
  },
  'Get current weather for a location'
);

const response = await client
  .chat([Message.user("What's the weather in Tokyo?")])
  .tools([weatherTool])
  .execute();

if (response.toolCalls) {
  for (const tc of response.toolCalls) {
    console.log(`Call ${tc.function.name}: ${tc.function.arguments}`);
  }
}
```

## Multi-turn Conversation

```typescript
import { AiClient, Message } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('anthropic/claude-3-5-sonnet');

const messages = [
  Message.system('You are a helpful coding assistant.'),
  Message.user('What is a closure in TypeScript?'),
];

const response = await client
  .chat(messages)
  .execute();

console.log(response.content);
```

## With Stats

```typescript
const { response, stats } = await client
  .chat([Message.user('Hello!')])
  .executeWithStats();

console.log('Content:', response.content);
console.log('Total tokens:', stats.totalTokens);
console.log('Latency:', stats.latencyMs, 'ms');
```

## Next Steps

- **[AiClient API](/ts/client/)** — Detailed API reference
- **[Streaming Pipeline](/ts/streaming/)** — How streaming works
- **[Resilience](/ts/resilience/)** — Circuit breaker, rate limiting, retry
- **[Advanced Features](/ts/advanced/)** — Embeddings, cache, plugins, batch
