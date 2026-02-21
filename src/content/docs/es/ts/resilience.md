---
title: TypeScript Resilience
description: Production-ready resilience patterns in ai-lib-ts.
---

# Resilience

## Overview

ai-lib-ts provides built-in resilience patterns for production workloads.

## Retry Policy

Automatic retry with exponential backoff:

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

### Retry Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `maxRetries` | 3 | Maximum retry attempts |
| `initialDelayMs` | 100 | Initial delay in ms |
| `maxDelayMs` | 30000 | Maximum delay cap |
| `multiplier` | 2.0 | Backoff multiplier |

## Circuit Breaker

Prevent cascading failures:

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

// Monitor state
const signals = await client.signals();
console.log('Circuit state:', signals.circuitBreaker?.state);
// States: 'closed', 'open', 'half-open'
```

### Circuit Breaker States

| State | Behavior |
|-------|----------|
| `closed` | Requests pass through normally |
| `open` | Requests fail fast immediately |
| `half-open` | Limited requests to test recovery |

## Rate Limiter

Token bucket rate limiting:

```typescript
import { RateLimiter } from '@hiddenpath/ai-lib-ts';

const client = await createClientBuilder()
  .withRateLimiter(RateLimiter.fromRps(10)) // 10 requests per second
  .build('openai/gpt-4o');
```

### Rate Limiter Configuration

```typescript
const limiter = new RateLimiter({
  tokensPerSecond: 10,
  bucketSize: 20,
});
```

## Backpressure

Limit concurrent requests:

```typescript
import { Backpressure } from '@hiddenpath/ai-lib-ts';

const client = await createClientBuilder()
  .withBackpressure(new Backpressure({
    maxConcurrent: 20,
  }))
  .build('openai/gpt-4o');
```

## PreflightChecker

Unified request gating (circuit breaker + rate limiter + backpressure):

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
} else {
  console.log('Request gated:', result.reason);
}
```

## Fallback Chain

Automatic fallback to backup models:

```typescript
const client = await createClientBuilder()
  .withFallbacks([
    'anthropic/claude-3-5-sonnet',
    'deepseek/deepseek-chat',
    'openai/gpt-4o-mini',
  ])
  .build('openai/gpt-4o');
```

## Combining Patterns

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

## Monitoring

Get runtime signals:

```typescript
const signals = await client.signals();

console.log('Circuit breaker:', signals.circuitBreaker);
// { state: 'closed', failures: 2, successes: 10 }

console.log('Rate limiter:', signals.rateLimiter);
// { available: 8, total: 10 }

console.log('Inflight:', signals.inflight);
// { inUse: 3, max: 20 }
```
