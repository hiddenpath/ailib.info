---
title: Visión general del SDK Rust
description: Arquitectura y diseño de ai-lib-rust — el tiempo de ejecución Rust de alto rendimiento para AI-Protocol.
---

# Visión general del SDK Rust

**ai-lib-rust** (v0.8.0) es el tiempo de ejecución Rust de alto rendimiento para la especificación AI-Protocol. Implementa una arquitectura impulsada por protocolo donde todo el comportamiento del proveedor proviene de la configuración, no del código.

## Alineación con el protocolo V2

ai-lib-rust v0.8.0 está alineado con la especificación AI-Protocol V2:

- **Códigos de error estándar**: Enumeración `StandardErrorCode` de 13 variantes (E1001–E9999) integrada en todas las rutas de error
- **Banderas de características**: 7 características de capacidad (`embeddings`, `batch`, `guardrails`, `tokens`, `telemetry`, `routing_mvp`, `interceptors`) más la meta-característica `full`
- **Pruebas de conformidad**: 20/20 casos de prueba entre tiempos de ejecución aprobados
- **Salida estructurada**: Modo JSON con validación de esquema

## Arquitectura

El SDK está organizado en capas distintas:

### Capa de cliente (`client/`)
La API orientada al usuario:
- **AiClient** — Punto de entrada principal, creado a partir de identificadores de modelo
- **AiClientBuilder** — Constructor de configuración con ajustes de resiliencia
- **ChatRequestBuilder** — API fluida para construir solicitudes de chat
- **CallStats** — Estadísticas de solicitud/respuesta (tokens, latencia)
- **CancelHandle** — Cancelación elegante del flujo

### Capa de protocolo (`protocol/`)
Carga e interpreta manifiestos AI-Protocol:
- **ProtocolLoader** — Carga desde archivos locales, variables de entorno o GitHub
- **ProtocolManifest** — Configuración de proveedor analizada
- **Validator** — Validación JSON Schema
- **UnifiedRequest** — Formato de solicitud estándar compilado a JSON específico del proveedor

### Capa de canalización (`pipeline/`)
El corazón del procesamiento en streaming — una canalización basada en operadores:
- **Decoder** — Convierte flujos de bytes a frames JSON (SSE, JSON Lines)
- **Selector** — Filtra frames usando expresiones JSONPath
- **Accumulator** — Ensambla statefulmente llamadas a herramientas a partir de fragmentos parciales
- **FanOut** — Expande respuestas multicandidato
- **EventMapper** — Convierte frames a tipos `StreamingEvent` unificados
- **Retry/Fallback** — Operadores de reintento y fallback a nivel de canalización

### Capa de transporte (`transport/`)
Comunicación HTTP:
- **HttpTransport** — Cliente HTTP basado en reqwest
- **Auth** — Resolución de API key (keyring del SO → variables de entorno)
- **Middleware** — Middleware de transporte para logging, métricas

### Capa de resiliencia (`resilience/`)
Patrones de confiabilidad para producción:
- **CircuitBreaker** — Aislamiento de fallos abierto/semiabierto/cerrado
- **RateLimiter** — Algoritmo de token bucket
- **Backpressure** — Semáforo max_inflight

### Módulos adicionales
- **embeddings/** — EmbeddingClient con operaciones vectoriales
- **cache/** — Caché de respuestas con TTL (MemoryCache)
- **batch/** — BatchCollector y BatchExecutor
- **tokens/** — Conteo de tokens y estimación de costos
- **plugins/** — Rasgo Plugin, registro, hooks, middleware
- **guardrails/** — Filtrado de contenido, detección de PII
- **routing/** — Enrutamiento de modelos y balanceo de carga (con puerta de características)
- **telemetry/** — Recolector de retroalimentación para recolección de feedback del usuario

## Dependencias principales

| Crate | Propósito |
|-------|-----------|
| `tokio` | Tiempo de ejecución asíncrono |
| `reqwest` | Cliente HTTP |
| `serde` / `serde_json` / `serde_yaml` | Serialización |
| `jsonschema` | Validación de manifiestos |
| `tracing` | Registro estructurado |
| `arc-swap` | Soporte de recarga en caliente |
| `notify` | Vigilancia de archivos |
| `keyring` | Integración con keyring del SO |

## Banderas de características

Características opcionales habilitadas vía Cargo (use `full` para habilitar todas):

| Feature | Lo que habilita |
|---------|-----------------|
| `embeddings` | EmbeddingClient, operaciones vectoriales |
| `batch` | BatchCollector, BatchExecutor |
| `guardrails` | Filtrado de contenido, detección de PII |
| `tokens` | Conteo de tokens, estimación de costos |
| `telemetry` | Recolectores de observabilidad avanzada |
| `routing_mvp` | CustomModelManager, ModelArray, estrategias de balanceo de carga |
| `interceptors` | InterceptorPipeline para logging, métricas, auditoría |

## Variables de entorno

| Variable | Propósito |
|----------|-----------|
| `AI_PROTOCOL_DIR` | Directorio del manifiesto del protocolo |
| `<PROVIDER>_API_KEY` | Clave API del proveedor (ej. `OPENAI_API_KEY`) |
| `AI_LIB_RPS` | Límite de velocidad (solicitudes por segundo) |
| `AI_LIB_BREAKER_FAILURE_THRESHOLD` | Umbral del circuit breaker |
| `AI_LIB_MAX_INFLIGHT` | Máximo de solicitudes concurrentes |
| `AI_HTTP_TIMEOUT_SECS` | Timeout HTTP |

## Próximos pasos

- **[Inicio rápido](/rust/quickstart/)** — Comenzar en minutos
- **[API AiClient](/rust/client/)** — Detalles de uso del cliente
- **[Canalización de streaming](/rust/streaming/)** — Profundice en la canalización
- **[Resiliencia](/rust/resilience/)** — Patrones de confiabilidad
