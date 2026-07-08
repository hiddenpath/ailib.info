---
title: TypeScript クイックスタート
description: 数分钟内上手 ai-lib-ts。
---

# TypeScript クイックスタート

## インサ安装

```bash
npm install @ailib-official/ai-lib-ts

# 或
yarn add @ailib-official/ai-lib-ts

# 或
pnpm add @ailib-official/ai-lib-ts
```

## 訽置

库会自动在以下位置查找协议清单：

1. `node_modules/@ailib-official/ai-protocol/dist`（`npm i @ailib-official/ai-protocol`）、または従来の `node_modules/ai-protocol/dist` / `node_modules/@ailib-official/ai-protocol/dist`
2. `../ai-protocol/dist`、 `./protocols`

### Provider API 寊钥钥

通过环境变量 `<PROVIDER_ID>_API_KEY` 设置 API 密钥：

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="..."
```

## 崚本聊天

```typescript
import { AiClient, Message } from '@ailib-official/ai-lib-ts';

const client = await AiClient.new('deepseek/deepseek-chat');

const response = await client
  .chat([Message.system('You are a helpful assistant.'), Message.user('简单解释量子计算')])
  .temperature(0.7)
  .maxTokens(500)
  .execute();

console.log(response.content);
```

## 流式
