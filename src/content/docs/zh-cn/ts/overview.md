---
title: TypeScript 概述
description: 理解 ai-lib-ts 架构和核心概念。
---

# TypeScript 概述

## 什么是 ai-lib-ts？

ai-lib-ts 是 AI-Protocol 的官方 TypeScript/Node.js 运行时。它提供了统一的接口来与不同提供商的 AI 模型交互，无需硬编码提供商特定的逻辑。

## 设计理念

| 原则 | 描述 |
|------|------|
| **协议驱动** | 所有行为通过协议清单配置，而非代码 |
| **提供商无关** | 统一接口支持 OpenAI、Anthropic、Google、DeepSeek 等 30+ 提供商 |
| **流式优先** | 原生支持服务器发送事件 (SSE) 流式输出 |
| **类型安全** | 强类型的请求/响应处理和完整的错误类型 |

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│                       应用层                                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      AiClient                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ ChatBuilder │  │  Embeddings │  │   Tools     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Pipeline                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Decoder  │→ │ Selector │→ │  Mapper  │→ │ Emitter  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    HttpTransport                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Retry   │  │ Circuit  │  │  Rate    │  │ Backpres │   │
│  │  Policy  │  │ Breaker  │  │ Limiter  │  │   sure   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Protocol Loader                            │
│              (V1 + V2 清单支持)                              │
└─────────────────────────────────────────────────────────────┘
```

## 核心模块

### AiClient

AI 交互的主入口：

```typescript
import { AiClient, Message } from '@hiddenpath/ai-lib-ts';

const client = await AiClient.new('anthropic/claude-3-5-sonnet');
const response = await client.chat([Message.user('你好')]).execute();
```

### 消息类型

支持系统、用户和助手消息及多模态内容：

```typescript
import { Message, ContentBlock } from '@hiddenpath/ai-lib-ts';

const msg = Message.user([
  ContentBlock.text('这张图片是什么？'),
  ContentBlock.image('https://example.com/image.png'),
]);
```

### 流式事件

实时流式输出与类型化事件：

| 事件 | 描述 |
|------|------|
| `PartialContentDelta` | 增量文本内容 |
| `PartialToolCall` | 增量工具调用参数 |
| `ToolCallStarted` | 工具调用已启动 |
| `StreamEnd` | 流已结束 |

### 弹性模式

内置弹性模式：

- **RetryPolicy**：指数退避重试
- **CircuitBreaker**：防止级联故障
- **RateLimiter**：令牌桶限流
- **Backpressure**：并发请求限制

### 路由

智能模型选择：

- **ModelManager**：管理多个模型客户端
- **CostBasedSelector**：按成本效率选择
- **QualityBasedSelector**：按质量分数选择
- **FallbackChain**：跨模型故障转移

### 扩展功能

附加能力：

- **EmbeddingClient**：向量嵌入
- **SttClient**：语音转文字
- **TtsClient**：文字转语音
- **RerankerClient**：文档重排序
- **McpToolBridge**：MCP 协议集成

## 错误处理

标准化的错误码用于一致的错误处理：

```typescript
import { AiLibError, StandardErrorCode, isRetryable } from '@hiddenpath/ai-lib-ts';

try {
  const response = await client.chat([Message.user('Hi')]).execute();
} catch (e) {
  if (e instanceof AiLibError) {
    console.log('错误码:', e.code);
    console.log('可重试:', isRetryable(e.code));
  }
}
```

## 下一步

- **[快速开始](/ts/quickstart/)** — 快速上手
- **[AiClient API](/ts/client/)** — 详细 API 参考
- **[弹性模式](/ts/resilience/)** — 生产就绪的模式
