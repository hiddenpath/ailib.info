---
title: Descripción general del SDK de TypeScript
description: Arquitectura y API pública de ai-lib-ts v1.0.0 — el runtime TypeScript de AI-Protocol.
---

# Descripción general del SDK de TypeScript

**ai-lib-ts** (v1.0.0) es el runtime TypeScript / Node.js de [AI-Protocol](https://github.com/ailib-official/ai-protocol). Se publica como `@ailib-official/ai-lib-ts` con tres puntos de entrada:

| Importación | Capa | Cuándo usarlo |
|--------|-------|----------|
| `@ailib-official/ai-lib-ts` | Fachada E + P | SDK completo (predeterminado) |
| `@ailib-official/ai-lib-ts/core` | Solo ejecución | Bundle mínimo — sin envoltorio de política en el transport |
| `@ailib-official/ai-lib-ts/contact` | Solo política | Resiliencia, enrutamiento — sin `AiClient` |

## Ruta de ejecución principal

En el chat, **`AiClient` no usa la API de operadores de bajo nivel `Pipeline`**. El flujo es:

1. Cargar el manifiesto del proveedor
2. Construir peticiones HTTP a partir de los campos del manifiesto
3. Enviar mediante **`HttpTransport`**
4. Analizar JSON / SSE con `response_paths` del manifiesto y respaldos al estilo OpenAI

`Pipeline` sigue siendo público para pruebas de cumplimiento e integraciones avanzadas. En este runtime **no existe** `ProviderDriver`.

## API pública de un vistazo

**Exportaciones de la raíz del paquete:**

- `AiClient`, `AiClientBuilder`, `createClient`, `createClientBuilder`
- `Message`, `StreamingEvent`, `Tool`, tipos de metadatos de ejecución
- `ProtocolLoader`, tipos de manifiesto + V2
- Política: `RetryPolicy`, `CircuitBreaker`, `RateLimiter`, `ModelManager`, `FallbackChain`, …
- Extras: `EmbeddingClient`, `McpToolBridge`, `Guardrails`, helpers de telemetría

### Límites de capacidad (descripción honesta)

| Área | En el paquete | No incluido |
|------|----------------|--------------|
| **MCP** | Conversión con `McpToolBridge` | Transporte de servidor MCP en `AiClient` |
| **Computer Use** | Tipos de configuración V2 | Ejecutor en tiempo de ejecución |
| **Hot reload** | — | No implementado |
| **Resiliencia** | Reintentos del manifiesto en el transport predeterminado | CB / límite de tasa / contrapresión salvo configuración explícita en el transport |
| **Embeddings** | `EmbeddingClient` | No es la ruta Pipeline del manifiesto |

## Siguientes pasos

- [Inicio rápido](/es/ts/quickstart/)
- [Streaming](/es/ts/streaming/)
- [Resiliencia](/es/ts/resilience/)
