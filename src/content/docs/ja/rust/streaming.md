---
title: ストリーミングパイプライン（Rust）
description: ai-lib-rust v0.7.1 におけるオペレーターベースのストリーミングパイプラインの詳細。
---

# ストリーミングパイプライン

ストリーミングパイプラインは ai-lib-rust の中核です。プロトコル設定によって駆動される構成可能なオペレーターを通じて、プロバイダーのレスポンスを処理します。

## パイプラインアーキテクチャ

```
Raw Bytes → Decoder → Selector → Accumulator → FanOut → EventMapper → StreamingEvent
```

各オペレーターはパイプラインのステージです：

### 1. Decoder

生のバイトストリームを JSON フレームに変換します。

| 形式 | 説明 |
|------|------|
| `sse` | Server-Sent Events（OpenAI、Groq など） |
| `ndjson` | 改行区切り JSON |
| `anthropic_sse` | Anthropic のカスタム SSE 形式 |

デコーダー形式はプロバイダーマニフェストで指定されます：

```yaml
streaming:
  decoder:
    format: "sse"
    done_signal: "[DONE]"
```

### 2. Selector

マニフェストの `event_map` で定義された JSONPath 式を使用して JSON フレームをフィルタリングします：

```yaml
event_map:
  - match: "$.choices[0].delta.content"
    emit: "PartialContentDelta"
```

### 3. Accumulator

部分的なツール呼び出しを状態を持って組み立てます。プロバイダーがツール呼び出し引数をチャンクでストリーミングする場合、アキュムレーターはそれらを完全なツール呼び出しに収集します：

```
PartialToolCall("get_we") → PartialToolCall("ather") → PartialToolCall("(\"Tokyo\")")
```

### 4. FanOut

マルチ候補レスポンス（`n > 1` の場合）を処理します。候補を別々のイベントストリームに展開します。

### 5. EventMapper

最終ステージ — 処理済みフレームを統一 `StreamingEvent` 型に変換します：

- `StreamingEvent::ContentDelta` — テキストコンテンツ
- `StreamingEvent::ToolCallStarted` — ツール呼び出しの開始
- `StreamingEvent::PartialToolCall` — ツール引数チャンク
- `StreamingEvent::StreamEnd` — レスポンス完了

## プロトコル駆動の構築

パイプラインはプロバイダーマニフェストから自動的に構築されます。手動設定は不要です：

```rust
// パイプラインはプロトコルマニフェストに基づいて内部的に構築されます
let mut stream = client.chat()
    .user("Hello")
    .stream()
    .execute_stream()
    .await?;
```

ランタイムはマニフェストの `streaming` セクションを読み、適切なデコーダー、セレクタールール、イベントマッパーを配線します。

## リトライおよびフォールバックオペレーター

パイプラインには耐障害性オペレーターも含まれます：

- **Retry** — マニフェストのリトライポリシーに基づいて失敗したストリームをリトライ
- **Fallback** — 障害時に代替プロバイダー/モデルにフォールバック

## 次のステップ

- **[耐障害性](/rust/resilience/)** — サーキットブレーカー、レートリミッター
- **[高度な機能](/rust/advanced/)** — 埋め込み、キャッシュ、バッチ
