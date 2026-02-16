---
title: 耐障害性（Rust）
description: ai-lib-rust v0.8.0 における本番グレードの信頼性パターン — サーキットブレーカー、レートリミッター、バックプレッシャー、リトライ。
---

# 耐障害性パターン

ai-lib-rust（v0.8.0）には本番グレードの信頼性パターンが標準で含まれています。リトライとフォールバックの判断は V2 標準エラーコードを使用します：`StandardErrorCode` の `retryable` と `fallbackable` プロパティが、エラーがリトライまたはモデルフォールバックをトリガーするかどうかを決定します。

## サーキットブレーカー

障害中のプロバイダーへのリクエストを止めることで、連鎖故障を防ぎます：

**状態：**
- **Closed** — 通常動作、リクエストが通過
- **Open** — 失敗が多すぎ、リクエストは即座に拒否
- **Half-Open** — クールダウン後、テストリクエストを許可

**設定：**

```bash
export AI_LIB_BREAKER_FAILURE_THRESHOLD=5
export AI_LIB_BREAKER_COOLDOWN_SECS=30
```

サーキットは `FAILURE_THRESHOLD` 回の連続失敗後にオープンし、テスト前に `COOLDOWN_SECS` 秒間オープンのままになります。

## レートリミッター

トークンバケットアルゴリズムでプロバイダーのレート制限超過を防ぎます：

```bash
export AI_LIB_RPS=10    # 1 秒あたりの最大リクエスト数
export AI_LIB_RPM=600   # 1 分あたりの最大リクエスト数
```

制限を超えたリクエストは拒否ではなくキューイングされ、スムーズなスループットを提供します。

## バックプレッシャー

セマフォで同時実行中のリクエストを制限します：

```bash
export AI_LIB_MAX_INFLIGHT=50
```

制限に達すると、新しいリクエストはスロットが空くまで待機します。

## リトライ

プロトコルマニフェストのリトライポリシーに基づく指数バックオフリトライ：

```yaml
# プロバイダーマニフェスト内
retry_policy:
  strategy: "exponential_backoff"
  max_retries: 3
  initial_delay_ms: 1000
  max_delay_ms: 30000
  retryable_errors:
    - "rate_limited"
    - "overloaded"
    - "server_error"
```

リトライ可能と分類されたエラーのみがリトライをトリガーします。認証エラーなどは即座に失敗します。

## パターンの組み合わせ

すべての耐障害性パターンは連携して動作します。典型的なリクエストフロー：

1. **バックプレッシャー** — 最大実行中数の場合はスロットを待機
2. **サーキットブレーカー** — サーキットがオープンの場合は即座に拒否
3. **レートリミッター** — レート制限の場合はトークンを待機
4. **実行** — リクエストを送信
5. **リトライ** — リトライ可能なエラーの場合、待機してリトライ
6. **更新** — サーキットブレーカー用に成功/失敗を記録

## オブザーバビリティ

ランタイムで耐障害性の状態を監視します：

```rust
// サーキットブレーカーの状態を確認
let state = client.circuit_state();
println!("Circuit: {:?}", state); // Closed, Open, HalfOpen

// 現在の実行中数を確認
let inflight = client.current_inflight();
```

## 次のステップ

- **[高度な機能](/rust/advanced/)** — 埋め込み、キャッシュ、プラグイン
- **[AiClient API](/rust/client/)** — クライアントの使い方
