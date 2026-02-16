---
title: Contribuir proveedores
description: Guía paso a paso para agregar un nuevo proveedor de IA a la especificación AI-Protocol.
---

# Contribuir un proveedor

Agregar un nuevo proveedor de IA a AI-Protocol lo hace disponible instantáneamente en todos los tiempos de ejecución (Rust, Python y cualquier implementación futura).

## Pasos

> **Formato v2-alpha**: La versión v0.7.0 del protocolo introduce el formato de proveedor v2-alpha con la estructura de manifiesto Anillo 1/2/3. Los nuevos proveedores pueden opcionalmente orientarse a v2-alpha para códigos de error estandarizados, banderas de características y extensiones de capacidades. Consulte la [Visión general del protocolo](/protocol/overview/) para detalles de la arquitectura V2.

### 1. Investigar la API del proveedor

Documente lo siguiente sobre el proveedor:

- URL base y ruta del endpoint de chat
- Método de autenticación (Bearer token, API key en encabezado, etc.)
- Formato de parámetros de solicitud
- Formato de respuesta en streaming (SSE, NDJSON, personalizado)
- Estructura de respuesta de error
- Modelos disponibles y sus capacidades

### 2. Crear el manifiesto del proveedor

Cree `v1/providers/<provider-id>.yaml`:

```yaml
id: <provider-id>
name: "<Provider Name>"
protocol_version: "1.5"

endpoint:
  base_url: "https://api.example.com/v1"
  chat_path: "/chat/completions"

auth:
  type: bearer
  token_env: "<PROVIDER_ID>_API_KEY"

parameter_mappings:
  temperature: "temperature"
  max_tokens: "max_tokens"
  stream: "stream"
  tools: "tools"

streaming:
  decoder:
    format: "sse"
    done_signal: "[DONE]"
  event_map:
    - match: "$.choices[0].delta.content"
      emit: "PartialContentDelta"
      extract:
        content: "$.choices[0].delta.content"

error_classification:
  by_http_status:
    "401": "authentication"
    "429": "rate_limited"
    "500": "server_error"

capabilities:
  streaming: true
  tools: true
  vision: false
```

### 3. Agregar modelos

Cree o actualice `v1/models/<family>.yaml`:

```yaml
models:
  example-model:
    provider: <provider-id>
    model_id: "example-model-v1"
    context_window: 128000
    capabilities: [chat, streaming, tools]
    pricing:
      input_per_token: 0.000001
      output_per_token: 0.000002
```

### 4. Validar

```bash
npm run validate
```

Esto verifica su manifiesto contra JSON Schema y reporta cualquier error.

### 5. Compilar

```bash
npm run build
```

Esto compila su YAML a JSON en el directorio `dist/`.

### 6. Enviar una solicitud de extracción

- Haga un fork del repositorio
- Cree una rama
- Agregue su manifiesto de proveedor y entradas de modelos
- Asegúrese de que la validación pase
- Envíe un PR con documentación sobre el proveedor

## Reglas de validación

El JSON Schema exige:

- Campos obligatorios (`id`, `endpoint`, `auth`, `parameter_mappings`)
- Formatos válidos para URLs, nombres de variables de entorno
- Estructura correcta para configuración de streaming
- Tipos de clasificación de errores válidos
- Banderas de capacidad como booleanos

## Consejos

- Use el **formato compatible con OpenAI** si el proveedor sigue la estructura de la API OpenAI — muchos lo hacen (Groq, Together AI, DeepSeek)
- Pruebe cuidadosamente la configuración de streaming — aquí es donde existen la mayoría de las diferencias entre proveedores
- Incluya las banderas de `capabilities` con precisión — los tiempos de ejecución las usan para validación previa al vuelo
