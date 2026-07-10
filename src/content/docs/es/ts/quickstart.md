---
title: Inicio rápido de TypeScript
description: Empiece a usar ai-lib-ts en minutos.
---

# Inicio rápido de TypeScript

## Instalación

```bash
npm install @ailib-official/ai-lib-ts
export OPENAI_API_KEY="your-key"
```

Requiere **Node 18+**.

## Chat básico

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

## Servidor mock

```typescript
import { Message, createClientBuilder } from '@ailib-official/ai-lib-ts';

const client = await createClientBuilder()
  .withMockServer('http://localhost:4010')
  .build('openai/gpt-4o');

const response = await client.chat([Message.user('Hello!')]).execute();
```

Requiere [ai-protocol-mock](https://github.com/ailib-official/ai-protocol-mock). El patrón proviene de `tests/integration.test.ts`.

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

## Puntos de entrada

- **SDK completo:** `@ailib-official/ai-lib-ts`
- **Solo ejecución:** `@ailib-official/ai-lib-ts/core` (sin envoltorio de reintentos de política)
- **Solo política:** `@ailib-official/ai-lib-ts/contact`

## Siguientes pasos

- **[API del cliente](/es/ts/client/)**
- **[Streaming](/es/ts/streaming/)**
- **[Resiliencia](/es/ts/resilience/)**
