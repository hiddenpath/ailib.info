---
title: 推論モデル
description: AI-Lib で拡張思考・推論モデルを使用する方法です。
---

# 推論モデル

一部の AI モデルは拡張思考（チェーン・オブ・ソート推論）に対応しており、最終回答の前に推論プロセスを表示します。

## 対応モデル

| Model | Provider | Reasoning |
|-------|----------|-----------|
| o1, o1-mini, o3 | OpenAI | Extended thinking |
| Claude 3.5 Sonnet | Anthropic | Extended thinking |
| DeepSeek R1 | DeepSeek | Chain-of-thought |
| Gemini 2.0 Flash Thinking | Google | Thinking mode |

## 使用方法

推論モデルは同じ API で動作します。主な違いは、ストリーミング中に `ThinkingDelta` イベントを出力する場合があることです。

### Rust

```rust
let mut stream = client.chat()
    .user("Solve this step by step: What is 127 * 43?")
    .stream()
    .execute_stream()
    .await?;

while let Some(event) = stream.next().await {
    match event? {
        StreamingEvent::ThinkingDelta { text, .. } => {
            // Model's reasoning process
            print!("[thinking] {text}");
        }
        StreamingEvent::ContentDelta { text, .. } => {
            // Final answer
            print!("{text}");
        }
        _ => {}
    }
}
```

### Python

```python
async for event in client.chat() \
    .user("Solve this step by step: What is 127 * 43?") \
    .stream():
    if event.is_thinking_delta:
        print(f"[thinking] {event.text}", end="")
    elif event.is_content_delta:
        print(event.as_content_delta.text, end="")
```

## 仕組み

1. プロバイダーマニフェストで `capabilities.reasoning: true` が宣言されます
2. ストリーミングデコーダーが推論専用イベントを認識します
3. EventMapper が推論コンテンツに対して `ThinkingDelta` を出力します
4. `ContentDelta` イベントに最終回答が含まれます

プロトコルマニフェストがプロバイダー固有のフォーマットの違いを処理します：

- **OpenAI o1**: 内部推論トークンを使用します
- **Anthropic Claude**: `thinking` コンテンツブロックを使用します
- **DeepSeek R1**: コンテンツ内の `<think>` タグを使用します

## ヒント

- 推論モデルは複雑なタスクで一般に良好な結果を生成します
- より多くのトークンを使用します（推論トークンもカウントされます）
- Temperature が制限される場合があります（一部の推論モデルは無視します）
- すべてのプロバイダーが推論に対応しているわけではありません — `capabilities.reasoning` を確認してください
