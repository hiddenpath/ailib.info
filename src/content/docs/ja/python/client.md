---
title: AiClient API（Python）
description: ai-lib-python における AiClient、ChatRequestBuilder、レスポンス型の詳細ガイド。
---

# AiClient API

## クライアントの作成

### モデル識別子から

```python
from ai_lib_python import AiClient

client = await AiClient.create("anthropic/claude-3-5-sonnet")
```

### ビルダーを使用

```python
client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .protocol_dir("./ai-protocol") \
    .timeout(60) \
    .build()
```

### 耐障害性付き

```python
from ai_lib_python.resilience import ResilientConfig

config = ResilientConfig(
    max_retries=3,
    rate_limit_rps=10,
    circuit_breaker_threshold=5,
    max_inflight=50,
)

client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .resilience(config) \
    .build()
```

## ChatRequestBuilder

リクエスト構築のための fluent API：

```python
response = await client.chat() \
    .system("You are a helpful assistant") \
    .user("Hello!") \
    .messages([Message.user("Follow-up")]) \
    .temperature(0.7) \
    .max_tokens(1000) \
    .top_p(0.9) \
    .tools([tool_definition]) \
    .execute()
```

## レスポンス型

### ChatResponse

```python
class ChatResponse:
    content: str              # レスポンステキスト
    tool_calls: list[ToolCall]  # 関数呼び出し
    finish_reason: str        # 完了理由
    usage: Usage              # トークン数
```

### StreamingEvent

```python
class StreamingEvent:
    # 型チェック
    is_content_delta: bool
    is_tool_call_started: bool
    is_partial_tool_call: bool
    is_stream_end: bool

    # 型安全アクセサー
    as_content_delta -> ContentDelta
    as_tool_call_started -> ToolCallStarted
    as_partial_tool_call -> PartialToolCall
    as_stream_end -> StreamEnd
```

### CallStats

```python
class CallStats:
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    model: str
    provider: str
```

## 実行モード

### 非ストリーミング

```python
# シンプルなレスポンス
response = await client.chat().user("Hello").execute()

# 統計付き
response, stats = await client.chat().user("Hello").execute_with_stats()
```

### ストリーミング

```python
async for event in client.chat().user("Hello").stream():
    if event.is_content_delta:
        print(event.as_content_delta.text, end="")
```

### キャンセル可能なストリーム

```python
from ai_lib_python import CancelToken

token = CancelToken()

async for event in client.chat().user("Long task...").stream(cancel_token=token):
    if event.is_content_delta:
        print(event.as_content_delta.text, end="")
    if should_cancel:
        token.cancel()
        break
```

## エラーハンドリング

すべてのエラーは `standard_code` プロパティで V2 標準エラーコードを公開します（ai-lib-python v0.6.0+）：

```python
from ai_lib_python.errors import (
    AiLibError, ProtocolError, TransportError, RemoteError
)

try:
    response = await client.chat().user("Hello").execute()
except RemoteError as e:
    print(f"Provider error: {e.error_type}")  # 標準エラークラス
    print(f"Standard code: {e.standard_code}")  # V2 StandardErrorCode（例：E1001）
    print(f"HTTP status: {e.status_code}")
except TransportError as e:
    print(f"Network error: {e}")
except ProtocolError as e:
    print(f"Protocol error: {e}")
except AiLibError as e:
    print(f"Other error: {e}")
```

## 次のステップ

- **[ストリーミングパイプライン](/python/streaming/)** — パイプラインの内部
- **[耐障害性](/python/resilience/)** — 信頼性パターン
- **[高度な機能](/python/advanced/)** — テレメトリ、ルーティング、プラグイン
