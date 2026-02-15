---
title: 仕様詳細
description: AI-Protocol コア仕様の詳細 — 標準パラメータ、イベント、エラークラス、リトライポリシー。
---

# コア仕様

コア仕様（`v1/spec.yaml`）は、すべてのプロバイダーマニフェストとランタイムが共有する標準語彙を定義します。

## 標準パラメータ

これらのパラメータはすべてのプロバイダーで一貫した意味を持ちます：

| パラメータ | 型 | 説明 |
|------------|------|------|
| `temperature` | float | ランダム性の制御（0.0 – 2.0） |
| `max_tokens` | integer | 最大レスポンストークン数 |
| `top_p` | float | ヌクレアスサンプリングしきい値 |
| `stream` | boolean | ストリーミングレスポンスを有効化 |
| `stop` | string[] | 停止シーケンス |
| `tools` | object[] | ツール/関数定義 |
| `tool_choice` | string/object | ツール選択モード |
| `response_format` | object | 構造化出力形式 |

プロバイダーマニフェストはこれらの標準名をプロバイダー固有のパラメータ名にマッピングします。例えば、OpenAI は `max_completion_tokens` を使用し、Anthropic は `max_tokens` を使用します。

## ストリーミングイベント

仕様はランタイムが発行する統一ストリーミングイベント型を定義します：

| イベント | 説明 |
|----------|------|
| `PartialContentDelta` | テキストコンテンツフラグメント |
| `ThinkingDelta` | 推論/思考ブロック（拡張思考モデル） |
| `ToolCallStarted` | 関数/ツール呼び出しの開始 |
| `PartialToolCall` | ツール呼び出し引数のストリーミング |
| `ToolCallEnded` | ツール呼び出しの完了 |
| `StreamEnd` | レスポンスストリームの完了 |
| `StreamError` | ストリームレベルのエラー |
| `Metadata` | 使用統計、モデル情報 |

プロバイダーマニフェストは、プロバイダー固有のイベントをこれらの標準型にマッピングする JSONPath ベースのルールを宣言します。

## エラークラス（V2 標準コード）

V2 では 13 の標準化されたエラーコードを定義しています。プロバイダー固有のエラーは、ランタイム間で一貫したハンドリングのためにこれらのコードにマッピングされます：

| コード | 名前 | カテゴリ | リトライ可能 | フォールバック可能 |
|-------|------|----------|--------------|-------------------|
| E1001 | `invalid_request` | Client | No | No |
| E1002 | `authentication` | Client | No | Yes |
| E1003 | `permission_denied` | Client | No | No |
| E1004 | `not_found` | Client | No | No |
| E1005 | `request_too_large` | Client | No | No |
| E2001 | `rate_limited` | Rate | Yes | Yes |
| E2002 | `quota_exhausted` | Rate | No | Yes |
| E3001 | `server_error` | Server | Yes | Yes |
| E3002 | `overloaded` | Server | Yes | Yes |
| E3003 | `timeout` | Server | Yes | Yes |
| E4001 | `conflict` | Operational | Yes | No |
| E4002 | `cancelled` | Operational | No | No |
| E9999 | `unknown` | Unknown | No | No |

- **リトライ可能** — 一時的な障害に対してランタイムがリクエストをリトライできます（バックオフ付き）
- **フォールバック可能** — ランタイムがフォールバックチェーンで代替プロバイダーまたはモデルを試行できます

## リトライポリシー

仕様は標準リトライ戦略を定義します：

```yaml
retry_policy:
  strategy: "exponential_backoff"
  max_retries: 3
  initial_delay_ms: 1000
  max_delay_ms: 30000
  backoff_multiplier: 2.0
  retryable_errors:
    - "rate_limited"
    - "overloaded"
    - "server_error"
    - "timeout"
```

## 終了理由

レスポンス完了の正規化された終了理由：

| 理由 | 説明 |
|------|------|
| `end_turn` | 自然な完了 |
| `max_tokens` | トークン制限に到達 |
| `tool_use` | モデルがツールを呼び出そうとしている |
| `stop_sequence` | 停止シーケンスに遭遇 |
| `content_filter` | コンテンツポリシーでフィルタリングされた |

## API ファミリ

プロバイダーはリクエスト/レスポンス形式の混乱を防ぐために API ファミリに分類されます：

- `openai` — OpenAI 互換 API（Groq、Together、DeepSeek なども使用）
- `anthropic` — Anthropic Messages API
- `gemini` — Google Gemini API
- `custom` — プロバイダー固有の形式

## 次のステップ

- **[プロバイダーマニフェスト](/protocol/providers/)** — プロバイダー設定の仕組み
- **[モデルレジストリ](/protocol/models/)** — モデル設定の詳細
