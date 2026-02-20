---
title: AiClient API（Rust）
description: ai-lib-rust v0.8.0 における AiClient、ChatRequestBuilder、レスポンス型の詳細ガイド。
---

# AiClient API

## クライアントの作成

### モデル識別子から

```rust
// プロトコルは自動的に読み込まれます
let client = AiClient::new("anthropic/claude-3-5-sonnet").await?;
```

### ビルダーを使用

```rust
let client = AiClient::builder()
    .model("openai/gpt-4o")
    .protocol_dir("./ai-protocol")
    .timeout(Duration::from_secs(60))
    .build()
    .await?;
```

## ChatRequestBuilder

ビルダーパターンにより fluent API を提供します：

```rust
let response = client.chat()
    // メッセージ
    .system("You are a helpful assistant")
    .user("Hello!")
    .messages(vec![Message::user("Follow-up")])

    // パラメータ
    .temperature(0.7)
    .max_tokens(1000)
    .top_p(0.9)
    .stop(vec!["END".into()])

    // ツール
    .tools(vec![weather_tool])
    .tool_choice("auto")

    // 実行
    .execute()
    .await?;
```

## レスポンス型

### ChatResponse

```rust
pub struct ChatResponse {
    pub content: String,         // レスポンステキスト
    pub tool_calls: Vec<ToolCall>, // 関数呼び出し（ある場合）
    pub finish_reason: String,    // レスポンス終了の理由
    pub usage: Usage,             // トークン使用量
}
```

### StreamingEvent

```rust
pub enum StreamingEvent {
    ContentDelta { text: String, index: usize },
    ThinkingDelta { text: String },
    ToolCallStarted { id: String, name: String, index: usize },
    PartialToolCall { id: String, arguments: String, index: usize },
    ToolCallEnded { id: String, index: usize },
    StreamEnd { finish_reason: Option<String>, usage: Option<Usage> },
    Metadata { model: Option<String>, usage: Option<Usage> },
}
```

### CallStats

```rust
pub struct CallStats {
    pub total_tokens: u32,
    pub prompt_tokens: u32,
    pub completion_tokens: u32,
    pub latency_ms: u64,
    pub model: String,
    pub provider: String,
}
```

## 実行モード

### 非ストリーミング

```rust
// シンプルなレスポンス
let response = client.chat().user("Hello").execute().await?;

// 統計付きレスポンス
let (response, stats) = client.chat().user("Hello").execute_with_stats().await?;
```

### ストリーミング

```rust
let mut stream = client.chat()
    .user("Hello")
    .stream()
    .execute_stream()
    .await?;

while let Some(event) = stream.next().await {
    // 各 StreamingEvent を処理
}
```

### ストリームキャンセル

```rust
let (mut stream, cancel_handle) = client.chat()
    .user("Long task...")
    .stream()
    .execute_stream_cancellable()
    .await?;

// 別タスクからキャンセル
tokio::spawn(async move {
    tokio::time::sleep(Duration::from_secs(5)).await;
    cancel_handle.cancel();
});
```

## エラーハンドリング

```rust
use ai_lib_rust::{Error, ErrorContext};

match client.chat().user("Hello").execute().await {
    Ok(response) => println!("{}", response.content),
    Err(Error::Protocol(e)) => eprintln!("Protocol error: {e}"),
    Err(Error::Transport(e)) => eprintln!("HTTP error: {e}"),
    Err(Error::Remote(e)) => {
        eprintln!("Provider error: {}", e.error_type);
        // e.error_type は 13 の標準エラークラスのいずれか
    }
    Err(e) => eprintln!("Other error: {e}"),
}
```

すべてのエラーは `ErrorContext` 経由で V2 標準エラーコードを保持します。プログラムによる処理には `error.context().standard_code` で `StandardErrorCode` enum（E1001–E9999）にアクセスしてください。

## バッチ操作

複数のチャットリクエストを並列実行します：

```rust
// Execute multiple chat requests in parallel
let results = client.chat_batch(requests, 5).await; // concurrency limit = 5

// Smart batching with automatic concurrency tuning
let results = client.chat_batch_smart(requests).await;
```

## リクエスト検証

送信前にプロトコルマニフェストに対してリクエストを検証します：

```rust
// Validate a request against the protocol manifest before sending
client.validate_request(&request)?;
```

## フィードバックと可観測性

RLHF やモニタリング用のフィードバックイベントを報告し、耐障害性の状態を確認します：

```rust
// Report feedback events for RLHF / monitoring
client.report_feedback(FeedbackEvent::Rating(RatingFeedback {
    request_id: "req-123".into(),
    rating: 5,
    max_rating: 5,
    category: None,
    comment: Some("Great response".into()),
    timestamp: chrono::Utc::now(),
})).await?;

// Get current resilience state
let signals = client.signals().await;
println!("Circuit: {:?}", signals.circuit_breaker);
```

## ビルダー設定

高度な設定には `AiClientBuilder` を使用します：

```rust
let client = AiClientBuilder::new()
    .protocol_path("path/to/protocols".into())
    .hot_reload(true)
    .with_fallbacks(vec!["openai/gpt-4o".into()])
    .feedback_sink(my_sink)
    .max_inflight(10)
    .circuit_breaker_default()
    .rate_limit_rps(5.0)
    .base_url_override("https://my-proxy.example.com")
    .build("anthropic/claude-3-5-sonnet")
    .await?;
```

## 次のステップ

- **[ストリーミングパイプライン](/rust/streaming/)** — パイプラインがストリームを処理する方法
- **[耐障害性](/rust/resilience/)** — 信頼性パターン
- **[高度な機能](/rust/advanced/)** — 埋め込み、キャッシュ、プラグイン
