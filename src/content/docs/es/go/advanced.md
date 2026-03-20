---
title: Características avanzadas (Go)
description: Embeddings, caché, procesamiento por lotes, plugins, guardrails, banderas de características, salida estructurada y códigos de error V2 en ai-lib-go v0.5.0.
---

# Características avanzadas

Más allá de la funcionalidad principal de chat, ai-lib-go proporciona varias capacidades avanzadas.

## Embeddings

Genere y trabaje con embeddings vectoriales:

```go
import "github.com/ailib-official/ai-lib-go/embeddings"

// Crear cliente de embeddings
client, err := embeddings.NewEmbeddingClient(ctx, "openai/text-embedding-3-small", nil)
if err != nil {
    panic(err)
}

// Generar embeddings
results, err := client.Embed(ctx, []string{
    "Go programming language",
    "Python programming language",
    "Cooking recipes",
})
if err != nil {
    panic(err)
}

// Calcular similitud
sim := embeddings.CosineSimilarity(results[0], results[1])
fmt.Printf("Similitud Go vs Python: %.3f\n", sim)
```

Las operaciones vectoriales incluyen similitud coseno, distancia euclidiana y producto escalar.

## Caché de respuestas

Almacene en caché las respuestas para reducir costos y latencia:

```go
import "github.com/ailib-official/ai-lib-go/cache"

// Configurar gestor de caché
mgr := cache.NewCacheManager(cache.NewMemoryCache(), 3600 * time.Second)

// Aplicar al cliente
aiClient, _ := client.NewAiClient(ctx, "openai", &client.Options{
    Cache: mgr,
})

// La primera llamada llega al proveedor
resp1, _ := aiClient.Chat().Model("gpt-4o").User("¿Cuánto es 2+2?").Execute(ctx)

// La segunda llamada idéntica devuelve la respuesta en caché
resp2, _ := aiClient.Chat().Model("gpt-4o").User("¿Cuánto es 2+2?").Execute(ctx)
```

## Procesamiento por lotes

Ejecute múltiples solicitudes eficientemente:

```go
import "github.com/ailib-official/ai-lib-go/batch"

executor := batch.NewBatchExecutor(5, 30 * time.Second)

requests := []client.ChatRequest{
    aiClient.Chat().User("Pregunta 1"),
    aiClient.Chat().User("Pregunta 2"),
    aiClient.Chat().User("Pregunta 3"),
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

## Conteo de tokens

Estime el uso de tokens y costos:

```go
import "github.com/ailib-official/ai-lib-go/tokens"

counter := tokens.GetCounterForModel("gpt-4o")
count := counter.Count("Hola, ¿cómo estás?")
fmt.Printf("Tokens: %d\n", count)

pricing := tokens.GetPricingForModel("openai/gpt-4o")
cost := pricing.Estimate(promptTokens, completionTokens)
fmt.Printf("Coste estimado: $%.4f\n", cost)
```

## Sistema de plugins

Extienda el cliente con plugins personalizados:

```go
import "github.com/ailib-official/ai-lib-go/plugins"

type LoggingPlugin struct{}

func (p *LoggingPlugin) OnRequest(req *plugins.Request) {
    fmt.Printf("Enviando solicitud a %s\n", req.Model)
}

func (p *LoggingPlugin) OnResponse(res *plugins.Response) {
    fmt.Printf("Obtenidos %d tokens\n", res.Usage.TotalTokens)
}

aiClient.RegisterPlugin(&LoggingPlugin{})
```

## Guardrails

Filtrado de contenido y seguridad:

```go
import "github.com/ailib-official/ai-lib-go/guardrails"

config := guardrails.NewConfig().
    AddFilter(guardrails.NewKeywordFilter([]string{"unsafe_word"})).
    EnablePiiDetection()

aiClient.SetGuardrails(config)
```

## Con puerta de características: Routing

Enrutamiento inteligente de modelos:

```go
import "github.com/ailib-official/ai-lib-go/routing"

manager := routing.NewModelManager().
    AddModel("openai/gpt-4o", 0.7).
    AddModel("anthropic/claude-3-5-sonnet", 0.3).
    SetStrategy(routing.StrategyWeighted)
```

## Con puerta de características: Interceptors

Interceptación de solicitudes/respuestas:

```go
import "github.com/ailib-official/ai-lib-go/interceptors"

pipeline := interceptors.NewPipeline().
    Add(&LoggingInterceptor{}).
    Add(&MetricsInterceptor{}).
    Add(&AuditInterceptor{})
```
