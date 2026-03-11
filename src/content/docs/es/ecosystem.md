---
title: Arquitectura del ecosistema
description: Cómo AI-Protocol, ai-lib-rust, ai-lib-python, ai-lib-ts y ai-lib-go funcionan juntos como un ecosistema integrado.
---

# Arquitectura del ecosistema

El ecosistema AI-Lib se basa en una arquitectura limpia de tres capas donde cada capa tiene una responsabilidad distinta. Versiones actuales: **AI-Protocol v0.8.3**, **ai-lib-rust v0.9.3**, **ai-lib-python v0.8.3**, **ai-lib-ts v0.5.3**, **ai-lib-go v0.0.1**, **ai-protocol-mock v0.1.11**.

## Las tres capas

### 1. Capa de protocolo — AI-Protocol

La capa de **especificación**. Los manifiestos YAML definen:

- **Manifiestos de proveedores** (`providers/*.yaml`) — Endpoint, autenticación, mapeo de parámetros, decodificador de streaming, clasificación de errores para cada uno de los 37 proveedores
- **Registro de modelos** (`models/*.yaml`) — Instancias de modelos con ventanas de contexto, capacidades y precios
- **Especificación principal** (`spec.yaml`) — Parámetros estándar, eventos, tipos de error, políticas de reintento
- **Esquemas** (`schemas/`) — Validación JSON Schema para toda la configuración

La capa de protocolo es **independiente del lenguaje**. Cualquier tiempo de ejecución en cualquier lenguaje la consume.

### 2. Capa de tiempo de ejecución — SDKs Rust, Python, TypeScript y Go

La capa de **ejecución**. Los tiempos de ejecución implementan:

- **Carga de protocolo** — Lectura y validación de manifiestos desde archivos locales, variables de entorno o GitHub
- **Compilación de solicitudes** — Conversión de solicitudes unificadas a llamadas HTTP específicas del proveedor
- **Canalización de streaming** — Decodificación, selección, acumulación y mapeo de respuestas del proveedor a eventos unificados
- **Resiliencia** — Circuit breaker, limitación de velocidad, reintentos, fallback
- **Extensiones** — Embeddings, caché, procesamiento por lotes, plugins

Los tres runtimes comparten la misma arquitectura impulsada por protocolo:

| Concepto | Rust | Python | TypeScript |
|----------|------|--------|------------|
| Cliente | `AiClient` | `AiClient` | `AiClient` |
| Constructor | `AiClientBuilder` | `AiClientBuilder` | `AiClientBuilder` |
| Solicitud | `ChatRequestBuilder` | `ChatRequestBuilder` | `ChatBuilder` |
| Eventos | Enumeración `StreamingEvent` | Clase `StreamingEvent` | eventos unificados de streaming |
| Transporte | reqwest (tokio) | httpx (asyncio) | fetch (Node.js) |
| Tipos | Estructuras Rust | Modelos Pydantic v2 | interfaces TypeScript |

### 3. Capa de aplicación — Su código

Las aplicaciones utilizan la API unificada del tiempo de ejecución. Una única interfaz `AiClient` funciona con todos los proveedores:

```
Your App → AiClient → Protocol Manifest → Provider API
```

Cambie de proveedor modificando un solo identificador de modelo. Sin cambios de código.

## Flujo de datos

Esto es lo que ocurre cuando llama a `client.chat().user("Hello").stream()`:

1. **AiClient** recibe la solicitud
2. **ProtocolLoader** proporciona el manifiesto del proveedor
3. **Compilador de solicitudes** mapea los parámetros estándar al JSON específico del proveedor
4. **Transporte** envía la solicitud HTTP con autenticación/encabezados correctos
5. **Canalización** procesa la respuesta en streaming:
   - **Decoder** convierte bytes → frames JSON (SSE o NDJSON)
   - **Selector** filtra los frames relevantes mediante expresiones JSONPath
   - **Accumulator** ensambla las llamadas a herramientas parciales
   - **EventMapper** convierte frames → `StreamingEvent` unificados
6. **Aplicación** itera sobre los eventos unificados

## Carga del protocolo

Los tres runtimes buscan manifiestos del protocolo en este orden:

1. **Ruta personalizada** — Establecida explícitamente en el constructor
2. **Variable de entorno** — `AI_PROTOCOL_DIR` o `AI_PROTOCOL_PATH`
3. **Rutas relativas** — `ai-protocol/` o `../ai-protocol/` desde el directorio de trabajo
4. **Respaldo GitHub** — Descarga desde el repositorio `hiddenpath/ai-protocol`

Esto significa que puede comenzar a desarrollar sin ninguna configuración local — los tiempos de ejecución obtendrán los manifiestos de GitHub automáticamente.

## Evolución del protocolo V2 y mejoras de gobernanza

La base V2 se amplía en `v0.8.2` con cierre de gobernanza fullchain para capacidades generativas:

- **L1 Protocolo principal** — Formato de mensaje, códigos de error estándar (E1001–E9999), declaración de versión
- **L2 Extensiones de capacidades** — Streaming, visión, herramientas, MCP, Computer Use y multimodal
- **L3 Perfil de entorno** — Claves API, endpoints, políticas de reintento — configuración específica del entorno

Scripts de gate de gobernanza ahora disponibles:

- `npm run drift:check`
- `npm run gate:manifest-consumption`
- `npm run gate:compliance-matrix`
- `npm run gate:fullchain`
- `npm run release:gate`

También soportan modo `--report-only` para adopción gradual sin bloqueo inmediato.

El ciclo async de video en `ai-protocol-mock` soporta estados terminales deterministas `succeeded` / `failed` / `cancelled`, controlados por `X-Mock-Video-Terminal` o `terminal_state`.

La matriz de compliance entre Rust/Python/TypeScript cubre protocol loading, error classification, retry, message, stream y request.

## Relación con MCP

AI-Protocol y MCP (Model Context Protocol) son **complementarios**:

- **MCP** maneja aspectos de alto nivel — registro de herramientas, gestión de contexto, coordinación de agentes
- **AI-Protocol** maneja aspectos de bajo nivel — normalización de API, conversión de formato de streaming, clasificación de errores

Operan en capas diferentes y pueden usarse conjuntamente.

## Próximos pasos

- **[Visión general de AI-Protocol](/protocol/overview/)** — Profundice en la especificación
- **[SDK Rust](/rust/overview/)** — Explore el tiempo de ejecución Rust
- **[SDK Python](/python/overview/)** — Explore el tiempo de ejecución Python
- **[SDK TypeScript](/ts/overview/)** — Explore el tiempo de ejecución TypeScript
