---
title: クイックスタート
description: 5 分以内に AI-Lib を始める — Rust または Python を選択してください。
---

# クイックスタート

ランタイムを選んで、数分で AI 呼び出しを開始しましょう。

## 前提条件

- サポート対象のプロバイダーの API キー（例：`OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、`DEEPSEEK_API_KEY`）
- AI-Protocol リポジトリ（ローカルにない場合は GitHub から自動取得されます）

## Rust

### 1. 依存関係を追加する

```toml
[dependencies]
ai-lib = "0.7"
tokio = { version = "1", features = ["full"] }
```

### 2. API キーを設定する

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 3. 最初のプログラムを書く

```rust
use ai_lib::{AiClient, StreamingEvent};
use futures::StreamExt;

#[tokio::main]
async fn main() -> ai_lib::Result<()> {
    // クライアントを作成 — プロトコルマニフェストは自動的に読み込まれます
    let client = AiClient::from_model("anthropic/claude-3-5-sonnet").await?;

    // ストリーミングチャット
    let mut stream = client.chat()
        .user("What is AI-Protocol?")
        .temperature(0.7)
        .max_tokens(500)
        .stream()
        .execute_stream()
        .await?;

    while let Some(event) = stream.next().await {
        match event? {
            StreamingEvent::ContentDelta { text, .. } => print!("{text}"),
            StreamingEvent::StreamEnd { .. } => println!(),
            _ => {}
        }
    }
    Ok(())
}
```

### 4. 実行する

```bash
cargo run
```

## Python

### 1. パッケージをインストールする

```bash
pip install ai-lib-python>=0.6.0
```

### 2. API キーを設定する

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 3. 最初のスクリプトを書く

```python
import asyncio
from ai_lib_python import AiClient

async def main():
    # クライアントを作成 — プロトコルマニフェストは自動的に読み込まれます
    client = await AiClient.create("anthropic/claude-3-5-sonnet")

    # ストリーミングチャット
    async for event in client.chat() \
        .user("What is AI-Protocol?") \
        .temperature(0.7) \
        .max_tokens(500) \
        .stream():
        if event.is_content_delta:
            print(event.as_content_delta.text, end="")
    print()

asyncio.run(main())
```

### 4. 実行する

```bash
python main.py
```

## プロバイダーの切り替え

AI-Lib の醍醐味：1 つの文字列を変更するだけでプロバイダーを切り替えられます。

```rust
// Rust — モデル ID を変更するだけ
let client = AiClient::from_model("openai/gpt-4o").await?;
let client = AiClient::from_model("deepseek/deepseek-chat").await?;
let client = AiClient::from_model("gemini/gemini-2.0-flash").await?;
```

```python
# Python — 同じこと
client = await AiClient.create("openai/gpt-4o")
client = await AiClient.create("deepseek/deepseek-chat")
client = await AiClient.create("gemini/gemini-2.0-flash")
```

コード変更は不要です。プロトコルマニフェストが各プロバイダーのエンドポイント、認証、パラメータマッピング、ストリーミング形式を処理します。

## 次のステップ

- **[エコシステムアーキテクチャ](/ecosystem/)** — 構成要素の関係
- **[チャット補完ガイド](/guides/chat/)** — チャット API の詳細な使い方
- **[Function Calling](/guides/tools/)** — ツール使用と function calling
- **[Rust SDK 詳細](/rust/overview/)** — Rust の詳細
- **[Python SDK 詳細](/python/overview/)** — Python の詳細
