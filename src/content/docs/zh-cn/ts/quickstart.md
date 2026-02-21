---
title: TypeScript 快速开始
description: 数分钟内上手 ai-lib-ts。
---

# TypeScript 快速开始

## 安装

```bash
npm install @hiddenpath/ai-lib-ts

# 或
yarn add @hiddenpath/ai-lib-ts

# 或
pnpm add @hiddenpath/ai-lib-ts
```

## 配置

库会自动在以下位置查找协议清单：
1. `node_modules/ai-protocol/dist` 或 `node_modules/@hiddenpath/ai-protocol/dist`
2. `../ai-protocol/dist` 或 `./protocols`

### Provider API 密钥

通过环境变量 `<PROVIDER_ID>_API_KEY` 设置 API 密钥：

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="..."
```

## 基本聊天

```typescript
import { AiClient, Message } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('deepseek/deepseek-chat');

const response = await client
  .chat([
    Message.system('你是一个有帮助的助手。'),
    Message.user('用简单的语言解释量子计算'),
  ])
  .temperature(0.7)
  .maxTokens(500)
  .execute();

console.log(response.content);
```

## 流式输出

```typescript
import { AiClient, Message } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('anthropic/claude-3-5-sonnet');

const stream = client
  .chat([
    Message.system('你是一个有帮助的助手。'),
    Message.user('讲一个短故事。'),
  ])
  .stream()
  .executeStream();

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## 工具调用

```typescript
import { AiClient, Message, Tool } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('openai/gpt-4o');

const weatherTool = Tool.define(
  'get_weather',
  {
    type: 'object',
    properties: {
    location: { type: 'string', description: '城市名称' },
  },
  required: ['location'],
  },
  '获取指定位置的当前天气'
);

const response = await client
  .chat([Message.user('东京的天气怎么样？')])
  .tools([weatherTool])
  .execute();

if (response.toolCalls) {
  for (const tc of response.toolCalls) {
    console.log(`调用 ${tc.function.name}: ${tc.function.arguments}`);
  }
}
```

## 多轮对话

```typescript
import { AiClient, Message } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('anthropic/claude-3-5-sonnet');

const messages = [
  Message.system('你是一个有帮助的编程助手。'),
  Message.user('TypeScript 中的闭包是什么？'),
];

const response = await client
  .chat(messages)
  .execute();

console.log(response.content);
```

## 获取统计信息

```typescript
const { response, stats } = await client
  .chat([Message.user('你好！')])
  .executeWithStats();

console.log('内容:', response.content);
console.log('总 Token 数:', stats.totalTokens);
console.log('延迟:', stats.latencyMs, 'ms');
```

## 下一步

- **[AiClient API](/ts/client/)** — 详细 API 参考
- **[流式管道](/ts/streaming/)** — 流式输出工作原理
- **[弹性模式](/ts/resilience/)** — 熔断器、限流、重试
- **[高级功能](/ts/advanced/)** — 嵌入、缓存、插件、批处理
