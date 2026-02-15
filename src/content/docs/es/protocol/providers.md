---
title: Manifiestos de proveedores
description: Cómo funcionan los manifiestos de proveedores de AI-Protocol — configuración de endpoints, autenticación, mapeo de parámetros, streaming y manejo de errores.
---

# Manifiestos de proveedores

Cada proveedor de IA del ecosistema tiene un archivo de manifiesto YAML (`v1/providers/<provider>.yaml`) que describe completamente cómo interactuar con su API.

## Proveedores compatibles

Los manifiestos de proveedores están disponibles en dos formatos: **v1** (heredado) y **v2-alpha**. El formato v2-alpha utiliza la estructura concéntrica Anillo 1/2/3 (Esqueleto principal → Mapeo de capacidades → Extensiones avanzadas). **OpenAI, Anthropic y Gemini** están disponibles en formatos v1 y v2-alpha.

### Proveedores globales

OpenAI, Anthropic, Google Gemini, Groq, Mistral, Cohere, Perplexity, Together AI, DeepInfra, OpenRouter, Azure OpenAI, NVIDIA, Fireworks AI, Replicate, AI21 Labs, Cerebras, Lepton AI, Grok

### Proveedores de la región China

DeepSeek, Qwen (Alibaba), Zhipu GLM, Doubao (ByteDance), Baidu ERNIE, iFlytek Spark, Tencent Hunyuan, SenseNova, Tiangong, Moonshot (Kimi), MiniMax, Baichuan, Yi (01.AI), SiliconFlow

## Estructura del manifiesto

### Configuración del endpoint

```yaml
endpoint:
  base_url: "https://api.openai.com/v1"
  chat_path: "/chat/completions"
  protocol: "https"
  timeout_ms: 60000
```

### Autenticación

Soporta múltiples tipos de autenticación:

```yaml
# Bearer token (más común)
auth:
  type: bearer
  token_env: "OPENAI_API_KEY"

# API key en encabezado
auth:
  type: api_key
  header: "x-api-key"
  token_env: "ANTHROPIC_API_KEY"

# Encabezados personalizados
auth:
  type: bearer
  token_env: "ANTHROPIC_API_KEY"
  headers:
    anthropic-version: "2023-06-01"
```

### Mapeo de parámetros

Mapea nombres de parámetros estándar a campos específicos del proveedor:

```yaml
parameter_mappings:
  temperature: "temperature"
  max_tokens: "max_completion_tokens"  # OpenAI usa nombre diferente
  stream: "stream"
  tools: "tools"
  tool_choice: "tool_choice"
  response_format: "response_format"
```

### Configuración de streaming

Declara cómo decodificar e interpretar las respuestas en streaming:

```yaml
streaming:
  decoder:
    format: "sse"              # "sse", "ndjson", o "anthropic_sse"
    done_signal: "[DONE]"      # Marcador de terminación del flujo
  event_map:
    - match: "$.choices[0].delta.content"
      emit: "PartialContentDelta"
      extract:
        content: "$.choices[0].delta.content"
    - match: "$.choices[0].delta.tool_calls"
      emit: "PartialToolCall"
      extract:
        tool_calls: "$.choices[0].delta.tool_calls"
    - match: "$.choices[0].finish_reason"
      emit: "StreamEnd"
      extract:
        finish_reason: "$.choices[0].finish_reason"
```

### Clasificación de errores

Mapea respuestas HTTP a tipos de error estándar:

```yaml
error_classification:
  by_http_status:
    "400": "invalid_request"
    "401": "authentication"
    "403": "permission"
    "404": "not_found"
    "429": "rate_limited"
    "500": "server_error"
    "503": "overloaded"
  by_error_code:
    "context_length_exceeded": "context_length"
    "content_filter": "content_filter"
```

### Capacidades

Banderas de características que los tiempos de ejecución verifican antes de realizar solicitudes:

```yaml
capabilities:
  streaming: true
  tools: true
  vision: true
  audio: false
  reasoning: true
  agentic: true
  json_mode: true
```

## Cómo los tiempos de ejecución usan los manifiestos

1. **Cargar** — Leer manifiesto YAML (local, variable de entorno o GitHub)
2. **Validar** — Verificar contra JSON Schema
3. **Compilar** — Convertir solicitud del usuario usando mapeos de parámetros
4. **Ejecutar** — Enviar solicitud HTTP con autenticación/encabezados correctos
5. **Decodificar** — Procesar respuesta usando configuración de streaming
6. **Clasificar** — Manejar errores usando reglas de clasificación

## Próximos pasos

- **[Registro de modelos](/protocol/models/)** — Cómo se configuran los modelos
- **[Contribuir proveedores](/protocol/contributing/)** — Agregar un nuevo proveedor
