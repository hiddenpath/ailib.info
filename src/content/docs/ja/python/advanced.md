---
title: 高度な機能（Python）
description: ai-lib-python v0.7.0 におけるテレメトリ、モデルルーティング、埋め込み、キャッシュ、プラグイン、構造化出力。
---

# 高度な機能

## 機能 Extra

pip extra 経由でオプション機能をインストール（v0.7.0+）：

| Extra | 目的 |
|-------|------|
| `vision` | 画像処理（Pillow） |
| `audio` | オーディオ処理（soundfile） |
| `embeddings` | 埋め込み生成 |
| `structured` | 構造化出力 / JSON モード |
| `batch` | バッチ処理 |
| `agentic` | エージェントワークフローサポート |
| `telemetry` | OpenTelemetry 統合 |
| `tokenizer` | トークンカウント（tiktoken） |
| `full` | すべての機能 + watchdog + keyring |

```bash
pip install ai-lib-python[full]   # すべての機能
pip install ai-lib-python[vision,embeddings]   # 選択した extra
```

## V2 エラーコード

`errors/standard_codes.py` の `StandardErrorCode` 型は、プロトコルに準拠したエラー分類を提供します：

- **13 の frozen dataclass コード** — E1001–E9999 範囲
- **`from_http_status(status_code)`** — HTTP ステータスコードを標準コードにマッピング
- **`from_name(name)`** — 文字列名でコードを検索
- **分類パイプライン** — 耐障害性の判断（リトライ、フォールバックチェーン）に `retryable` と `fallbackable` プロパティを使用

```python
from ai_lib_python.errors.standard_codes import StandardErrorCode

code = StandardErrorCode.from_http_status(429)
print(code.retryable)   # True
print(code.fallbackable)  # True
```

## 本番テレメトリ

### メトリクス（Prometheus）

```python
from ai_lib_python.telemetry import MetricsCollector

metrics = MetricsCollector()

# リクエスト数、レイテンシ、トークン使用量、エラーを自動追跡
client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .metrics(metrics) \
    .build()

# Prometheus にエクスポート
metrics.export_prometheus()  # Prometheus テキスト形式を返す
```

### 分散トレーシング（OpenTelemetry）

```python
from ai_lib_python.telemetry import Tracer

tracer = Tracer(service_name="my-app")

# トレースはリクエストライフサイクル全体に伝播
client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .tracer(tracer) \
    .build()
```

### ヘルス監視

```python
from ai_lib_python.telemetry import HealthChecker

health = HealthChecker()
status = await health.check()
print(f"Healthy: {status.is_healthy}")
```

## モデルルーティング

複数のプロバイダーにわたるインテリジェントなモデル選択：

```python
from ai_lib_python.routing import ModelManager, ModelInfo

manager = ModelManager()

# モデルを登録
manager.register(ModelInfo(
    model_id="openai/gpt-4o",
    weight=0.7,
    capabilities=["chat", "tools", "vision"],
))
manager.register(ModelInfo(
    model_id="anthropic/claude-3-5-sonnet",
    weight=0.3,
    capabilities=["chat", "tools", "reasoning"],
))

# 戦略に基づいて選択
model = manager.select(strategy="weighted")
```

### 事前設定カタログ

```python
from ai_lib_python.routing import create_openai_models, create_anthropic_models

openai_models = create_openai_models()
anthropic_models = create_anthropic_models()
```

### 選択戦略

| 戦略 | 説明 |
|------|------|
| `round_robin` | モデルをローテーション |
| `weighted` | 確率ベースの選択 |
| `cost_based` | より安いモデルを優先 |
| `quality_based` | より高品質なモデルを優先 |
| `latency_based` | より速いモデルを優先 |

## 埋め込み

```python
from ai_lib_python.embeddings import EmbeddingClient

client = EmbeddingClient(model="openai/text-embedding-3-small")

embeddings = await client.embed([
    "Python programming",
    "Machine learning",
    "Cooking recipes",
])

from ai_lib_python.embeddings.vectors import cosine_similarity
sim = cosine_similarity(embeddings[0], embeddings[1])
print(f"Similarity: {sim:.3f}")
```

## レスポンスキャッシュ

```python
from ai_lib_python.cache import CacheManager, MemoryCache, DiskCache

# メモリキャッシュ
cache = CacheManager(backend=MemoryCache(), ttl=3600)

# ディスクキャッシュ
cache = CacheManager(backend=DiskCache("./cache"), ttl=86400)

client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .cache(cache) \
    .build()
```

## トークンカウント

```python
from ai_lib_python.tokens import TokenCounter

counter = TokenCounter.for_model("gpt-4o")
count = counter.count("Hello, how are you?")

# コスト見積もり
from ai_lib_python.tokens import CostEstimator
estimator = CostEstimator.for_model("openai/gpt-4o")
cost = estimator.estimate(prompt_tokens=100, completion_tokens=50)
```

## バッチ処理

```python
from ai_lib_python.batch import BatchCollector, BatchExecutor

collector = BatchCollector()
collector.add(client.chat().user("Question 1"))
collector.add(client.chat().user("Question 2"))
collector.add(client.chat().user("Question 3"))

executor = BatchExecutor(concurrency=5, timeout=30)
results = await executor.execute(collector)
```

## プラグインシステム

```python
from ai_lib_python.plugins import Plugin, PluginRegistry

class LoggingPlugin(Plugin):
    def name(self) -> str:
        return "logging"

    async def on_request(self, request):
        print(f"→ {request.model}")

    async def on_response(self, response):
        print(f"← {response.usage.total_tokens} tokens")

registry = PluginRegistry()
registry.register(LoggingPlugin())
```

## 構造化出力

```python
from ai_lib_python.structured import JsonMode, SchemaGenerator

# JSON モード
response = await client.chat() \
    .user("List 3 countries as JSON") \
    .response_format(JsonMode()) \
    .execute()

# Pydantic スキーマ付き
from pydantic import BaseModel

class Country(BaseModel):
    name: str
    capital: str

schema = SchemaGenerator.from_model(Country)
```

## ガードレール

```python
from ai_lib_python.guardrails import ContentFilter, PiiDetector

filter = ContentFilter(blocked_keywords=["unsafe"])
pii = PiiDetector()
```
