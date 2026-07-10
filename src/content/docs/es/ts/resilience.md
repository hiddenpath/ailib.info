---
title: Resiliencia (TypeScript)
description: Patrones de fiabilidad en producción en ai-lib-ts v1.0.0.
---

# Patrones de resiliencia

ai-lib-ts (v1.0.0) aplica **reintentos derivados del manifiesto** en el `HttpTransport` de la capa P predeterminado que usa `AiClient`. El circuit breaker, el límite de tasa y la contrapresión **no** se activan automáticamente mediante `AiClientBuilder`: configure `TransportOptions.resilience` al construir el transport manualmente, o use `PreflightChecker` junto al cliente.

## Qué incluye el `AiClient` predeterminado

| Patrón | `AiClient` predeterminado |
|---------|-------------------|
| Reintento (no streaming) | Sí — desde el manifiesto / valores predeterminados |
| Circuit breaker | No |
| Límite de tasa | No |
| Contrapresión | No |

## `/core` frente a la raíz

`@ailib-official/ai-lib-ts/core` usa el `HttpTransport` de la capa E **sin envoltorio de reintentos**. Use la raíz o `/contact` cuando necesite comportamiento de política.

## Resiliencia manual

Importe desde la capa de política y conecte las opciones del transport de forma explícita (véase `src/transport/index.ts`). `AiClientBuilder` no ofrece métodos encadenados `.withCircuitBreaker()` / `.withRateLimiter()`.

## Siguientes pasos

- **[Avanzado](/es/ts/advanced/)**
- **[API del cliente](/es/ts/client/)**
