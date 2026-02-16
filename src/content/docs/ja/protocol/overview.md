---
title: AI-Protocol 概要
description: AI-Protocol 仕様の理解 — AI-Lib エコシステムのプロバイダー非依存の基盤。
---

# AI-Protocol 概要

AI-Protocol は、AI モデルとのやり取りを標準化する **プロバイダー非依存の仕様** です。ランタイムがプロバイダーについて知る必要があること（設定）と、リクエストの実行方法（コード）を分離します。

## コアの哲学

> **すべてのロジックはオペレーター、すべての設定はプロトコル。**

プロバイダー固有の動作のすべて — エンドポイント、認証、パラメータ名、ストリーミング形式、エラーコード — は YAML 設定ファイルで宣言されます。ランタイム実装には **ハードコーディングされたプロバイダーロジックは一切含まれません**。

## リポジトリの構成

```
ai-protocol/
├── v1/
│   ├── spec.yaml          # コア仕様（v0.7.0）
│   ├── providers/          # 37 のプロバイダーマニフェスト
│   │   ├── openai.yaml
│   │   ├── anthropic.yaml
│   │   ├── gemini.yaml
│   │   ├── deepseek.yaml
│   │   └── ...
│   └── models/             # モデルインスタンスレジストリ
│       ├── gpt.yaml
│       ├── claude.yaml
│       └── ...
├── schemas/                # JSON Schema 検証
│   ├── v1.json
│   └── spec.json
├── dist/                   # プリコンパイル済み JSON（生成）
├── scripts/                # ビルド & 検証ツール
└── examples/               # 使用例
```

## プロバイダーマニフェスト

各プロバイダーには、ランタイムが必要とするすべてを宣言する YAML マニフェストがあります：

| セクション | 目的 |
|------------|------|
| `endpoint` | ベース URL、チャットパス、プロトコル |
| `auth` | 認証タイプ、トークン環境変数、ヘッダー |
| `parameter_mappings` | 標準 → プロバイダー固有のパラメータ名 |
| `streaming` | デコーダー形式（SSE/NDJSON）、イベントマッピングルール（JSONPath） |
| `error_classification` | HTTP ステータス → 標準エラー型 |
| `retry_policy` | 戦略、遅延、リトライ条件 |
| `rate_limit_headers` | レート制限情報のヘッダー名 |
| `capabilities` | フィーチャーフラグ（streaming、tools、vision、reasoning） |

### 例：Anthropic プロバイダー

```yaml
id: anthropic
protocol_version: "0.7"
endpoint:
  base_url: "https://api.anthropic.com/v1"
  chat_path: "/messages"
auth:
  type: bearer
  token_env: "ANTHROPIC_API_KEY"
  headers:
    anthropic-version: "2023-06-01"
parameter_mappings:
  temperature: "temperature"
  max_tokens: "max_tokens"
  stream: "stream"
  tools: "tools"
streaming:
  decoder:
    format: "anthropic_sse"
  event_map:
    - match: "$.type == 'content_block_delta'"
      emit: "PartialContentDelta"
      extract:
        content: "$.delta.text"
    - match: "$.type == 'message_stop'"
      emit: "StreamEnd"
error_classification:
  by_http_status:
    "429": "rate_limited"
    "401": "authentication"
    "529": "overloaded"
capabilities:
  streaming: true
  tools: true
  vision: true
  reasoning: true
```

## モデルレジストリ

モデルはプロバイダー参照、機能、価格で登録されます：

```yaml
models:
  claude-3-5-sonnet:
    provider: anthropic
    model_id: "claude-3-5-sonnet-20241022"
    context_window: 200000
    capabilities: [chat, vision, tools, streaming, reasoning]
    pricing:
      input_per_token: 0.000003
      output_per_token: 0.000015
```

## 検証

すべてのマニフェストは JSON Schema（2020-12）を使用して AJV で検証されます。CI パイプラインで正確性が強制されます：

```bash
npm run validate    # すべての設定を検証
npm run build       # YAML → JSON をコンパイル
```

## バージョニング

AI-Protocol はレイヤードバージョニングを使用します：

1. **仕様バージョン**（`v1/spec.yaml`）— スキーマ構造のバージョン（現在 v0.7.0）
2. **プロトコルバージョン**（マニフェスト内）— 使用するプロトコル機能（現在 0.7）
3. **リリースバージョン**（`package.json`）— 仕様パッケージの SemVer（v0.7.0）

## V2 プロトコルアーキテクチャ

プロトコル v0.7.0 は **V2 アーキテクチャ** を導入しています — レイヤー間の明確な関心の分離と、同心円マニフェストモデルです。

### 3 層ピラミッド

- **L1 コアプロトコル** — メッセージ形式、標準エラーコード（E1001–E9999）、バージョン宣言。すべてのプロバイダーがこのレイヤーを実装する必要があります。
- **L2 機能拡張** — ストリーミング、ビジョン、ツール。各拡張はフィーチャーフラグで制御され、プロバイダーは機能ごとにオプトインします。
- **L3 環境プロファイル** — API キー、エンドポイント、リトライポリシー。プロバイダーロジックを変更せずにオーバーライドできる環境固有の設定。

### 同心円マニフェストモデル

- **Ring 1 コアスケルトン**（必須）— 有効なマニフェストの最小フィールド：endpoint、auth、parameter mappings
- **Ring 2 機能マッピング**（条件付き）— ストリーミング設定、ツールマッピング、ビジョンパラメータ — プロバイダーがサポートする場合に存在
- **Ring 3 高度な拡張**（オプション）— カスタムヘッダー、レート制限ヘッダー、高度なリトライポリシー

### V2-Alpha プロバイダー

OpenAI、Anthropic、Gemini はすでに **v2-alpha** 形式で利用可能です。これらのマニフェストは Ring 1/2/3 構造を使用し、v1 マニフェストと併用できます。

### 標準エラーコード

V2 では 5 カテゴリにわたる 13 の標準化されたエラーコード（E1001–E9999）を定義しています：クライアントエラー（E1xxx）、レート/クォータ（E2xxx）、サーバー（E3xxx）、競合/キャンセル（E4xxx）、不明（E9999）。完全なコード一覧は [仕様](/protocol/spec/) をご覧ください。

### クロスランタイム一貫性

**コンプライアンステストスイート** により、Rust と Python ランタイム間で同一の動作が保証されます。すべての V2 プロバイダーは両実装で同じテストマトリックスに合格します。

## 次のステップ

- **[仕様詳細](/protocol/spec/)** — コア仕様の詳細
- **[プロバイダーマニフェスト](/protocol/providers/)** — マニフェストの仕組み
- **[モデルレジストリ](/protocol/models/)** — モデル設定
- **[プロバイダーへの貢献](/protocol/contributing/)** — 新規プロバイダーの追加
