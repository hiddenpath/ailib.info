---
title: Registro de modelos
description: Cómo el registro de modelos de AI-Protocol mapea identificadores de modelos a configuraciones de proveedores con capacidades y precios.
---

# Registro de modelos

El registro de modelos (`v1/models/*.yaml`) mapea identificadores de modelos a configuraciones de proveedores, registrando capacidades, ventanas de contexto y precios para cada modelo.

## Estructura de archivos de modelos

Los modelos se organizan por familia (GPT, Claude, Gemini, etc.):

```
v1/models/
├── gpt.yaml          # OpenAI GPT models
├── claude.yaml        # Anthropic Claude models
├── gemini.yaml        # Google Gemini models
├── deepseek.yaml      # DeepSeek models
├── qwen.yaml          # Alibaba Qwen models
├── mistral.yaml       # Mistral models
├── llama.yaml         # Meta Llama models
└── ...                # 28+ model files
```

## Definición de modelo

Cada entrada de modelo incluye:

```yaml
models:
  gpt-4o:
    provider: openai
    model_id: "gpt-4o"
    context_window: 128000
    max_output_tokens: 16384
    capabilities:
      - chat
      - streaming
      - tools
      - vision
      - json_mode
    pricing:
      input_per_token: 0.0000025
      output_per_token: 0.00001
    release_date: "2024-05-13"
```

## Identificadores de modelos

Los tiempos de ejecución usan un formato `provider/model` para identificar modelos:

```
anthropic/claude-3-5-sonnet
openai/gpt-4o
deepseek/deepseek-chat
gemini/gemini-2.0-flash
qwen/qwen-plus
```

El tiempo de ejecución divide esto en:
1. **ID del proveedor** (`anthropic`) → carga el manifiesto del proveedor
2. **Nombre del modelo** (`claude-3-5-sonnet`) → busca en el registro de modelos

## Capacidades

Banderas de capacidad estándar:

| Capability | Description |
|-----------|-------------|
| `chat` | Completaciones de chat básicas |
| `streaming` | Respuestas en streaming |
| `tools` | Llamadas a funciones/herramientas |
| `vision` | Comprensión de imágenes |
| `audio` | Entrada/salida de audio |
| `reasoning` | Pensamiento extendido (CoT) |
| `agentic` | Flujos de trabajo de agentes multietapa |
| `json_mode` | Salida JSON estructurada |

## Precios

El precio por token permite la estimación de costos en los tiempos de ejecución:

```yaml
pricing:
  input_per_token: 0.000003      # $3 por 1M tokens de entrada
  output_per_token: 0.000015     # $15 por 1M tokens de salida
  cached_input_per_token: 0.0000003  # Descuento de prompt en caché
```

Ambos tiempos de ejecución Rust y Python utilizan estos datos para cálculos de `CostEstimate`.

## Verificación

Los modelos pueden incluir estado de verificación para despliegues en producción:

```yaml
verification:
  status: "verified"
  last_checked: "2025-01-15"
  verified_capabilities:
    - chat
    - streaming
    - tools
```

## Próximos pasos

- **[Contribuir proveedores](/protocol/contributing/)** — Agregar nuevos proveedores y modelos
- **[Inicio rápido](/quickstart/)** — Comenzar a usar modelos con los tiempos de ejecución
