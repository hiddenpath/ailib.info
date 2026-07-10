---
title: レジリエンス（TypeScript）
description: ai-lib-ts v1.0.0 の本番向け信頼性パターン。
---

# レジリエンスパターン

ai-lib-ts（v1.0.0）は、`AiClient` が使うデフォルトの P 層 `HttpTransport` 上で**マニフェスト由来の再試行**を適用します。サーキットブレーカー、レート制限、背圧は `AiClientBuilder` 経由では**自動有効化されません** — transport を手動構築するときに `TransportOptions.resilience` を設定するか、クライアントの傍らで `PreflightChecker` を使ってください。

## デフォルトの `AiClient` に含まれるもの

| パターン | デフォルト `AiClient` |
|---------|-------------------|
| 再試行（非ストリーム） | あり — マニフェスト / デフォルトから |
| サーキットブレーカー | なし |
| レート制限 | なし |
| 背圧 | なし |

## `/core` とルートパッケージ

`@ailib-official/ai-lib-ts/core` は再試行ラッパーのない E 層 `HttpTransport` を使います。ポリシー動作が必要な場合はルートパッケージまたは `/contact` を使ってください。

## 手動レジリエンス

ポリシー層からインポートし、transport オプションを明示的に配線します（`src/transport/index.ts` を参照）。`AiClientBuilder` に `.withCircuitBreaker()` / `.withRateLimiter()` チェーンメソッドはありません。

## 次のステップ

- **[高度な機能](/ja/ts/advanced/)**
- **[Client API](/ja/ts/client/)**
