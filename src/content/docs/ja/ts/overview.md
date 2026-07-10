---
title: TypeScript SDK 概要
description: ai-lib-ts v1.0.0 のアーキテクチャと公開 API — AI-Protocol の TypeScript ランタイム。
---

# TypeScript SDK 概要

**ai-lib-ts**（v1.0.0）は [AI-Protocol](https://github.com/ailib-official/ai-protocol) の TypeScript / Node.js ランタイムです。npm パッケージ `@ailib-official/ai-lib-ts` として公開され、3 つのエントリポイントを提供します。

| インポート | レイヤー | 用途 |
|--------|-------|----------|
| `@ailib-official/ai-lib-ts` | E + P ファサード | フル SDK（デフォルト） |
| `@ailib-official/ai-lib-ts/core` | 実行層のみ | 最小バンドル — ポリシー層の transport ラッパーなし |
| `@ailib-official/ai-lib-ts/contact` | ポリシー層のみ | レジリエンス、ルーティング — `AiClient` なし |

## 主な実行パス

チャットでは、**`AiClient` は低レベルな `Pipeline` 演算子 API を使いません**。流れは次のとおりです。

1. プロバイダーマニフェストを読み込む
2. マニフェストのフィールドから HTTP リクエストを構築する
3. **`HttpTransport`** 経由で送信する
4. マニフェストの `response_paths` と OpenAI スタイルのフォールバックで JSON / SSE を解析する

`Pipeline` はコンプライアンステストと高度な統合向けに公開されたままです。このランタイムに **`ProviderDriver` はありません**。

## 公開 API の概観

**パッケージルートのエクスポート:**

- `AiClient`、`AiClientBuilder`、`createClient`、`createClientBuilder`
- `Message`、`StreamingEvent`、`Tool`、実行メタデータ型
- `ProtocolLoader`、マニフェスト + V2 型
- ポリシー: `RetryPolicy`、`CircuitBreaker`、`RateLimiter`、`ModelManager`、`FallbackChain`、…
- 追加機能: `EmbeddingClient`、`McpToolBridge`、`Guardrails`、テレメトリヘルパー

### 能力境界（正直な記述）

| 領域 | パッケージに含まれるもの | 含まれないもの |
|------|----------------|--------------|
| **MCP** | `McpToolBridge` による形式変換 | `AiClient` 内の MCP サーバートランスポート |
| **Computer Use** | V2 設定型 | ランタイム実行環境 |
| **ホットリロード** | — | 未実装 |
| **レジリエンス** | デフォルト transport 上のマニフェスト再試行 | CB / レート制限 / 背圧は transport に明示設定が必要 |
| **Embeddings** | `EmbeddingClient` | マニフェスト Pipeline パスではない |

## 次のステップ

- [クイックスタート](/ja/ts/quickstart/)
- [ストリーミング](/ja/ts/streaming/)
- [レジリエンス](/ja/ts/resilience/)
