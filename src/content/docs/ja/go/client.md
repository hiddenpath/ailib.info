---
title: AiClient (Go)
description: Go の AiClient インターフェースのリファレンス。
---

# AiClient

`AiClient` は `ai-lib-go` を使用するための主要なエントリポイントです。基礎となる `net/http` クライアント、マニフェストの解析、エラーマッピング、およびストリーミングパイプラインを管理します。

## 構成

```go
aiClient, err := client.NewAiClient(ctx, providerName, options)
```

- `providerName`: プロバイダーマニフェストの正確な名前（例: `openai`, `anthropic`, `gemini`）。
- `options`: カスタムマニフェストパス、HTTP クライアントのオーバーライド、または明示的な API キーなどのオプション引数（ただし、環境変数が推奨されます）。

## コンテキストの統合

他のランタイムとは異なり、Go SDK は耐障害性とライフサイクル管理のために `context.Context` を強力に活用します：

```go
ctx, cancel := context.WithTimeout(context.Background(), 10 * time.Second)
defer cancel()

// HTTP リクエストまたはストリームが 10 秒以上かかる場合、自動的にキャンセルされます。
stream, err := aiClient.Chat().Model("gpt-4o").User("5 つの色をリストしてください").ExecuteStream(ctx)
```

## サポートされているエンドポイント

現在、`Chat()` と `Embeddings()` ビルダーが利用可能です。マルチモーダル、MCP、および Computer Use のサポートは、`v0.6.0` リリースに向けて計画されています。
