---
title: TypeScript クイックスタート
description: TypeScript/Node.js ランタイム，面向 npm 生态系统。协议驱动、流式优先。

## イン

---

title: TypeScript クイックスタート
description: TypeScript/Node.js ランタイム、面向 npm 生态系统。协议驱动、流式优先。

## イン

```bash
npm install @hiddenpath/ai-lib-ts
# 或
yarn add @hiddenpath/ai-lib-ts
# 或
pnpm add @hiddenpath/ai-lib-ts
```

## 設定

库会自动在以下位置查找协议清单文件：
1. `node_modules/ai-protocol/dist` 或 `node_modules/@hiddenpath/ai-protocol/dist`
2. `../ai-protocol/dist` 或 `./protocols`

### Provider API 密钥钥

通过环境变量 `<PROVIDER_ID>_API_KEY` 设置：

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="..."
```

## 嵌入

```typescript
import { EmbeddingClient } from '@hiddenpath/ai-lib-ts';

const client = await EmbeddingClient.new('openai/text-embedding-3-small');

const response = await client.embed('你好，世界！');
console.log(`维度: ${response.embeddings[0].vector.length}`);
```

## 批处理

```typescript
import { batchExecute } from '@hiddenpath/ai-lib-ts';

const result = await batchExecute(
  ['问题1', '问题2', '问题3'],
  async (q: string) => {
    const client = await AiClient.new('openai/gpt-4o');
    return (await client.chat([Message.user(q)]).execute()).content;
  },
  { maxConcurrent: 3 }
);
```
