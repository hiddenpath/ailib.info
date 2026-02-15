---
title: 耐障害性（Python）
description: ai-lib-python v0.6.0 における本番グレードの信頼性パターン — ResilientExecutor、サーキットブレーカー、レートリミッター、フォールバック。
---

# 耐障害性パターン

ai-lib-python（v0.6.0+）には、`ResilientExecutor` を中心とした包括的な耐障害性システムが含まれています。リトライとフォールバックの判断は、`StandardErrorCode` の `retryable` と `fallbackable` プロパティを介して V2 標準エラーコードを使用するようになり、プロトコルに準拠した動作を保証しています。

## ResilientExecutor

すべての信頼性パターンを 1 つのエグゼキューターに統合します：

```python
from ai_lib_python.resilience import (
    ResilientConfig, RetryConfig, RateLimiterConfig,
    CircuitBreakerConfig, BackpressureConfig
)

config = ResilientConfig(
    retry=RetryConfig(
        max_retries=3,
        initial_delay=1.0,
        max_delay=30.0,
        backoff_multiplier=2.0,
    ),
    rate_limiter=RateLimiterConfig(
        requests_per_second=10,
    ),
    circuit_breaker=CircuitBreakerConfig(
        failure_threshold=5,
        cooldown_seconds=30,
    ),
    backpressure=BackpressureConfig(
        max_inflight=50,
    ),
)

client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .resilience(config) \
    .build()
```

## 個別パターン

### サーキットブレーカー

```python
from ai_lib_python.resilience import CircuitBreaker

breaker = CircuitBreaker(
    failure_threshold=5,
    cooldown_seconds=30,
)

# 状態を確認
print(breaker.state)  # "closed"、"open"、"half_open"
```

### レートリミッター

トークンバケットアルゴリズム：

```python
from ai_lib_python.resilience import RateLimiter

limiter = RateLimiter(
    requests_per_second=10,
    burst_size=20,
)
```

### バックプレッシャー

同時実行制限：

```python
from ai_lib_python.resilience import Backpressure

bp = Backpressure(max_inflight=50)
```

### フォールバックチェーン

マルチターゲットフェイルオーバー：

```python
from ai_lib_python.resilience import FallbackChain

chain = FallbackChain([
    "openai/gpt-4o",
    "anthropic/claude-3-5-sonnet",
    "deepseek/deepseek-chat",
])
```

## PreflightChecker

リクエスト実行前の統合ゲート：

```python
from ai_lib_python.resilience import PreflightChecker

checker = PreflightChecker()
# リクエストを許可する前にサーキット状態、レート制限、実行中数をチェック
```

## SignalsSnapshot

集約されたランタイム状態：

```python
signals = client.signals_snapshot()
print(f"Circuit: {signals.circuit_state}")
print(f"Inflight: {signals.current_inflight}")
print(f"Rate remaining: {signals.rate_remaining}")
```

## 環境変数

| 変数 | 目的 |
|------|------|
| `AI_LIB_RPS` | レート制限（1 秒あたりのリクエスト数） |
| `AI_LIB_BREAKER_FAILURE_THRESHOLD` | サーキットブレーカーのしきい値 |
| `AI_LIB_BREAKER_COOLDOWN_SECS` | クールダウン期間 |
| `AI_LIB_MAX_INFLIGHT` | 最大同時リクエスト数 |

## 次のステップ

- **[高度な機能](/python/advanced/)** — テレメトリ、ルーティング、プラグイン
- **[AiClient API](/python/client/)** — クライアントの使い方
