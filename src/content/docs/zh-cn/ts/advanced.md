---
title: TypeScript 高级功能
description: 高级功能包括嵌入、批处理、MCP 和插件。
---

# 高级功能

## 嵌入

为文本生成向量嵌入：

```typescript
import { EmbeddingClient } from '@hiddenpath/ai-lib-ts';

const client = await EmbeddingClient.new('openai/text-embedding-3-small');

const response = await client.embed('你好，世界！');
console.log(`维度: ${response.embeddings[0].vector.length}`);
console.log(`Token 数: ${response.usage?.totalTokens}`);
```

### 批量嵌入

```typescript
const response = await client.embedBatch([
  '你好，世界！',
  '再见，世界！',
  'AI 太神奇了！',
]);

response.embeddings.forEach((e, i) => {
  console.log(`文本 ${i}: ${e.vector.length} 维`);
});
```

## 语音转文字 (STT)

将音频转录为文字：

```typescript
import { SttClient } from '@hiddenpath/ai-lib-ts';

const client = await SttClient.new('openai/whisper-1');

const response = await client.transcribe(audioBuffer, {
  language: 'zh',
  format: 'json',
});

console.log('转录:', response.text);
```

## 文字转语音 (TTS)

将文字转换为语音：

```typescript
import { TtsClient } from '@hiddenpath/ai-lib-ts';

const client = await TtsClient.new('openai/tts-1');

const audioBuffer = await client.speak('你好，这是一个测试！', {
  voice: 'alloy',
  format: 'mp3',
});

// audioBuffer 是 ArrayBuffer
```

## 重排序

按相关性重新排序文档：

```typescript
import { RerankerClient } from '@hiddenpath/ai-lib-ts';

const client = await RerankerClient.new('cohere/rerank-english-v3.0');

const result = await client.rerank({
  query: '什么是机器学习？',
  documents: [
    '机器学习是 AI 的一个子集...',
    '深度学习使用神经网络...',
    'Python 是一种编程语言...',
  ],
  topN: 3,
});

result.results.forEach((r, i) => {
  console.log(`${i + 1}. 分数: ${r.relevanceScore}, 文档: ${r.document}`);
});
```

## MCP 工具桥

将 MCP 工具桥接到 AI-Protocol 格式：

```typescript
import { McpToolBridge } from '@hiddenpath/ai-lib-ts';

const bridge = new McpToolBridge('http://localhost:3001/mcp');

// 列出可用工具
const tools = await bridge.listTools();
console.log('MCP 工具:', tools);

// 转换为 AI-Protocol 格式
const toolDefs = tools.map(t => bridge.toToolDefinition(t));

// 在聊天中使用
const response = await client
  .chat([Message.user('使用搜索工具')])
  .tools(toolDefs)
  .execute();
```

## 批处理

并行执行多个请求：

```typescript
import { BatchExecutor, batchExecute } from '@hiddenpath/ai-lib-ts';

const op = async (question: string) => {
  const client = await AiClient.new('openai/gpt-4o');
  const r = await client.chat([Message.user(question)]).execute();
  return r.content;
};

const result = await batchExecute(
  ['什么是 AI？', '什么是 Python？', '什么是 async？'],
  op,
  { maxConcurrent: 5 }
);

console.log(`成功: ${result.successfulCount}`);
console.log(`失败: ${result.failedCount}`);
result.results.forEach((r, i) => {
  if (r.status === 'fulfilled') {
    console.log(`${i}: ${r.value}`);
  }
});
```

## 插件

通过钩子扩展功能：

```typescript
import { PluginRegistry } from '@hiddenpath/ai-lib-ts';

const plugins = new PluginRegistry();

// 注册插件
plugins.register({
  name: 'logger',
  hooks: {
    beforeRequest: async (req) => {
      console.log('请求:', req);
      return req;
    },
    afterResponse: async (res) => {
      console.log('响应:', res.content.slice(0, 100));
      return res;
    },
  },
});

// 与客户端一起使用
const client = await createClientBuilder()
  .withPlugins(plugins)
  .build('openai/gpt-4o');
```

### 可用钩子

| 钩子 | 时机 | 输入 |
|------|------|------|
| `beforeRequest` | API 调用前 | 请求对象 |
| `afterResponse` | API 调用后 | 响应对象 |
| `onError` | 出错时 | 错误对象 |
| `onStreamEvent` | 每个流事件 | 流事件 |

## Token 估算

无需 API 调用估算 Token：

```typescript
import { estimateTokens, estimateCost } from '@hiddenpath/ai-lib-ts';

const tokens = estimateTokens('你好，今天过得怎么样？');
console.log(`估算 Token: ${tokens}`);
```

## 成本估算

估算请求成本：

```typescript
const cost = estimateCost({
  inputTokens: 1000,
  outputTokens: 500,
  model: 'gpt-4o',
});

console.log(`输入成本: $${cost.inputCost}`);
console.log(`输出成本: $${cost.outputCost}`);
console.log(`总成本: $${cost.totalCost}`);
```
