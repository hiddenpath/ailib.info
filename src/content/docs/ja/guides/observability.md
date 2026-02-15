---
title: オブザーバビリティ
description: AI-Lib ランタイムでの監視、メトリクス、ログ、トレーシング。
---

# オブザーバビリティ

両ランタイムは本番デプロイメント向けのオブザーバビリティ機能を提供します。

## Rust：構造化ログ

ai-lib-rust は `tracing` エコシステムを使用します：

```rust
use tracing_subscriber;

// ログを有効化
tracing_subscriber::init();

// すべての AI-Lib 操作が構造化ログイベントを発行
let client = AiClient::new("openai/gpt-4o").await?;
```

ログレベル：
- `INFO` — リクエスト/レスポンスサマリー
- `DEBUG` — プロトコル読み込み、パイプラインステージ
- `TRACE` — 個々のフレーム、JSONPath マッチ

## Rust：呼び出し統計

すべてのリクエストが使用統計を返します：

```rust
let (response, stats) = client.chat()
    .user("Hello")
    .execute_with_stats()
    .await?;

println!("Model: {}", stats.model);
println!("Provider: {}", stats.provider);
println!("Prompt tokens: {}", stats.prompt_tokens);
println!("Completion tokens: {}", stats.completion_tokens);
println!("Total tokens: {}", stats.total_tokens);
println!("Latency: {}ms", stats.latency_ms);
```

## Python：メトリクス（Prometheus）

```python
from ai_lib_python.telemetry import MetricsCollector

metrics = MetricsCollector()

client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .metrics(metrics) \
    .build()

# いくつかのリクエストの後...
prometheus_text = metrics.export_prometheus()
```

追跡されるメトリクス：
- `ai_lib_requests_total` — モデル/プロバイダー別リクエスト数
- `ai_lib_request_duration_seconds` — レイテンシヒストグラム
- `ai_lib_tokens_total` — タイプ別トークン使用量
- `ai_lib_errors_total` — タイプ別エラー数

## Python：分散トレーシング（OpenTelemetry）

```python
from ai_lib_python.telemetry import Tracer

tracer = Tracer(
    service_name="my-app",
    endpoint="http://jaeger:4317",
)

client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .tracer(tracer) \
    .build()
```

トレースには以下のスパンが含まれます：
- プロトコル読み込み
- リクエストコンパイル
- HTTP トランスポート
- パイプライン処理
- イベントマッピング

## Python：ヘルス監視

```python
from ai_lib_python.telemetry import HealthChecker

health = HealthChecker()
status = await health.check()

print(f"Healthy: {status.is_healthy}")
print(f"Details: {status.details}")
```

## Python：ユーザーフィードバック

AI レスポンスへのフィードバックを収集します：

```python
from ai_lib_python.telemetry import FeedbackCollector

feedback = FeedbackCollector()

# レスポンスを取得した後
feedback.record(
    request_id=stats.request_id,
    rating=5,
    comment="Helpful response",
)
```

## 耐障害性のオブザーバビリティ

サーキットブレーカーとレートリミッターの状態を監視します：

```rust
// Rust
let state = client.circuit_state(); // Closed, Open, HalfOpen
let inflight = client.current_inflight();
```

```python
# Python
signals = client.signals_snapshot()
print(f"Circuit: {signals.circuit_state}")
print(f"Inflight: {signals.current_inflight}")
```
