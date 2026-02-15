---
title: Visión general de AI-Protocol
description: Comprensión de la especificación AI-Protocol — la base independiente del proveedor del ecosistema AI-Lib.
---

# Visión general de AI-Protocol

AI-Protocol es una **especificación independiente del proveedor** que estandariza las interacciones con los modelos de IA. Separa lo que los tiempos de ejecución necesitan saber sobre un proveedor (configuración) de cómo ejecutan las solicitudes (código).

## Filosofía central

> **Toda la lógica son operadores, toda la configuración es protocolo.**

Cada comportamiento específico del proveedor — endpoints, autenticación, nombres de parámetros, formatos de streaming, códigos de error — se declara en archivos de configuración YAML. Las implementaciones en tiempo de ejecución contienen **lógica de proveedor sin codificar**.

## Contenido del repositorio

```
ai-protocol/
├── v1/
│   ├── spec.yaml          # Core specification (v0.5.0)
│   ├── providers/          # 30+ provider manifests
│   │   ├── openai.yaml
│   │   ├── anthropic.yaml
│   │   ├── gemini.yaml
│   │   ├── deepseek.yaml
│   │   └── ...
│   └── models/             # Model instance registry
│       ├── gpt.yaml
│       ├── claude.yaml
│       └── ...
├── schemas/                # JSON Schema validation
│   ├── v1.json
│   └── spec.json
├── dist/                   # Pre-compiled JSON (generated)
├── scripts/                # Build & validation tools
└── examples/               # Usage examples
```

## Manifiestos de proveedores

Cada proveedor tiene un manifiesto YAML que declara todo lo que un tiempo de ejecución necesita:

| Section | Purpose |
|---------|---------|
| `endpoint` | URL base, ruta de chat, protocolo |
| `auth` | Tipo de autenticación, variable de entorno del token, encabezados |
| `parameter_mappings` | Nombres de parámetros estándar → específicos del proveedor |
| `streaming` | Formato del decodificador (SSE/NDJSON), reglas de mapeo de eventos (JSONPath) |
| `error_classification` | Código de estado HTTP → tipos de error estándar |
| `retry_policy` | Estrategia, retardos, condiciones de reintento |
| `rate_limit_headers` | Nombres de encabezados para información de límite de velocidad |
| `capabilities` | Banderas de características (streaming, tools, vision, reasoning) |

### Ejemplo: Proveedor Anthropic

```yaml
id: anthropic
protocol_version: "0.5"
endpoint:
  base_url: "https://api.anthropic.com/v1"
  chat_path: "/messages"
auth:
  type: bearer
  token_env: "ANTHROPIC_API_KEY"
  headers:
    anthropic-version: "2023-06-01"
parameter_mappings:
  temperature: "temperature"
  max_tokens: "max_tokens"
  stream: "stream"
  tools: "tools"
streaming:
  decoder:
    format: "anthropic_sse"
  event_map:
    - match: "$.type == 'content_block_delta'"
      emit: "PartialContentDelta"
      extract:
        content: "$.delta.text"
    - match: "$.type == 'message_stop'"
      emit: "StreamEnd"
error_classification:
  by_http_status:
    "429": "rate_limited"
    "401": "authentication"
    "529": "overloaded"
capabilities:
  streaming: true
  tools: true
  vision: true
  reasoning: true
```

## Registro de modelos

Los modelos se registran con referencias de proveedores, capacidades y precios:

```yaml
models:
  claude-3-5-sonnet:
    provider: anthropic
    model_id: "claude-3-5-sonnet-20241022"
    context_window: 200000
    capabilities: [chat, vision, tools, streaming, reasoning]
    pricing:
      input_per_token: 0.000003
      output_per_token: 0.000015
```

## Validación

Todos los manifiestos se validan contra JSON Schema (2020-12) usando AJV. Las canalizaciones CI hacen cumplir la corrección:

```bash
npm run validate    # Validate all configurations
npm run build       # Compile YAML → JSON
```

## Versionado

AI-Protocol utiliza versionado en capas:

1. **Versión de la especificación** (`v1/spec.yaml`) — Versión de la estructura del esquema (actualmente v0.5.0)
2. **Versión del protocolo** (en manifiestos) — Características del protocolo utilizadas (actualmente 0.5)
3. **Versión de lanzamiento** (`package.json`) — SemVer para el paquete de especificación (v0.5.0)

## Arquitectura del protocolo V2

La versión v0.5.0 del protocolo introduce la **arquitectura V2** — una separación limpia de responsabilidades entre capas y un modelo de manifiesto concéntrico.

### Pirámide de tres capas

- **L1 Protocolo principal** — Formato de mensaje, códigos de error estándar (E1001–E9999), declaración de versión. Todos los proveedores deben implementar esta capa.
- **L2 Extensiones de capacidades** — Streaming, visión, herramientas. Cada extensión se controla por banderas de características; los proveedores optan por cada capacidad.
- **L3 Perfil de entorno** — Claves API, endpoints, políticas de reintento. Configuración específica del entorno que puede sobrescribirse sin cambiar la lógica del proveedor.

### Modelo de manifiesto concéntrico

- **Anillo 1 Esqueleto principal** (obligatorio) — Campos mínimos para un manifiesto válido: endpoint, auth, parameter mappings
- **Anillo 2 Mapeo de capacidades** (condicional) — Config de streaming, mapeo de tools, parámetros de visión — presente cuando el proveedor los soporta
- **Anillo 3 Extensiones avanzadas** (opcional) — Encabezados personalizados, encabezados de límite de velocidad, políticas de reintento avanzadas

### Proveedores V2-Alpha

OpenAI, Anthropic y Gemini ya están disponibles en formato **v2-alpha**. Estos manifiestos utilizan la estructura Anillo 1/2/3 y pueden usarse junto con manifiestos v1.

### Códigos de error estándar

V2 define 13 códigos de error estandarizados (E1001–E9999) en 5 categorías: errores de cliente (E1xxx), tasa/cuota (E2xxx), servidor (E3xxx), conflicto/cancelación (E4xxx) y desconocido (E9999). Consulte la [especificación](/protocol/spec/) para la lista completa de códigos.

### Consistencia entre tiempos de ejecución

Un **conjunto de pruebas de conformidad** garantiza un comportamiento idéntico entre los tiempos de ejecución Rust y Python. Todos los proveedores V2 pasan la misma matriz de pruebas en ambas implementaciones.

## Próximos pasos

- **[Detalles de la especificación](/protocol/spec/)** — Profundice en la especificación principal
- **[Manifiestos de proveedores](/protocol/providers/)** — Cómo funcionan los manifiestos
- **[Registro de modelos](/protocol/models/)** — Configuración de modelos
- **[Contribuir proveedores](/protocol/contributing/)** — Agregar un nuevo proveedor
