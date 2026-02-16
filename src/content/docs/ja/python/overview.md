---
title: Python SDK 概要
description: ai-lib-python のアーキテクチャと設計 — AI-Protocol 用の開発者フレンドリーな Python ランタイム。
---

# Python SDK 概要

**ai-lib-python**（v0.7.0）は、AI-Protocol の公式 Python ランタイムです。Pydantic v2 による型安全性と本番グレードのテレメトリを持つ、開発者フレンドリーな完全 async インターフェースを提供します。

## アーキテクチャ

Python SDK は Rust ランタイムのレイヤーアーキテクチャを反映しています：

### クライアントレイヤー（`client/`）
- **AiClient** — ファクトリメソッド付きのメインエントリポイント
- **AiClientBuilder** — fluent 設定ビルダー
- **ChatRequestBuilder** — リクエスト構築
- **ChatResponse** / **CallStats** — レスポンス型
- **CancelToken** / **CancellableStream** — ストリームキャンセル

### プロトコルレイヤー（`protocol/`）
- **ProtocolLoader** — キャッシュ付きでローカル/環境変数/GitHub からマニフェストを読み込み
- **ProtocolManifest** — プロバイダー設定用の Pydantic モデル
- **Validator** — JSON Schema 検証（fastjsonschema）

### パイプラインレイヤー（`pipeline/`）
- **Decoder** — SSE、JSON Lines、Anthropic SSE デコーダー
- **Selector** — JSONPath ベースのフレーム選択（jsonpath-ng）
- **Accumulator** — ツール呼び出しの組み立て
- **FanOut** — マルチ候補展開
- **EventMapper** — プロトコル駆動、Default、Anthropic マッパー

### トランスポートレイヤー（`transport/`）
- **HttpTransport** — ストリーミング対応 httpx ベースの非同期 HTTP
- **Auth** — 環境変数と keyring からの API キー解決
- **ConnectionPool** — パフォーマンスのためのコネクションプール

### 耐障害性レイヤー（`resilience/`）
- **ResilientExecutor** — すべてのパターンを統合
- **RetryPolicy** — 指数バックオフ
- **RateLimiter** — トークンバケット
- **CircuitBreaker** — 障害分離
- **Backpressure** — 同時実行制限
- **FallbackChain** — マルチターゲットフェイルオーバー
- **PreflightChecker** — 統合リクエストゲート

### ルーティングレイヤー（`routing/`）
- **ModelManager** — モデル登録と選択
- **ModelArray** — エンドポイント間のロードバランシング
- **選択戦略** — ラウンドロビン、重み付き、コストベース、品質ベース

### テレメトリレイヤー（`telemetry/`）
- **MetricsCollector** — Prometheus メトリクスエクスポート
- **Tracer** — OpenTelemetry 分散トレーシング
- **Logger** — 構造化ログ
- **HealthChecker** — サービスヘルス監視
- **FeedbackCollector** — ユーザーフィードバック

### 追加モジュール
- **embeddings/** — ベクトル操作付き EmbeddingClient
- **cache/** — マルチバックエンドキャッシュ（メモリ、ディスク）
- **tokens/** — TokenCounter（tiktoken）とコスト見積もり
- **batch/** — 同時実行制御付き BatchCollector/Executor
- **plugins/** — プラグインベース、レジストリ、フック、ミドルウェア
- **structured/** — JSON モード、スキーマ生成、出力検証
- **guardrails/** — コンテンツフィルタリング、バリデーター

## 主要な依存関係

| パッケージ | 目的 |
|------------|------|
| `httpx` | 非同期 HTTP クライアント |
| `pydantic` | データ検証と型 |
| `pydantic-settings` | 設定管理 |
| `fastjsonschema` | マニフェスト検証 |
| `jsonpath-ng` | JSONPath 式 |
| `pyyaml` | YAML パース |

### オプション

| Extra | パッケージ |
|-------|------------|
| `[telemetry]` | OpenTelemetry、Prometheus |
| `[tokenizer]` | tiktoken |
| `[full]` | 上記すべて + watchdog、keyring |

## V2 プロトコル対応

v0.7.0 は AI-Protocol V2 仕様に対応しています：

- **標準エラーコード** — `errors/standard_codes.py` の 13 の frozen dataclass コード（E1001–E9999）
- **機能 Extra** — 8 つの pip extra（vision、audio、embeddings、structured、batch、agentic、telemetry、tokenizer）に加え「full」メタ extra
- **コンプライアンステスト** — 20/20 のクロスランタイムテストケースが合格
- **プロトコルバージョンサポート** — プロトコルバージョン 1.0、1.1、1.5、2.0 をサポート

## Python バージョン

**Python 3.10+** が必要です。

## 次のステップ

- **[クイックスタート](/python/quickstart/)** — すぐに始める
- **[AiClient API](/python/client/)** — 詳細な API ガイド
- **[ストリーミングパイプライン](/python/streaming/)** — パイプラインの内部
- **[耐障害性](/python/resilience/)** — 信頼性パターン
