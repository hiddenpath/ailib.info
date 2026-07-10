---
title: Funciones avanzadas de TypeScript
description: "Funciones avanzadas: embeddings, procesamiento por lotes, MCP y plugins."
---

# Funciones avanzadas

## Embeddings

Genere embeddings vectoriales a partir de texto:

```typescript
import { EmbeddingClient } from '@ailib-official/ai-lib-ts';

const client = await EmbeddingClient.new('openai/text-embedding-3-small');

const response = await client.embed('Hello, world!');
console.log(`Dimensions: ${response.embeddings[0].vector.length}`);
console.log(`Tokens: ${response.usage?.totalTokens}`);
```

### Embeddings por lotes

```typescript
const response = await client.embedBatch(['Hello, world!', 'Goodbye, world!', 'AI is amazing!']);

response.embeddings.forEach((e, i) => {
  console.log(`Text ${i}: ${e.vector.length} dimensions`);
});
```

## Voz a texto (STT)

Transcriba audio a texto:

```typescript
import { SttClient } from '@ailib-official/ai-lib-ts';

const client = await SttClient.new('openai/whisper-1');

const response = await client.transcribe(audioBuffer, {
  language: 'en',
  format: 'json',
});

console.log('Transcript:', response.text);
```

## Texto a voz (TTS)

Convierta texto en audio:

```typescript
import { TtsClient } from '@ailib-official/ai-lib-ts';

const client = await TtsClient.new('openai/tts-1');

const audioBuffer = await client.speak('Hello, this is a test!', {
  voice: 'alloy',
  format: 'mp3',
});

// audioBuffer is ArrayBuffer
```

## Reordenación (reranking)

Reordene documentos por relevancia:

```typescript
import { RerankerClient } from '@ailib-official/ai-lib-ts';

const client = await RerankerClient.new('cohere/rerank-english-v3.0');

const result = await client.rerank({
  query: 'What is machine learning?',
  documents: [
    'Machine learning is a subset of AI...',
    'Deep learning uses neural networks...',
    'Python is a programming language...',
  ],
  topN: 3,
});

result.results.forEach((r, i) => {
  console.log(`${i + 1}. Score: ${r.relevanceScore}, Doc: ${r.document}`);
});
```

## Puente de herramientas MCP

`McpToolBridge` **solo convierte** definiciones de herramientas MCP al formato AI-Protocol. No incluye transporte de servidor MCP dentro de `AiClient`.

```typescript
import { McpToolBridge } from '@ailib-official/ai-lib-ts';

const bridge = new McpToolBridge('http://localhost:3001/mcp');

// List available tools
const tools = await bridge.listTools();
console.log('MCP tools:', tools);

// Convert to AI-Protocol format
const toolDefs = tools.map((t) => bridge.toToolDefinition(t));

// Use in chat
const response = await client
  .chat([Message.user('Use the search tool')])
  .tools(toolDefs)
  .execute();
```

## Procesamiento por lotes

Ejecute varias peticiones en paralelo:

```typescript
import { BatchExecutor, batchExecute } from '@ailib-official/ai-lib-ts';

const op = async (question: string) => {
  const client = await AiClient.new('openai/gpt-4o');
  const r = await client.chat([Message.user(question)]).execute();
  return r.content;
};

const result = await batchExecute(['What is AI?', 'What is Python?', 'What is async?'], op, {
  maxConcurrent: 5,
});

console.log(`Successful: ${result.successfulCount}`);
console.log(`Failed: ${result.failedCount}`);
result.results.forEach((r, i) => {
  if (r.status === 'fulfilled') {
    console.log(`${i}: ${r.value}`);
  }
});
```

### Clase BatchExecutor

```typescript
const executor = new BatchExecutor({
  maxConcurrent: 10,
  retryPolicy: RetryPolicy.fromConfig({ maxRetries: 2 }),
});

// Add tasks
executor.add(() => client.chat([Message.user('Task 1')]).execute());
executor.add(() => client.chat([Message.user('Task 2')]).execute());

// Wait for all
const results = await executor.waitForAll();
```

## Plugins

Amplíe la funcionalidad con hooks:

```typescript
import { PluginRegistry, HookManager } from '@ailib-official/ai-lib-ts';

const plugins = new PluginRegistry();

// Register a plugin
plugins.register({
  name: 'logger',
  hooks: {
    beforeRequest: async (req) => {
      console.log('Request:', req);
      return req;
    },
    afterResponse: async (res) => {
      console.log('Response:', res.content.slice(0, 100));
      return res;
    },
  },
});

// Use with client
const client = await createClientBuilder().withPlugins(plugins).build('openai/gpt-4o');
```

### Hooks disponibles

| Hook            | Momento            | Entrada           |
| --------------- | ----------------- | --------------- |
| `beforeRequest` | Antes de la llamada a la API   | Objeto de petición  |
| `afterResponse` | Después de la llamada a la API    | Objeto de respuesta |
| `onError`       | Ante un error          | Objeto de error    |
| `onStreamEvent` | Cada evento de streaming | Evento de streaming |

## Estimación de tokens

Estime tokens sin llamar a la API:

```typescript
import { estimateTokens, estimateCost } from '@ailib-official/ai-lib-ts';

const tokens = estimateTokens('Hello, how are you doing today?');
console.log(`Estimated tokens: ${tokens}`);
```

## Estimación de coste

Estime el coste de una petición:

```typescript
const cost = estimateCost({
  inputTokens: 1000,
  outputTokens: 500,
  model: 'gpt-4o',
});

console.log(`Input cost: $${cost.inputCost}`);
console.log(`Output cost: $${cost.outputCost}`);
console.log(`Total cost: $${cost.totalCost}`);
```

## Caché en memoria

Caché en memoria para respuestas:

```typescript
import { MemoryCache } from '@ailib-official/ai-lib-ts';

const cache = new MemoryCache({
  maxSize: 1000,
  ttlSeconds: 3600,
});

// Check cache
const cached = await cache.get('cache-key');
if (cached) {
  console.log('Cache hit:', cached);
}

// Store in cache
await cache.set('cache-key', response);
```

## Salida estructurada

Modo JSON para respuestas estructuradas:

```typescript
import { jsonObjectConfig, jsonSchemaConfig } from '@ailib-official/ai-lib-ts';

const response = await client
  .chat([Message.user('Return a JSON object with name and age')])
  .jsonMode(jsonObjectConfig())
  .execute();

const data = JSON.parse(response.content);
console.log('Name:', data.name);
console.log('Age:', data.age);
```

### Con JSON Schema

```typescript
const schema = {
  type: 'object',
  properties: {
    name: { type: 'string' },
    age: { type: 'number' },
  },
  required: ['name', 'age'],
};

const response = await client
  .chat([Message.user('Generate a person')])
  .jsonMode(jsonSchemaConfig(schema))
  .execute();
```
