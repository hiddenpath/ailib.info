---
title: AiClient (Go)
description: Referencia de la interfaz AiClient de Go.
---

# AiClient

`AiClient` es el punto de entrada principal para utilizar `ai-lib-go`. Gestiona el cliente `net/http` subyacente, el análisis de manifiestos, el mapeo de errores y las canalizaciones de streaming.

## Instanciación

```go
aiClient, err := client.NewAiClient(ctx, providerName, options)
```

- `providerName`: El nombre exacto del manifiesto del proveedor (por ejemplo, `openai`, `anthropic`, `gemini`).
- `options`: Argumentos opcionales como rutas de manifiesto personalizadas, sobrescritura del cliente HTTP o claves API explícitas (aunque se prefieren las variables de entorno).

## Integración de contexto

A diferencia de otros runtimes, el SDK de Go aprovecha enormemente `context.Context` para la resiliencia y la gestión del ciclo de vida:

```go
ctx, cancel := context.WithTimeout(context.Background(), 10 * time.Second)
defer cancel()

// Si la solicitud HTTP o el flujo tardan más de 10 segundos, se cancelarán automáticamente.
stream, err := aiClient.Chat().Model("gpt-4o").User("Lista 5 colores").ExecuteStream(ctx)
```

## Endpoints compatibles

Actualmente, los constructores `Chat()` y `Embeddings()` están disponibles. El soporte para Multimodal, MCP y Computer Use está previsto para la versión `v0.6.0`.
