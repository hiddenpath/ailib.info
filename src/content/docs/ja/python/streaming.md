---
title: ストリーミングパイプライン（Python）
description: ai-lib-python v0.6.0 におけるストリーミングパイプラインの仕組み — デコーダー、セレクター、アキュムレーター、イベントマッパー。
---

# ストリーミングパイプライン

Python SDK は、Python の非同期エコシステムに適応した、Rust ランタイムと同じオペレーターベースのパイプラインアーキテクチャを実装しています。

## パイプラインステージ

```
Raw Bytes → Decoder → Selector → Accumulator → FanOut → EventMapper → StreamingEvent
```

### 1. Decoder

HTTP レスポンスバイトを JSON フレームに変換します：

| デコーダークラス | プロバイダー形式 |
|------------------|------------------|
| `SseDecoder` | 標準 SSE（OpenAI、Groq など） |
| `JsonLinesDecoder` | 改行区切り JSON |
| `AnthropicSseDecoder` | Anthropic のカスタム SSE |

デコーダーはマニフェストの `streaming.decoder.format` に基づいて選択されます。

### 2. Selector

マニフェストの JSONPath 式を使用して JSON フレームをフィルタリングします：

```python
# 内部的に、パイプラインはマニフェストルールからセレクターを作成します：
# match: "$.choices[0].delta.content" → emit: "PartialContentDelta"
```

JSONPath 式の評価に `jsonpath-ng` を使用します。

### 3. Accumulator

部分的なツール呼び出しを完全な呼び出しに組み立てます：

```python
# プロバイダーのストリーム：
#   {"tool_calls": [{"index": 0, "function": {"arguments": '{"ci'}}]}
#   {"tool_calls": [{"index": 0, "function": {"arguments": 'ty":"T'}}]}
#   {"tool_calls": [{"index": 0, "function": {"arguments": 'okyo"}'}}]}
# アキュムレーターが完全な {"city": "Tokyo"} を生成
```

### 4. FanOut

マルチ候補レスポンス（`n > 1`）の場合、候補ごとのストリームに展開します。

### 5. EventMapper

3 つのマッパー実装：

| マッパー | 説明 |
|----------|------|
| `ProtocolEventMapper` | マニフェストの event_map ルール（JSONPath → イベント型）を使用 |
| `DefaultEventMapper` | OpenAI 互換プロバイダー用フォールバック |
| `AnthropicEventMapper` | Anthropic の独自イベント構造を処理 |

## 非同期イテレーション

パイプラインはイベントを非同期イテレーターとして公開します：

```python
async for event in client.chat().user("Hello").stream():
    if event.is_content_delta:
        text = event.as_content_delta.text
        print(text, end="")
    elif event.is_tool_call_started:
        call = event.as_tool_call_started
        print(f"\nTool: {call.name}")
    elif event.is_stream_end:
        end = event.as_stream_end
        print(f"\nFinish: {end.finish_reason}")
```

## キャンセル

ストリームはグラースフルなキャンセルをサポートします：

```python
from ai_lib_python import CancelToken

token = CancelToken()

async for event in client.chat().user("...").stream(cancel_token=token):
    # 十分なコンテンツを受信したらキャンセル
    if total_chars > 1000:
        token.cancel()
        break
```

## 次のステップ

- **[耐障害性](/python/resilience/)** — 信頼性パターン
- **[高度な機能](/python/advanced/)** — テレメトリ、ルーティング、プラグイン
