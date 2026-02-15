---
title: Visión general del SDK Python
description: Arquitectura y diseño de ai-lib-python — el tiempo de ejecución Python orientado al desarrollador para AI-Protocol.
---

# Visión general del SDK Python

**ai-lib-python** (v0.6.0) es el tiempo de ejecución Python oficial para AI-Protocol. Proporciona una interfaz totalmente asíncrona orientada al desarrollador con seguridad de tipos Pydantic v2 y telemetría de nivel producción.

## Arquitectura

El SDK Python refleja la arquitectura en capas del tiempo de ejecución Rust:

### Capa de cliente (`client/`)
- **AiClient** — Punto de entrada principal con métodos de fábrica
- **AiClientBuilder** — Constructor de configuración fluido
- **ChatRequestBuilder** — Construcción de solicitudes
- **ChatResponse** / **CallStats** — Tipos de respuesta
- **CancelToken** / **CancellableStream** — Cancelación de flujo

### Capa de protocolo (`protocol/`)
- **ProtocolLoader** — Carga manifiestos desde local/env/GitHub con caché
- **ProtocolManifest** — Modelos Pydantic para configuraciones de proveedores
- **Validator** — Validación JSON Schema (fastjsonschema)

### Capa de canalización (`pipeline/`)
- **Decoder** — Decodificadores SSE, JSON Lines, Anthropic SSE
- **Selector** — Selección de frames basada en JSONPath (jsonpath-ng)
- **Accumulator** — Ensamblaje de llamadas a herramientas
- **FanOut** — Expansión multicandidato
- **EventMapper** — Mapeadores impulsados por protocolo, Default y Anthropic

### Capa de transporte (`transport/`)
- **HttpTransport** — HTTP asíncrono basado en httpx con streaming
- **Auth** — Resolución de API key desde variables de entorno y keyring
- **ConnectionPool** — Pool de conexiones para rendimiento

### Capa de resiliencia (`resilience/`)
- **ResilientExecutor** — Combina todos los patrones
- **RetryPolicy** — Backoff exponencial
- **RateLimiter** — Token bucket
- **CircuitBreaker** — Aislamiento de fallos
- **Backpressure** — Limitación de concurrencia
- **FallbackChain** — Conmutación por error multiobjetivo
- **PreflightChecker** — Control unificado antes de la ejecución

### Capa de enrutamiento (`routing/`)
- **ModelManager** — Registro y selección de modelos
- **ModelArray** — Balanceo de carga entre endpoints
- **Estrategias de selección** — Round-robin, ponderado, basado en costo, basado en calidad

### Capa de telemetría (`telemetry/`)
- **MetricsCollector** — Exportación de métricas Prometheus
- **Tracer** — Trazado distribuido OpenTelemetry
- **Logger** — Registro estructurado
- **HealthChecker** — Monitoreo de salud del servicio
- **FeedbackCollector** — Retroalimentación del usuario

### Módulos adicionales
- **embeddings/** — EmbeddingClient con operaciones vectoriales
- **cache/** — Caché multibackend (memoria, disco)
- **tokens/** — TokenCounter (tiktoken) y estimación de costos
- **batch/** — BatchCollector/Executor con control de concurrencia
- **plugins/** — Base de plugins, registro, hooks, middleware
- **structured/** — Modo JSON, generación de esquemas, validación de salida
- **guardrails/** — Filtrado de contenido, validadores

## Dependencias principales

| Package | Propósito |
|---------|-----------|
| `httpx` | Cliente HTTP asíncrono |
| `pydantic` | Validación de datos y tipos |
| `pydantic-settings` | Gestión de configuración |
| `fastjsonschema` | Validación de manifiestos |
| `jsonpath-ng` | Expresiones JSONPath |
| `pyyaml` | Análisis de YAML |

### Opcional

| Extra | Paquetes |
|-------|----------|
| `[telemetry]` | OpenTelemetry, Prometheus |
| `[tokenizer]` | tiktoken |
| `[full]` | Todo lo anterior + watchdog, keyring |

## Alineación con el protocolo V2

v0.6.0 está alineado con la especificación AI-Protocol V2:

- **Códigos de error estándar** — 13 códigos dataclass congelados (E1001–E9999) en `errors/standard_codes.py`
- **Extras de capacidades** — 8 extras pip (vision, audio, embeddings, structured, batch, agentic, telemetry, tokenizer) más un meta-extra "full"
- **Pruebas de conformidad** — 20/20 casos de prueba entre tiempos de ejecución aprobados
- **Soporte de versiones del protocolo** — Soporta versiones de protocolo 1.0, 1.1, 1.5, 2.0

## Versión de Python

Requiere **Python 3.10+**.

## Próximos pasos

- **[Inicio rápido](/python/quickstart/)** — Comenzar rápidamente
- **[API AiClient](/python/client/)** — Guía detallada de la API
- **[Canalización de streaming](/python/streaming/)** — Internals de la canalización
- **[Resiliencia](/python/resilience/)** — Patrones de confiabilidad
