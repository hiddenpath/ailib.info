---
title: Advanced Features (Go)
description: Embeddings, caching, batching, plugins, guardrails, feature flags, structured output, and V2 error codes in ai-lib-go v0.5.0.
---

# Advanced Features

Beyond core chat functionality, ai-lib-go provides several advanced capabilities.

## Embeddings

Generate and work with vector embeddings:

```go
import "github.com/hiddenpath/ai-lib-go/embeddings"

// Create embedding client
client, err := embeddings.NewEmbeddingClient(ctx, "openai/text-embedding-3-small", nil)
if err != nil {
    panic(err)
}

// Generate embeddings
results, err := client.Embed(ctx, []string{
    "Go programming language",
    "Python programming language",
    "Cooking recipes",
})
if err != nil {
    panic(err)
}

// Calculate similarity
sim := embeddings.CosineSimilarity(results[0], results[1])
fmt.Printf("Go vs Python similarity: %.3f\n", sim)
```

Vector operations include cosine similarity, Euclidean distance, and dot product.

## Response Caching

Cache responses to reduce costs and latency:

```go
import "github.com/hiddenpath/ai-lib-go/cache"

// Configure cache manager
mgr := cache.NewCacheManager(cache.NewMemoryCache(), 3600 * time.Second)

// Apply to client
aiClient, _ := client.NewAiClient(ctx, "openai", &client.Options{
    Cache: mgr,
})

// First call hits the provider
resp1, _ := aiClient.Chat().Model("gpt-4o").User("What is 2+2?").Execute(ctx)

// Second identical call returns cached response
resp2, _ := aiClient.Chat().Model("gpt-4o").User("What is 2+2?").Execute(ctx)
```

## Batch Processing

Execute multiple requests efficiently:

```go
import "github.com/hiddenpath/ai-lib-go/batch"

executor := batch.NewBatchExecutor(5, 30 * time.Second)

requests := []client.ChatRequest{
    aiClient.Chat().User("Question 1"),
    aiClient.Chat().User("Question 2"),
    aiClient.Chat().User("Question 3"),
}

results := executor.Execute(ctx, requests)
for _, res := range results {
    if res.Error != nil {
        fmt.Printf("Error: %v\n", res.Error)
        continue
    }
    fmt.Println(res.Response.Content)
}
```

## Token Counting

Estimate token usage and costs:

```go
import "github.com/hiddenpath/ai-lib-go/tokens"

counter := tokens.GetCounterForModel("gpt-4o")
count := counter.Count("Hello, how are you?")
fmt.Printf("Tokens: %d\n", count)

pricing := tokens.GetPricingForModel("openai/gpt-4o")
cost := pricing.Estimate(promptTokens, completionTokens)
fmt.Printf("Estimated cost: $%.4f\n", cost)
```

## Plugin System

Extend the client with custom plugins:

```go
import "github.com/hiddenpath/ai-lib-go/plugins"

type LoggingPlugin struct{}

func (p *LoggingPlugin) OnRequest(req *plugins.Request) {
    fmt.Printf("Sending request to %s\n", req.Model)
}

func (p *LoggingPlugin) OnResponse(res *plugins.Response) {
    fmt.Printf("Got %d tokens\n", res.Usage.TotalTokens)
}

aiClient.RegisterPlugin(&LoggingPlugin{})
```

## Guardrails

Content filtering and safety:

```go
import "github.com/hiddenpath/ai-lib-go/guardrails"

config := guardrails.NewConfig().
    AddFilter(guardrails.NewKeywordFilter([]string{"unsafe_word"})).
    EnablePiiDetection()

aiClient.SetGuardrails(config)
```

## Feature-Gated: Routing

Smart model routing:

```go
import "github.com/hiddenpath/ai-lib-go/routing"

manager := routing.NewModelManager().
    AddModel("openai/gpt-4o", 0.7).
    AddModel("anthropic/claude-3-5-sonnet", 0.3).
    SetStrategy(routing.StrategyWeighted)
```

## Feature-Gated: Interceptors

Request/response interception:

```go
import "github.com/hiddenpath/ai-lib-go/interceptors"

pipeline := interceptors.NewPipeline().
    Add(&LoggingInterceptor{}).
    Add(&MetricsInterceptor{}).
    Add(&AuditInterceptor{})
```
