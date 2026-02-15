---
title: Detalles de la especificación
description: Profundice en la especificación principal de AI-Protocol — parámetros estándar, eventos, clases de error y políticas de reintento.
---

# Especificación principal

La especificación principal (`v1/spec.yaml`) define el vocabulario estándar que comparten todos los manifiestos de proveedores y tiempos de ejecución.

## Parámetros estándar

Estos parámetros tienen un significado consistente en todos los proveedores:

| Parameter | Type | Description |
|-----------|------|-------------|
| `temperature` | float | Control de aleatoriedad (0.0 – 2.0) |
| `max_tokens` | integer | Máximo de tokens de respuesta |
| `top_p` | float | Umbral de muestreo por núcleo |
| `stream` | boolean | Habilitar respuesta en streaming |
| `stop` | string[] | Secuencias de parada |
| `tools` | object[] | Definiciones de herramientas/funciones |
| `tool_choice` | string/object | Modo de selección de herramientas |
| `response_format` | object | Formato de salida estructurada |

Los manifiestos de proveedores mapean estos nombres estándar a nombres de parámetros específicos del proveedor. Por ejemplo, OpenAI usa `max_completion_tokens` mientras que Anthropic usa `max_tokens`.

## Eventos de streaming

La especificación define tipos de eventos de streaming unificados que emiten los tiempos de ejecución:

| Event | Description |
|-------|-------------|
| `PartialContentDelta` | Fragmento de contenido de texto |
| `ThinkingDelta` | Bloque de razonamiento/pensamiento (modelos de pensamiento extendido) |
| `ToolCallStarted` | Comienza la invocación de función/herramienta |
| `PartialToolCall` | Streaming de argumentos de llamada a herramienta |
| `ToolCallEnded` | Invocación de herramienta completa |
| `StreamEnd` | Flujo de respuesta completo |
| `StreamError` | Error a nivel de flujo |
| `Metadata` | Estadísticas de uso, información del modelo |

Los manifiestos de proveedores declaran reglas basadas en JSONPath que mapean eventos específicos del proveedor a estos tipos estándar.

## Clases de error (códigos estándar V2)

V2 define 13 códigos de error estandarizados. Los errores específicos del proveedor se mapean a estos códigos para un manejo consistente entre tiempos de ejecución:

| Code | Name | Category | Retryable | Fallbackable |
|------|------|----------|-----------|--------------|
| E1001 | `invalid_request` | Client | No | No |
| E1002 | `authentication` | Client | No | Yes |
| E1003 | `permission_denied` | Client | No | No |
| E1004 | `not_found` | Client | No | No |
| E1005 | `request_too_large` | Client | No | No |
| E2001 | `rate_limited` | Rate | Yes | Yes |
| E2002 | `quota_exhausted` | Rate | No | Yes |
| E3001 | `server_error` | Server | Yes | Yes |
| E3002 | `overloaded` | Server | Yes | Yes |
| E3003 | `timeout` | Server | Yes | Yes |
| E4001 | `conflict` | Operational | Yes | No |
| E4002 | `cancelled` | Operational | No | No |
| E9999 | `unknown` | Unknown | No | No |

- **Retryable** — Los tiempos de ejecución pueden reintentar la solicitud (con backoff) ante fallos transitorios
- **Fallbackable** — Los tiempos de ejecución pueden probar un proveedor o modelo alternativo en una cadena de fallback

## Políticas de reintento

La especificación define estrategias de reintento estándar:

```yaml
retry_policy:
  strategy: "exponential_backoff"
  max_retries: 3
  initial_delay_ms: 1000
  max_delay_ms: 30000
  backoff_multiplier: 2.0
  retryable_errors:
    - "rate_limited"
    - "overloaded"
    - "server_error"
    - "timeout"
```

## Razones de finalización

Razones de finalización normalizadas para la completación de la respuesta:

| Reason | Description |
|--------|-------------|
| `end_turn` | Finalización natural |
| `max_tokens` | Se alcanzó el límite de tokens |
| `tool_use` | El modelo quiere llamar a una herramienta |
| `stop_sequence` | Se encontró secuencia de parada |
| `content_filter` | Filtrado por política de contenido |

## Familias de API

Los proveedores se categorizan en familias de API para evitar confusión de formato de solicitud/respuesta:

- `openai` — APIs compatibles con OpenAI (también usado por Groq, Together, DeepSeek, etc.)
- `anthropic` — API de mensajes Anthropic
- `gemini` — API Google Gemini
- `custom` — Formato específico del proveedor

## Próximos pasos

- **[Manifiestos de proveedores](/protocol/providers/)** — Cómo funcionan las configuraciones de proveedores
- **[Registro de modelos](/protocol/models/)** — Detalles de configuración de modelos
