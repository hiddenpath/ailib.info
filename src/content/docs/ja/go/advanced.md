---
title: 高度な機能（Go）
description: ai-lib-go v0.5.0 における埋め込み、キャッシュ、バッチ、プラグイン、ガードレール、フィーチャーフラグ、構造化出力、V2 エラーコード。
---

# 高度な機能

コアチャット機能に加え、ai-lib-go はいくつかの高度な機能を提供します。

## 埋め込み

ベクトル埋め込みの生成と操作：

```go
import "github.com/ailib-official/ai-lib-go/embeddings"

// 埋め込みクライアントの作成
client, err := embeddings.NewEmbeddingClient(ctx, "openai/text-embedding-3-small", nil)
if err != nil {
    panic(err)
}

// 埋め込みの生成
results, err := client.Embed(ctx, []string{
    "Go programming language",
    "Python programming language",
    "Cooking recipes",
})
if err != nil {
    panic(err)
}

// 類似度の計算
sim := embeddings.CosineSimilarity(results[0], results[1])
fmt.Printf("Go vs Python の類似度: %.3f\n", sim)
```

ベクトル操作にはコサイン類似度、ユークリッド距離、ドット積が含まれます。

## レスポンスキャッシュ

コストとレイテンシを削減するためのレスポンスキャッシュ：

```go
import "github.com/ailib-official/ai-lib-go/cache"

// キャッシュマネージャーの設定
mgr := cache.NewCacheManager(cache.NewMemoryCache(), 3600 * time.Second)

// クライアントへの適用
aiClient, _ := client.NewAiClient(ctx, "openai", &client.Options{
    Cache: mgr,
})

// 最初の呼び出しはプロバイダーにヒット
resp1, _ := aiClient.Chat().Model("gpt-4o").User("2+2 は何ですか？").Execute(ctx)

// 2 回目の同一呼び出しはキャッシュから返却
resp2, _ := aiClient.Chat().Model("gpt-4o").User("2+2 は何ですか？").Execute(ctx)
```

## バッチ処理

複数リクエストを効率的に実行：

```go
import "github.com/ailib-official/ai-lib-go/batch"

executor := batch.NewBatchExecutor(5, 30 * time.Second)

requests := []client.ChatRequest{
    aiClient.Chat().User("質問 1"),
    aiClient.Chat().User("質問 2"),
    aiClient.Chat().User("質問 3"),
}

results := executor.Execute(ctx, requests)
for _, res := range results {
    if res.Error != nil {
        fmt.Printf("エラー: %v\n", res.Error)
        continue
    }
    fmt.Println(res.Response.Content)
}
```

## トークンカウント

トークン使用量とコストの見積もり：

```go
import "github.com/ailib-official/ai-lib-go/tokens"

counter := tokens.GetCounterForModel("gpt-4o")
count := counter.Count("こんにちは、お元気ですか？")
fmt.Printf("トークン数: %d\n", count)

pricing := tokens.GetPricingForModel("openai/gpt-4o")
cost := pricing.Estimate(promptTokens, completionTokens)
fmt.Printf("見積もりコスト: $%.4f\n", cost)
```

## プラグインシステム

カスタムプラグインでクライアントを拡張：

```go
import "github.com/ailib-official/ai-lib-go/plugins"

type LoggingPlugin struct{}

func (p *LoggingPlugin) OnRequest(req *plugins.Request) {
    fmt.Printf("%s にリクエストを送信しています\n", req.Model)
}

func (p *LoggingPlugin) OnResponse(res *plugins.Response) {
    fmt.Printf("%d トークンを取得しました\n", res.Usage.TotalTokens)
}

aiClient.RegisterPlugin(&LoggingPlugin{})
```

## ガードレール

コンテンツフィルタリングとセーフティ：

```go
import "github.com/ailib-official/ai-lib-go/guardrails"

config := guardrails.NewConfig().
    AddFilter(guardrails.NewKeywordFilter([]string{"unsafe_word"})).
    EnablePiiDetection()

aiClient.SetGuardrails(config)
```

## フィーチャーゲート：ルーティング

スマートモデルルーティング：

```go
import "github.com/ailib-official/ai-lib-go/routing"

manager := routing.NewModelManager().
    AddModel("openai/gpt-4o", 0.7).
    AddModel("anthropic/claude-3-5-sonnet", 0.3).
    SetStrategy(routing.StrategyWeighted)
```

## フィーチャーゲート：インターセプター

リクエスト/レスポンスのインターセプション：

```go
import "github.com/ailib-official/ai-lib-go/interceptors"

pipeline := interceptors.NewPipeline().
    Add(&LoggingInterceptor{}).
    Add(&MetricsInterceptor{}).
    Add(&AuditInterceptor{})
```
