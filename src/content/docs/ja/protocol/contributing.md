---
title: プロバイダーへの貢献
description: AI-Protocol 仕様に新しい AI プロバイダーを追加するためのステップバイステップガイド。
---

# プロバイダーの貢献

AI-Protocol に新しい AI プロバイダーを追加すると、すべてのランタイム（Rust、Python、および将来の実装）で即座に利用可能になります。

## ステップ

> **V2-alpha 形式**：プロトコル v0.7.0 リリースでは、Ring 1/2/3 マニフェスト構造を持つ v2-alpha プロバイダー形式を導入しています。新規プロバイダーは、標準化されたエラーコード、フィーチャーフラグ、機能拡張のために v2-alpha をオプションで対象にできます。V2 アーキテクチャの詳細は [プロトコル概要](/protocol/overview/) をご覧ください。

### 1. プロバイダー API を調査する

プロバイダーについて以下を文書化します：

- ベース URL とチャットエンドポイントパス
- 認証方法（Bearer トークン、API キーヘッダーなど）
- リクエストパラメータ形式
- ストリーミングレスポンス形式（SSE、NDJSON、カスタム）
- エラーレスポンス構造
- 利用可能なモデルとその機能

### 2. プロバイダーマニフェストを作成する

`v1/providers/<provider-id>.yaml` を作成します：

```yaml
id: <provider-id>
name: "<Provider Name>"
protocol_version: "1.5"

endpoint:
  base_url: "https://api.example.com/v1"
  chat_path: "/chat/completions"

auth:
  type: bearer
  token_env: "<PROVIDER_ID>_API_KEY"

parameter_mappings:
  temperature: "temperature"
  max_tokens: "max_tokens"
  stream: "stream"
  tools: "tools"

streaming:
  decoder:
    format: "sse"
    done_signal: "[DONE]"
  event_map:
    - match: "$.choices[0].delta.content"
      emit: "PartialContentDelta"
      extract:
        content: "$.choices[0].delta.content"

error_classification:
  by_http_status:
    "401": "authentication"
    "429": "rate_limited"
    "500": "server_error"

capabilities:
  streaming: true
  tools: true
  vision: false
```

### 3. モデルを追加する

`v1/models/<family>.yaml` を作成または更新します：

```yaml
models:
  example-model:
    provider: <provider-id>
    model_id: "example-model-v1"
    context_window: 128000
    capabilities: [chat, streaming, tools]
    pricing:
      input_per_token: 0.000001
      output_per_token: 0.000002
```

### 4. 検証する

```bash
npm run validate
```

これにより、マニフェストが JSON Schema に対してチェックされ、エラーがあれば報告されます。

### 5. ビルドする

```bash
npm run build
```

これにより YAML が `dist/` ディレクトリに JSON としてコンパイルされます。

### 6. プルリクエストを送信する

- リポジトリをフォークする
- ブランチを作成する
- プロバイダーマニフェストとモデルエントリを追加する
- 検証が通ることを確認する
- プロバイダーに関するドキュメントを含む PR を送信する

## 検証ルール

JSON Schema により以下が強制されます：

- 必須フィールド（`id`、`endpoint`、`auth`、`parameter_mappings`）
- URL、環境変数名の有効な形式
- ストリーミング設定の正しい構造
- 有効なエラー分類型
- 機能フラグは boolean

## ヒント

- プロバイダーが OpenAI API 構造に従っている場合は **OpenAI 互換形式** を使用してください — 多くのプロバイダーが該当します（Groq、Together AI、DeepSeek）
- ストリーミング設定は慎重にテストしてください — プロバイダー間の違いのほとんどがここにあります
- `capabilities` フラグは正確に含めてください — ランタイムがフライト前検証に使用します
