---
title: API de AiClient en TypeScript
description: Referencia detallada de la API de AiClient en TypeScript.
---

# API de AiClient

## Crear un cliente

### Creación básica

```typescript
import { AiClient } from '@ailib-official/ai-lib-ts';

const client = await AiClient.new('openai/gpt-4o');
```

### Con patrón builder

```typescript
import { createClientBuilder } from '@ailib-official/ai-lib-ts';

const client = await createClientBuilder()
  .withFallbacks(['anthropic/claude-3-5-sonnet', 'deepseek/deepseek-chat'])
  .withTimeout(30000)
  .withStrictStreaming(true)
  .build('openai/gpt-4o');
```

## Métodos de ChatBuilder

### messages(messages: Message[])

Establece los mensajes de la conversación:

```typescript
const response = await client
  .chat([Message.system('You are helpful.'), Message.user('Hello!')])
  .execute();
```

### user(content: string)

Un mensaje de usuario rápido:

```typescript
const response = await client.chat().user('What is TypeScript?').execute();
```

### temperature(value: number)

Establece la temperatura de muestreo (0.0 - 2.0):

```typescript
const response = await client
  .chat([Message.user('Be creative')])
  .temperature(0.9)
  .execute();
```

### maxTokens(value: number)

Establece el máximo de tokens de salida:

```typescript
const response = await client
  .chat([Message.user('Hi')])
  .maxTokens(500)
  .execute();
```

### tools(tools: Tool[])

Añade definiciones de herramientas:

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

Activa el modo streaming:

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

## Métodos de ejecución

### execute()

Ejecuta la petición y devuelve la respuesta:

```typescript
const response = await client.chat([Message.user('Hello')]).execute();

console.log(response.content);
console.log(response.toolCalls);
console.log(response.usage);
```

### executeWithStats()

Ejecuta y devuelve la respuesta con estadísticas de tiempo:

```typescript
const { response, stats } = await client.chat([Message.user('Hi')]).executeWithStats();

console.log('Tokens:', stats.totalTokens);
console.log('Latency:', stats.latencyMs, 'ms');
console.log('Model:', stats.model);
```

### executeStream()

Ejecuta como flujo:

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

Ejecuta un flujo con soporte de cancelación:

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

## Objeto de respuesta

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

## Manejo de errores

```typescript
import { AiLibError, StandardErrorCode, isRetryable, isFallbackable } from '@ailib-official/ai-lib-ts';

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

## Señales

Obtiene señales de tiempo de ejecución para monitorización:

```typescript
const signals = await client.signals();

console.log('Circuit breaker:', signals.circuitBreaker?.state);
console.log('Rate limiter:', signals.rateLimiter?.available);
console.log('Inflight:', signals.inflight?.inUse);
```
