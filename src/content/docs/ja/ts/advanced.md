---
title: TypeScript Advanced Features
description: Advanced features including embeddings, batch processing, MCP, and plugins.
---

# Advanced Features

## Embeddings

Generate vector embeddings for text:

```typescript
import { EmbeddingClient } from '@hiddenpath/ai-lib-ts';

const client = await EmbeddingClient.new('openai/text-embedding-3-small');

const response = await client.embed('Hello, world!');
console.log(`Dimensions: ${response.embeddings[0].vector.length}`);
console.log(`Tokens: ${response.usage?.totalTokens}`);
```

### Batch Embeddings

```typescript
const response = await client.embedBatch([
  'Hello, world!',
  'Goodbye, world!',
  'AI is amazing!',
]);

response.embeddings.forEach((e, i) => {
  console.log(`Text ${i}: ${e.vector.length} dimensions`);
});
```

## Speech-to-Text (STT)

Transcribe audio to text:

```typescript
import { SttClient } from '@hiddenpath/ai-lib-ts';

const client = await SttClient.new('openai/whisper-1');

const response = await client.transcribe(audioBuffer, {
  language: 'en',
  format: 'json',
});

console.log('Transcript:', response.text);
```

## Text-to-Speech (TTS)

Convert text to speech:

```typescript
import { TtsClient } from '@hiddenpath/ai-lib-ts';

const client = await TtsClient.new('openai/tts-1');

const audioBuffer = await client.speak('Hello, this is a test!', {
  voice: 'alloy',
  format: 'mp3',
});

// audioBuffer is ArrayBuffer
```

## Reranking

Reorder documents by relevance:

```typescript
import { RerankerClient } from '@hiddenpath/ai-lib-ts';

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

## MCP Tool Bridge

Bridge MCP tools to AI-Protocol format:

```typescript
import { McpToolBridge } from '@hiddenpath/ai-lib-ts';

const bridge = new McpToolBridge('http://localhost:3001/mcp');

// List available tools
const tools = await bridge.listTools();
console.log('MCP tools:', tools);

// Convert to AI-Protocol format
const toolDefs = tools.map(t => bridge.toToolDefinition(t));

// Use in chat
const response = await client
  .chat([Message.user('Use the search tool')])
  .tools(toolDefs)
  .execute();
```

## Batch Processing

Execute multiple requests in parallel:

```typescript
import { BatchExecutor, batchExecute } from '@hiddenpath/ai-lib-ts';

const op = async (question: string) => {
  const client = await AiClient.new('openai/gpt-4o');
  const r = await client.chat([Message.user(question)]).execute();
  return r.content;
};

const result = await batchExecute(
  ['What is AI?', 'What is Python?', 'What is async?'],
  op,
  { maxConcurrent: 5 }
);

console.log(`Successful: ${result.successfulCount}`);
console.log(`Failed: ${result.failedCount}`);
result.results.forEach((r, i) => {
  if (r.status === 'fulfilled') {
    console.log(`${i}: ${r.value}`);
  }
});
```

### BatchExecutor Class

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

Extend functionality with hooks:

```typescript
import { PluginRegistry, HookManager } from '@hiddenpath/ai-lib-ts';

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
const client = await createClientBuilder()
  .withPlugins(plugins)
  .build('openai/gpt-4o');
```

### Available Hooks

| Hook | Timing | Input |
|------|--------|-------|
| `beforeRequest` | Before API call | Request object |
| `afterResponse` | After API call | Response object |
| `onError` | On error | Error object |
| `onStreamEvent` | Each stream event | Streaming event |

## Token Estimation

Estimate tokens without API call:

```typescript
import { estimateTokens, estimateCost } from '@hiddenpath/ai-lib-ts';

const tokens = estimateTokens('Hello, how are you doing today?');
console.log(`Estimated tokens: ${tokens}`);
```

## Cost Estimation

Estimate cost for a request:

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

## Memory Cache

In-memory caching for responses:

```typescript
import { MemoryCache } from '@hiddenpath/ai-lib-ts';

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

## Structured Output

JSON mode for structured responses:

```typescript
import { jsonObjectConfig, jsonSchemaConfig } from '@hiddenpath/ai-lib-ts';

const response = await client
  .chat([Message.user('Return a JSON object with name and age')])
  .jsonMode(jsonObjectConfig())
  .execute();

const data = JSON.parse(response.content);
console.log('Name:', data.name);
console.log('Age:', data.age);
```

### With JSON Schema

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
