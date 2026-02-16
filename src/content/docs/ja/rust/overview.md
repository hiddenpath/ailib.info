---
title: Rust SDK 概要
description: ai-lib-rust のアーキテクチャと設計 — AI-Protocol 用の高性能 Rust ランタイム。
---

# Rust SDK 概要

**ai-lib-rust**（v0.8.0）は、AI-Protocol 仕様の高性能 Rust ランタイムです。プロバイダーの動作のすべてが設定から来るプロトコル駆動アーキテクチャを実装しています。

## V2 プロトコル対応

ai-lib-rust v0.8.0 は AI-Protocol V2 仕様に対応しています：

- **標準エラーコード**：すべてのエラーパスに統合された 13 バリアントの `StandardErrorCode` enum（E1001–E9999）
- **フィーチャーフラグ**：7 つの機能（`embeddings`、`batch`、`guardrails`、`tokens`、`telemetry`、`routing_mvp`、`interceptors`）に加え `full` メタ機能
- **コンプライアンステスト**：20/20 のクロスランタイムテストケースが合格
- **構造化出力**：スキーマ検証付き JSON モード

## アーキテクチャ

SDK は明確なレイヤーに整理されています：

### クライアントレイヤー（`client/`）
ユーザー向け API：
- **AiClient** — メインエントリポイント、モデル識別子から作成
- **AiClientBuilder** — 耐障害性設定を含む設定ビルダー
- **ChatRequestBuilder** — チャットリクエスト構築のための fluent API
- **CallStats** — リクエスト/レスポンス統計（トークン、レイテンシ）
- **CancelHandle** — グラースフルなストリームキャンセル

### プロトコルレイヤー（`protocol/`）
AI-Protocol マニフェストの読み込みと解釈：
- **ProtocolLoader** — ローカルファイル、環境変数、または GitHub から読み込み
- **ProtocolManifest** — パース済みプロバイダー設定
- **Validator** — JSON Schema 検証
- **UnifiedRequest** — プロバイダー固有の JSON にコンパイルされる標準リクエスト形式

### パイプラインレイヤー（`pipeline/`）
ストリーミング処理の中核 — オペレーターベースのパイプライン：
- **Decoder** — バイトストリームを JSON フレーム（SSE、JSON Lines）に変換
- **Selector** — JSONPath 式でフレームをフィルタリング
- **Accumulator** — 部分チャンクからツール呼び出しを状態を持って組み立てる
- **FanOut** — マルチ候補レスポンスを展開
- **EventMapper** — フレームを統一 `StreamingEvent` 型に変換
- **Retry/Fallback** — パイプラインレベルのリトライおよびフォールバックオペレーター

### トランスポートレイヤー（`transport/`）
HTTP 通信：
- **HttpTransport** — reqwest ベースの HTTP クライアント
- **Auth** — API キー解決（OS キーリング → 環境変数）
- **Middleware** — ログ、メトリクス用のトランスポートミドルウェア

### 耐障害性レイヤー（`resilience/`）
本番の信頼性パターン：
- **CircuitBreaker** — オープン/ハーフオープン/クローズの障害分離
- **RateLimiter** — トークンバケットアルゴリズム
- **Backpressure** — max_inflight セマフォ

### 追加モジュール
- **embeddings/** — ベクトル操作付き EmbeddingClient
- **cache/** — TTL 付きレスポンスキャッシュ（MemoryCache）
- **batch/** — BatchCollector と BatchExecutor
- **tokens/** — トークンカウントとコスト見積もり
- **plugins/** — プラグイン trait、レジストリ、フック、ミドルウェア
- **guardrails/** — コンテンツフィルタリング、PII 検出
- **routing/** — モデルルーティングとロードバランシング（フィーチャーゲート）
- **telemetry/** — ユーザーフィードバック収集のフィードバックシンク

## 主要な依存関係

| Crate | 目的 |
|-------|------|
| `tokio` | 非同期ランタイム |
| `reqwest` | HTTP クライアント |
| `serde` / `serde_json` / `serde_yaml` | シリアライゼーション |
| `jsonschema` | マニフェスト検証 |
| `tracing` | 構造化ログ |
| `arc-swap` | ホットリロードサポート |
| `notify` | ファイル監視 |
| `keyring` | OS キーリング統合 |

## フィーチャーフラグ

Cargo 経由で有効化できるオプション機能（すべて有効にするには `full` を使用）：

| 機能 | 有効化するもの |
|------|----------------|
| `embeddings` | EmbeddingClient、ベクトル操作 |
| `batch` | BatchCollector、BatchExecutor |
| `guardrails` | コンテンツフィルタリング、PII 検出 |
| `tokens` | トークンカウント、コスト見積もり |
| `telemetry` | 高度なオブザーバビリティシンク |
| `routing_mvp` | CustomModelManager、ModelArray、ロードバランシング戦略 |
| `interceptors` | ログ、メトリクス、監査用の InterceptorPipeline |

## 環境変数

| 変数 | 目的 |
|------|------|
| `AI_PROTOCOL_DIR` | プロトコルマニフェストディレクトリ |
| `<PROVIDER>_API_KEY` | プロバイダー API キー（例：`OPENAI_API_KEY`） |
| `AI_LIB_RPS` | レート制限（1 秒あたりのリクエスト数） |
| `AI_LIB_BREAKER_FAILURE_THRESHOLD` | サーキットブレーカーのしきい値 |
| `AI_LIB_MAX_INFLIGHT` | 最大同時リクエスト数 |
| `AI_HTTP_TIMEOUT_SECS` | HTTP タイムアウト |

## 次のステップ

- **[クイックスタート](/rust/quickstart/)** — 数分で始める
- **[AiClient API](/rust/client/)** — クライアントの詳細な使い方
- **[ストリーミングパイプライン](/rust/streaming/)** — パイプラインの詳細
- **[耐障害性](/rust/resilience/)** — 信頼性パターン
