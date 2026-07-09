---
title: TypeScript Quick Start
description: Get up and running with ai-lib-ts in minutes.
---

# TypeScript Quick Start

## Installation

```bash
npm install @ailib-official/ai-lib-ts
export OPENAI_API_KEY="your-key"
```

Requires **Node 18+**.

## Basic Chat

```typescript
import { AiClient, Message } from '@ailib-official/ai-lib-ts';

const client = await AiClient.new('openai/gpt-4o');

const response = await client
  .chat([
    Message.system('You are a helpful assistant.'),
    Message.user('Hello!'),
  ])
  .execute();

console.log(response.content);
```

## Mock server

```typescript
import { Message, createClientBuilder } from '@ailib-official/ai-lib-ts';

const client = await createClientBuilder()
  .withMockServer('http://localhost:4010')
  .build('openai/gpt-4o');

const response = await client.chat([Message.user('Hello!')]).execute();
```

Requires [ai-protocol-mock](https://github.com/ailib-official/ai-protocol-mock). Pattern from `tests/integration.test.ts`.

## Streaming

```typescript
const stream = client
  .chat([Message.user('Count from 1 to 5')])
  .stream()
  .executeStream();

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## Entry points

- **Full SDK:** `@ailib-official/ai-lib-ts`
- **Execution only:** `@ailib-official/ai-lib-ts/core` (no policy retry wrapper)
- **Policy only:** `@ailib-official/ai-lib-ts/contact`

## Next Steps

- **[Client API](/ts/client/)**
- **[Streaming](/ts/streaming/)**
- **[Resilience](/ts/resilience/)**
