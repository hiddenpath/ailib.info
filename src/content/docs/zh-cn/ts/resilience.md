---
title: TypeScript 弹性模式
description: ai-lib-ts 中生产就绪的弹性模式。
---

# 弹性模式

## 概述

ai-lib-ts 为生产负载提供内置的弹性模式。

## 重试策略

自动重试与指数退避：

```typescript
import { createClientBuilder, RetryPolicy } from '@hiddenpath/ai-lib-ts';

const client = await createClientBuilder()
  .withRetry(RetryPolicy.fromConfig({
    maxRetries: 5,
    initialDelayMs: 100,
    maxDelayMs: 30000,
    multiplier: 2.0,
  }))
  .build('openai/gpt-4o');
```

### 重试配置

| 选项 | 默认值 | 描述 |
|------|--------|------|
| `maxRetries` | 3 | 最大重试次数 |
| `initialDelayMs` | 100 | 初始延迟 (ms) |
| `maxDelayMs` | 30000 | 最大延迟上限 |
| `multiplier` | 2.0 | 退避乘数 |

## 熔断器

防止级联故障：

```typescript
import { CircuitBreaker } from '@hiddenpath/ai-lib-ts';

const breaker = new CircuitBreaker({
  failureThreshold: 5,
  successThreshold: 3,
  timeoutSeconds: 60,
});

const client = await createClientBuilder()
  .withCircuitBreaker(breaker)
  .build('anthropic/claude-3-5-sonnet');

// 监控状态
const signals = await client.signals();
console.log('熔断器状态:', signals.circuitBreaker?.state);
// 状态: 'closed', 'open', 'half-open'
```

### 熔断器状态

| 状态 | 行为 |
|------|------|
| `closed` | 请求正常通过 |
| `open` | 请求立即快速失败 |
| `half-open` | 有限请求测试恢复 |

## 限流器

令牌桶限流：

```typescript
import { RateLimiter } from '@hiddenpath/ai-lib-ts';

const client = await createClientBuilder()
  .withRateLimiter(RateLimiter.fromRps(10)) // 每秒 10 个请求
  .build('openai/gpt-4o');
```

## 背压

限制并发请求：

```typescript
import { Backpressure } from '@hiddenpath/ai-lib-ts';

const client = await createClientBuilder()
  .withBackpressure(new Backpressure({
    maxConcurrent: 20,
  }))
  .build('openai/gpt-4o');
```

## 预检器

统一请求门控（熔断器 + 限流器 + 背压）：

```typescript
import { PreflightChecker, CircuitBreaker, RateLimiter, Backpressure } from '@hiddenpath/ai-lib-ts';

const checker = new PreflightChecker({
  circuitBreaker: new CircuitBreaker({ failureThreshold: 5 }),
  rateLimiter: RateLimiter.fromRps(10),
  backpressure: new Backpressure({ maxConcurrent: 5 }),
});

const result = await checker.check();
if (result.passed) {
  try {
    const response = await client.chat([Message.user('Hi')]).execute();
    checker.onSuccess();
    console.log(response.content);
  } catch (e) {
    checker.onFailure();
    throw e;
  } finally {
    result.release();
  }
}
```

## 回退链

自动回退到备用模型：

```typescript
const client = await createClientBuilder()
  .withFallbacks([
    'anthropic/claude-3-5-sonnet',
    'deepseek/deepseek-chat',
    'openai/gpt-4o-mini',
  ])
  .build('openai/gpt-4o');
```

## 组合模式

```typescript
const client = await createClientBuilder()
  .withRetry(RetryPolicy.fromConfig({ maxRetries: 3 }))
  .withCircuitBreaker(new CircuitBreaker({ failureThreshold: 5 }))
  .withRateLimiter(RateLimiter.fromRps(20))
  .withBackpressure(new Backpressure({ maxConcurrent: 10 }))
  .withFallbacks(['anthropic/claude-3-5-sonnet'])
  .withTimeout(30000)
  .build('openai/gpt-4o');
```
