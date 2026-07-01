---
title: Introducci贸n
description: Visi贸n general del ecosistema AI-Lib 鈥?especificaci贸n AI-Protocol y sus implementaciones runtime en Rust, Python, TypeScript y Go.
---

# Bienvenido a AI-Lib

**AI-Lib** es un ecosistema de c贸digo abierto que estandariza la forma en que las aplicaciones interact煤an con los modelos de IA. En lugar de escribir c贸digo espec铆fico de cada proveedor para cada servicio de IA, se utiliza una 煤nica API unificada 鈥?y la configuraci贸n del protocolo se encarga del resto.

## La idea central

> **Toda la l贸gica son operadores, toda la configuraci贸n es protocolo.**

Los SDKs de IA tradicionales incorporan l贸gica espec铆fica del proveedor en el c贸digo: diferentes endpoints HTTP, diferentes nombres de par谩metros, diferentes formatos de streaming, diferentes c贸digos de error. Al cambiar de proveedor, hay que reescribir c贸digo.

AI-Lib adopta un enfoque diferente:

- **AI-Protocol** define c贸mo comunicarse con cada proveedor en manifiestos YAML
- **Implementaciones en tiempo de ejecuci贸n** (Rust, Python, TypeScript, Go) leen estos manifiestos y ejecutan las solicitudes
- **L贸gica sin codificar** 鈥?ninguna rama `if provider == "openai"` en ning煤n lugar

## Seis proyectos, un ecosistema

| Project                       | Role                   | Language   | Version | Distribution                                                     |
| ----------------------------- | ---------------------- | ---------- | ------- | ---------------------------------------------------------------- |
| **[AI-Protocol](/protocol/)** | Capa de especificaci贸n | YAML/JSON  | v1.0.0  | [npm](https://www.npmjs.com/package/@ailib-official/ai-protocol) 路 GitHub |
| **[ai-lib-rust](/rust/)**     | Implementaci贸n runtime | Rust       | v1.0.0  | [Crates.io](https://crates.io/crates/ai-lib-rust)                |
| **[ai-lib-python](/python/)** | Implementaci贸n runtime | Python     | v1.0.0  | [PyPI](https://pypi.org/project/ai-lib-python/)                  |
| **[ai-lib-ts](/ts/)**         | Implementaci贸n runtime | TypeScript | v1.0.0  | [npm](https://www.npmjs.com/package/@ailib-official/ai-lib-ts)       |
| **ai-lib-go**                 | Implementaci贸n runtime | Go         | v1.0.0  | [Go Modules](https://pkg.go.dev/github.com/ailib-official/ai-lib-go) |
| **ai-protocol-mock**          | Capa de mock/testing   | Python     | v1.0.0 | [PyPI](https://pypi.org/project/ai-protocol-mock/)               |

El ciclo actual de releases extiende V2 con gates de gobernanza ejecutable: `drift`, `manifest-consumption`, `compliance-matrix`, `fullchain` y `release-gate`, incluyendo modo `--report-only` para adopci贸n por etapas.

### AI-Protocol (Especificaci贸n)

La base. Los manifiestos YAML describen 37 proveedores de IA: sus endpoints, autenticaci贸n, mapeo de par谩metros, configuraciones de decodificador de streaming, reglas de clasificaci贸n de errores y capacidades. JSON Schema valida todo.

### ai-lib-rust (Tiempo de ejecuci贸n Rust)

Tiempo de ejecuci贸n de alto rendimiento. La canalizaci贸n de streaming basada en operadores procesa las respuestas a trav茅s de etapas composables (Decoder 鈫?Selector 鈫?Accumulator 鈫?EventMapper). Resiliencia integrada con circuit breaker, limitador de velocidad y backpressure. Publicado en Crates.io.

### ai-lib-python (Tiempo de ejecuci贸n Python)

Tiempo de ejecuci贸n orientado al desarrollador. Soporte completo async/await, seguridad de tipos con Pydantic v2, telemetr铆a de nivel producci贸n (OpenTelemetry + Prometheus) y enrutamiento inteligente de modelos. Publicado en PyPI.

### ai-lib-ts (Tiempo de ejecuci贸n TypeScript)

Runtime para Node.js/npm con parsing V2 de manifiestos, errores estandarizados, streaming y m贸dulos de resiliencia, alineado con la matriz de compliance de Rust/Python.

## Caracter铆sticas principales

- **37 proveedores** 鈥?OpenAI, Anthropic, Gemini, DeepSeek, Qwen y muchos m谩s
- **Streaming unificado** 鈥?Mismos tipos `StreamingEvent` independientemente del proveedor
- **Impulsado por protocolo** 鈥?Todo el comportamiento definido en YAML, no en c贸digo
- **Recarga en caliente** 鈥?Actualice configuraciones de proveedores sin reiniciar
- **Resiliencia** 鈥?Circuit breaker, limitaci贸n de velocidad, reintentos, fallback
- **Llamadas a herramientas** 鈥?Llamadas a funciones unificadas entre proveedores
- **Embeddings** 鈥?Operaciones vectoriales y b煤squeda de similitud
- **Seguridad de tipos** 鈥?Validaci贸n en tiempo de compilaci贸n (Rust) y en tiempo de ejecuci贸n (Pydantic)

## Pr贸ximos pasos

- **[Inicio r谩pido](/quickstart/)** 鈥?Empiece en minutos
- **[Arquitectura del ecosistema](/ecosystem/)** 鈥?Comprenda c贸mo encajan las piezas
- **[AI-Protocol](/protocol/overview/)** 鈥?Profundice en la especificaci贸n
- **[SDK Rust](/rust/overview/)** 鈥?Comience con Rust
- **[SDK Python](/python/overview/)** 鈥?Comience con Python
- **[SDK TypeScript](/ts/overview/)** 鈥?Comience con TypeScript
