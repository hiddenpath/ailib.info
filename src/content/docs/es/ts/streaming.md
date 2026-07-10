---
title: Streaming en TypeScript
description: Cómo funciona el streaming en ai-lib-ts.
---

# Pipeline de streaming

## Descripción general

ai-lib-ts ofrece soporte orientado al streaming con Server-Sent Events (SSE) y eventos de streaming tipados.

## Streaming básico

```typescript
import { AiClient, Message } from '@ailib-official/ai-lib-ts';

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

## Eventos de streaming

| Evento                 | Descripción           | Campos clave                |
| --------------------- | --------------------- | ------------------------- |
| `PartialContentDelta` | Texto incremental      | `content`                 |
| `ToolCallStarted`     | Llamada a herramienta iniciada   | `toolCallId`, `name`      |
| `PartialToolCall`     | Argumentos de herramienta incrementales | `toolCallId`, `arguments` |
| `StreamEnd`           | Flujo completado      | `finishReason`            |

## Manejo de eventos

```typescript
import { StreamingEvent } from '@ailib-official/ai-lib-ts';

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

## Cancelación del flujo

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

## Arquitectura del pipeline

El pipeline de streaming procesa eventos en etapas:

```
SSE Stream → Decoder → Selector → EventMapper → Emitter
```

### Decoder

Analiza datos SSE en bruto en eventos estructurados:

```typescript
// Automatically selects decoder based on provider
// OpenAI format, Anthropic format, etc.
```

### Selector

Filtra eventos por tipo:

```typescript
// Only content events
// Only tool events
// All events
```

### EventMapper

Transforma eventos específicos del proveedor a tipos estándar:

```typescript
// Provider format → Standard StreamingEvent
```

### Creación manual del pipeline

```typescript
import { Pipeline, HttpTransport } from '@ailib-official/ai-lib-ts';

const pipeline = Pipeline.fromManifest(manifest);

const stream = transport.executeStream(request);
for await (const event of stream) {
  const mapped = pipeline.map(event);
  // Handle mapped event
}
```

## Soporte de AbortSignal

```typescript
const controller = new AbortController();

// Cancel after 5 seconds
setTimeout(() => controller.abort(), 5000);

const stream = client
  .chat([Message.user('Long task')])
  .stream()
  .executeStream({ signal: controller.signal });
```

## Buenas prácticas

1. **Siempre maneje errores en los flujos**

```typescript
try {
  for await (const event of stream) {
    // Handle event
  }
} catch (e) {
  console.error('Stream error:', e);
}
```

2. **Use la cancelación para paradas iniciadas por el usuario**

```typescript
// UI: user clicks "Stop" button
cancelHandle.cancel();
```

3. **Acumule en búfer para limitar la tasa**

```typescript
let buffer = '';
for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    buffer += event.content;
  }
}
```
