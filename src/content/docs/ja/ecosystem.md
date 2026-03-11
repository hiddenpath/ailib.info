---
title: エコシステムアーキテクチャ
description: AI-Protocol、ai-lib-rust、ai-lib-python、ai-lib-ts、ai-lib-go が統合エコシステムとしてどのように連携するか。
---

# エコシステムアーキテクチャ

AI-Lib エコシステムは、各レイヤーが明確な責務を持つクリーンな 3 層アーキテクチャで構築されています。現在のバージョン：**AI-Protocol v0.8.3**、**ai-lib-rust v0.9.3**、**ai-lib-python v0.8.3**、**ai-lib-ts v0.5.3**、**ai-lib-go v0.0.1**、**ai-protocol-mock v0.1.11**。

## 3 つのレイヤー

### 1. プロトコルレイヤー — AI-Protocol

**仕様**レイヤーです。YAML マニフェストで以下を定義します：

- **プロバイダーマニフェスト**（`providers/*.yaml`）— 37 のプロバイダーそれぞれのエンドポイント、認証、パラメータマッピング、ストリーミングデコーダー、エラー分類
- **モデルレジストリ**（`models/*.yaml`）— コンテキストウィンドウ、機能、価格を持つモデルインスタンス
- **コア仕様**（`spec.yaml`）— 標準パラメータ、イベント、エラー型、リトライポリシー
- **スキーマ**（`schemas/`）— すべての設定の JSON Schema 検証

プロトコルレイヤーは**言語非依存**です。あらゆる言語のランタイムから消費されます。

### 2. ランタイムレイヤー — Rust・Python・TypeScript・Go SDK

**実行**レイヤーです。ランタイムは以下を実装します：

- **プロトコル読み込み** — ローカルファイル、環境変数、GitHub からマニフェストを読み取り検証
- **リクエストコンパイル** — 統合リクエストをプロバイダー固有の HTTP 呼び出しに変換
- **ストリーミングパイプライン** — プロバイダーレスポンスをデコード、選択、蓄積、統一イベントにマッピング
- **耐障害性** — サーキットブレーカー、レート制限、リトライ、フォールバック
- **拡張機能** — 埋め込み、キャッシュ、バッチ処理、プラグイン

3 つのランタイムは同じプロトコル駆動アーキテクチャを共有します：

| コンセプト     | Rust                  | Python                 | TypeScript                 |
| -------------- | --------------------- | ---------------------- | -------------------------- |
| クライアント   | `AiClient`            | `AiClient`             | `AiClient`                 |
| ビルダー       | `AiClientBuilder`     | `AiClientBuilder`      | `AiClientBuilder`          |
| リクエスト     | `ChatRequestBuilder`  | `ChatRequestBuilder`   | `ChatBuilder`              |
| イベント       | `StreamingEvent` enum | `StreamingEvent` class | 統一ストリーミングイベント |
| トランスポート | reqwest (tokio)       | httpx (asyncio)        | fetch (Node.js)            |
| 型             | Rust structs          | Pydantic v2 models     | TypeScript interfaces      |

### 3. アプリケーションレイヤー — あなたのコード

アプリケーションは統合ランタイム API を使用します。単一の `AiClient` インターフェースがすべてのプロバイダーで動作します：

```
Your App → AiClient → Protocol Manifest → Provider API
```

モデル識別子を 1 つ変更するだけでプロバイダーを切り替えられます。コード変更は不要です。

## データフロー

`client.chat().user("Hello").stream()` を呼び出すと何が起こるか：

1. **AiClient** がリクエストを受け取る
2. **ProtocolLoader** がプロバイダーマニフェストを提供する
3. **リクエストコンパイラ** が標準パラメータをプロバイダー固有の JSON にマッピングする
4. **トランスポート** が正しい認証/ヘッダーで HTTP リクエストを送信する
5. **パイプライン** がストリーミングレスポンスを処理する：
   - **Decoder** がバイト → JSON フレーム（SSE または NDJSON）に変換
   - **Selector** が JSONPath で関連フレームをフィルタリング
   - **Accumulator** が部分的なツール呼び出しを組み立てる
   - **EventMapper** がフレーム → 統一 `StreamingEvent` に変換
6. **アプリケーション** が統一イベントをイテレートする

## プロトコルの読み込み

3 つのランタイムは次の順序でプロトコルマニフェストを検索します：

1. **カスタムパス** — ビルダーで明示的に設定
2. **環境変数** — `AI_PROTOCOL_DIR` または `AI_PROTOCOL_PATH`
3. **相対パス** — 作業ディレクトリからの `ai-protocol/` または `../ai-protocol/`
4. **GitHub フォールバック** — `hiddenpath/ai-protocol` リポジトリからダウンロード

つまり、ローカルセットアップなしで開発を開始できます。ランタイムが GitHub からマニフェストを自動的に取得します。

## V2 プロトコルの進化とガバナンス強化

V2 基盤は `v0.8.2` で生成系フルチェーンの運用ガバナンスまで拡張されました：

- **L1 コアプロトコル** — メッセージ形式、標準エラーコード（E1001–E9999）、バージョン宣言
- **L2 機能拡張** — ストリーミング、ビジョン、ツール、MCP、Computer Use、マルチモーダル
- **L3 環境プロファイル** — API キー、エンドポイント、リトライポリシー — 環境固有の設定

実行ガバナンス用のゲートスクリプトが追加されています：

- `npm run drift:check`
- `npm run gate:manifest-consumption`
- `npm run gate:compliance-matrix`
- `npm run gate:fullchain`
- `npm run release:gate`

さらに `--report-only` により段階的な非ブロッキング導入が可能です。

`ai-protocol-mock` の動画非同期ライフサイクルは、終端状態 `succeeded` / `failed` / `cancelled` をサポートし、`X-Mock-Video-Terminal` または `terminal_state` で制御できます。

Rust/Python/TypeScript の compliance 行列は、protocol loading、error classification、retry、message、stream、request を横断的に検証します。

## MCP との関係

AI-Protocol と MCP（Model Context Protocol）は**補完的**です：

- **MCP** は高レベルの関心事 — ツール登録、コンテキスト管理、エージェント調整
- **AI-Protocol** は低レベルの関心事 — API 正規化、ストリーミング形式変換、エラー分類

これらは異なるレイヤーで動作し、併用できます。

## 次のステップ

- **[AI-Protocol 概要](/protocol/overview/)** — 仕様を詳しく学ぶ
- **[Rust SDK](/rust/overview/)** — Rust ランタイムを探索する
- **[Python SDK](/python/overview/)** — Python ランタイムを探索する
- **[TypeScript SDK](/ts/overview/)** — TypeScript ランタイムを探索する
