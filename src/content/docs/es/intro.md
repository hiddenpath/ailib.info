---
title: Introducción
description: Visión general del ecosistema AI-Lib — especificación AI-Protocol y sus implementaciones runtime en Rust, Python, TypeScript y Go.
---

# Bienvenido a AI-Lib

**AI-Lib** es un ecosistema de código abierto que estandariza la forma en que las aplicaciones interactúan con los modelos de IA. En lugar de escribir código específico de cada proveedor para cada servicio de IA, se utiliza una única API unificada — y la configuración del protocolo se encarga del resto.

## La idea central

> **Toda la lógica son operadores, toda la configuración es protocolo.**

Los SDKs de IA tradicionales incorporan lógica específica del proveedor en el código: diferentes endpoints HTTP, diferentes nombres de parámetros, diferentes formatos de streaming, diferentes códigos de error. Al cambiar de proveedor, hay que reescribir código.

AI-Lib adopta un enfoque diferente:

- **AI-Protocol** define cómo comunicarse con cada proveedor en manifiestos YAML
- **Implementaciones en tiempo de ejecución** (Rust, Python, TypeScript, Go) leen estos manifiestos y ejecutan las solicitudes
- **Lógica sin codificar** — ninguna rama `if provider == "openai"` en ningún lugar

## Seis proyectos, un ecosistema

| Project                       | Role                   | Language   | Version | Distribution                                                     |
| ----------------------------- | ---------------------- | ---------- | ------- | ---------------------------------------------------------------- |
| **[AI-Protocol](/protocol/)** | Capa de especificación | YAML/JSON  | v0.8.3  | GitHub                                                           |
| **[ai-lib-rust](/rust/)**     | Implementación runtime | Rust       | v0.9.3  | [Crates.io](https://crates.io/crates/ai-lib-rust)                |
| **[ai-lib-python](/python/)** | Implementación runtime | Python     | v0.8.3  | [PyPI](https://pypi.org/project/ai-lib-python/)                  |
| **[ai-lib-ts](/ts/)**         | Implementación runtime | TypeScript | v0.5.3  | [npm](https://www.npmjs.com/package/@hiddenpath/ai-lib-ts)       |
| **ai-lib-go**                 | Implementación runtime | Go         | v0.0.1  | [Go Modules](https://pkg.go.dev/github.com/hiddenpath/ai-lib-go) |
| **ai-protocol-mock**          | Capa de mock/testing   | Python     | v0.1.11 | [PyPI](https://pypi.org/project/ai-protocol-mock/)               |

El ciclo actual de releases extiende V2 con gates de gobernanza ejecutable: `drift`, `manifest-consumption`, `compliance-matrix`, `fullchain` y `release-gate`, incluyendo modo `--report-only` para adopción por etapas.

### AI-Protocol (Especificación)

La base. Los manifiestos YAML describen 37 proveedores de IA: sus endpoints, autenticación, mapeo de parámetros, configuraciones de decodificador de streaming, reglas de clasificación de errores y capacidades. JSON Schema valida todo.

### ai-lib-rust (Tiempo de ejecución Rust)

Tiempo de ejecución de alto rendimiento. La canalización de streaming basada en operadores procesa las respuestas a través de etapas composables (Decoder → Selector → Accumulator → EventMapper). Resiliencia integrada con circuit breaker, limitador de velocidad y backpressure. Publicado en Crates.io.

### ai-lib-python (Tiempo de ejecución Python)

Tiempo de ejecución orientado al desarrollador. Soporte completo async/await, seguridad de tipos con Pydantic v2, telemetría de nivel producción (OpenTelemetry + Prometheus) y enrutamiento inteligente de modelos. Publicado en PyPI.

### ai-lib-ts (Tiempo de ejecución TypeScript)

Runtime para Node.js/npm con parsing V2 de manifiestos, errores estandarizados, streaming y módulos de resiliencia, alineado con la matriz de compliance de Rust/Python.

## Características principales

- **37 proveedores** — OpenAI, Anthropic, Gemini, DeepSeek, Qwen y muchos más
- **Streaming unificado** — Mismos tipos `StreamingEvent` independientemente del proveedor
- **Impulsado por protocolo** — Todo el comportamiento definido en YAML, no en código
- **Recarga en caliente** — Actualice configuraciones de proveedores sin reiniciar
- **Resiliencia** — Circuit breaker, limitación de velocidad, reintentos, fallback
- **Llamadas a herramientas** — Llamadas a funciones unificadas entre proveedores
- **Embeddings** — Operaciones vectoriales y búsqueda de similitud
- **Seguridad de tipos** — Validación en tiempo de compilación (Rust) y en tiempo de ejecución (Pydantic)

## Próximos pasos

- **[Inicio rápido](/quickstart/)** — Empiece en minutos
- **[Arquitectura del ecosistema](/ecosystem/)** — Comprenda cómo encajan las piezas
- **[AI-Protocol](/protocol/overview/)** — Profundice en la especificación
- **[SDK Rust](/rust/overview/)** — Comience con Rust
- **[SDK Python](/python/overview/)** — Comience con Python
- **[SDK TypeScript](/ts/overview/)** — Comience con TypeScript
