---
title: 高级功能（Go）
description: ai-lib-go v0.5.0 中的 embeddings、缓存、批处理、插件、guardrails、功能标志、结构化输出及 V2 错误码。
---

# 高级功能

除核心聊天功能外，ai-lib-go 还提供多项高级能力。

## Embeddings

生成并处理向量 embedding：

```go
import "github.com/hiddenpath/ai-lib-go/embeddings"

// 创建 embedding 客户端
client, err := embeddings.NewEmbeddingClient(ctx, "openai/text-embedding-3-small", nil)
if err != nil {
    panic(err)
}

// 生成 embeddings
results, err := client.Embed(ctx, []string{
    "Go 编程语言",
    "Python 编程语言",
    "食谱",
})
if err != nil {
    panic(err)
}

// 计算相似度
sim := embeddings.CosineSimilarity(results[0], results[1])
fmt.Printf("Go vs Python 相似度: %.3f\n", sim)
```

向量操作包括余弦相似度、欧几里得距离和点积。

## 响应缓存

缓存响应以降低成本和延迟：

```go
import "github.com/hiddenpath/ai-lib-go/cache"

// 配置缓存管理器
mgr := cache.NewCacheManager(cache.NewMemoryCache(), 3600 * time.Second)

// 应用到客户端
aiClient, _ := client.NewAiClient(ctx, "openai", &client.Options{
    Cache: mgr,
})

// 第一次调用请求提供商
resp1, _ := aiClient.Chat().Model("gpt-4o").User("2+2 等于几？").Execute(ctx)

// 第二次相同的调用返回缓存的响应
resp2, _ := aiClient.Chat().Model("gpt-4o").User("2+2 等于几？").Execute(ctx)
```

## 批处理

高效执行多个请求：

```go
import "github.com/hiddenpath/ai-lib-go/batch"

executor := batch.NewBatchExecutor(5, 30 * time.Second)

requests := []client.ChatRequest{
    aiClient.Chat().User("问题 1"),
    aiClient.Chat().User("问题 2"),
    aiClient.Chat().User("问题 3"),
}

results := executor.Execute(ctx, requests)
for _, res := range results {
    if res.Error != nil {
        fmt.Printf("错误: %v\n", res.Error)
        continue
    }
    fmt.Println(res.Response.Content)
}
```

## Token 计数

估算 token 使用量与成本：

```go
import "github.com/hiddenpath/ai-lib-go/tokens"

counter := tokens.GetCounterForModel("gpt-4o")
count := counter.Count("你好，最近怎么样？")
fmt.Printf("Tokens: %d\n", count)

pricing := tokens.GetPricingForModel("openai/gpt-4o")
cost := pricing.Estimate(promptTokens, completionTokens)
fmt.Printf("估算成本: $%.4f\n", cost)
```

## 插件系统

使用自定义插件扩展客户端：

```go
import "github.com/hiddenpath/ai-lib-go/plugins"

type LoggingPlugin struct{}

func (p *LoggingPlugin) OnRequest(req *plugins.Request) {
    fmt.Printf("正在向 %s 发送请求\n", req.Model)
}

func (p *LoggingPlugin) OnResponse(res *plugins.Response) {
    fmt.Printf("获得 %d 个 token\n", res.Usage.TotalTokens)
}

aiClient.RegisterPlugin(&LoggingPlugin{})
```

## Guardrails

内容过滤与安全：

```go
import "github.com/hiddenpath/ai-lib-go/guardrails"

config := guardrails.NewConfig().
    AddFilter(guardrails.NewKeywordFilter([]string{"不安全词汇"})).
    EnablePiiDetection()

aiClient.SetGuardrails(config)
```

## 功能门控：Routing

智能模型路由：

```go
import "github.com/hiddenpath/ai-lib-go/routing"

manager := routing.NewModelManager().
    AddModel("openai/gpt-4o", 0.7).
    AddModel("anthropic/claude-3-5-sonnet", 0.3).
    SetStrategy(routing.StrategyWeighted)
```

## 功能门控：Interceptors

请求/响应拦截：

```go
import "github.com/hiddenpath/ai-lib-go/interceptors"

pipeline := interceptors.NewPipeline().
    Add(&LoggingInterceptor{}).
    Add(&MetricsInterceptor{}).
    Add(&AuditInterceptor{})
```
