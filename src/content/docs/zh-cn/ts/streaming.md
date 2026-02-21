---
title: TypeScript 流式输出
description: ai-lib-ts 中流式输出的工作原理。
---

# 流式管道

## 概述

ai-lib-ts 提供流式优先的支持，基于服务器发送事件 (SSE) 和类型化流式事件。

## 基本流式

```typescript
import { AiClient, Message } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('openai/gpt-4o');

const stream = client
  .chat([Message.user('讲个故事')])
  .stream()
  .executeStream();

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## 流式事件

| 事件 | 描述 | 关键字段 |
|------|------|---------|
| `PartialContentDelta` | 增量文本 | `content` |
| `ToolCallStarted` | 工具调用已启动 | `toolCallId`, `name` |
| `PartialToolCall` | 增量工具参数 | `toolCallId`, `arguments` |
| `StreamEnd` | 流已结束 | `finishReason` |

## 事件处理

```typescript
import { StreamingEvent } from '@hiddenpath/ai-lib-ts';

for await (const event of stream) {
  switch (event.event_type) {
    case 'PartialContentDelta':
      process.stdout.write(event.content);
      break;
    
    case 'ToolCallStarted':
      console.log(`\n调用工具: ${event.name}`);
      break;
    
    case 'PartialToolCall':
      process.stdout.write(event.arguments);
      break;
    
    case 'StreamEnd':
      console.log(`\n完成: ${event.finishReason}`);
      break;
  }
}
```

## 流取消

```typescript
const { stream, cancelHandle } = client
  .chat([Message.user('写一个非常长的故事...')])
  .stream()
  .executeStreamWithCancel();

// 设置 10 秒后取消
setTimeout(() => {
  cancelHandle.cancel();
  console.log('流已取消');
}, 10000);

for await (const event of stream) {
  if (event.event_type === 'PartialContentDelta') {
    process.stdout.write(event.content);
  }
}
```

## AbortSignal 支持

```typescript
const controller = new AbortController();

// 5 秒后取消
setTimeout(() => controller.abort(), 5000);

const stream = client
  .chat([Message.user('长任务')])
  .stream()
  .executeStream({ signal: controller.signal });
```

## 最佳实践

1. **始终处理流中的错误**
```typescript
try {
  for await (const event of stream) {
    // 处理事件
  }
} catch (e) {
  console.error('流错误:', e);
}
```

2. **用户主动停止时使用取消**
```typescript
// UI: 用户点击"停止"按钮
cancelHandle.cancel();
```
