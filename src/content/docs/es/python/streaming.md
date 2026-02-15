---
title: Canalización de streaming (Python)
description: Cómo funciona la canalización de streaming en ai-lib-python v0.6.0 — decodificadores, selectores, acumuladores y mapeadores de eventos.
---

# Canalización de streaming

El SDK Python implementa la misma arquitectura de canalización basada en operadores que el tiempo de ejecución Rust, adaptada al ecosistema asíncrono de Python.

## Etapas de la canalización

```
Raw Bytes → Decoder → Selector → Accumulator → FanOut → EventMapper → StreamingEvent
```

### 1. Decoder

Convierte bytes de respuesta HTTP en frames JSON:

| Decoder Class | Provider Format |
|--------------|----------------|
| `SseDecoder` | SSE estándar (OpenAI, Groq, etc.) |
| `JsonLinesDecoder` | JSON delimitado por líneas nuevas |
| `AnthropicSseDecoder` | SSE personalizado de Anthropic |

El decodificador se selecciona según `streaming.decoder.format` del manifiesto.

### 2. Selector

Filtra frames JSON usando expresiones JSONPath del manifiesto:

```python
# Internally, the pipeline creates selectors from manifest rules:
# match: "$.choices[0].delta.content" → emit: "PartialContentDelta"
```

Utiliza `jsonpath-ng` para la evaluación de expresiones JSONPath.

### 3. Accumulator

Ensambla llamadas a herramientas parciales en invocaciones completas:

```python
# Provider streams:
#   {"tool_calls": [{"index": 0, "function": {"arguments": '{"ci'}}]}
#   {"tool_calls": [{"index": 0, "function": {"arguments": 'ty":"T'}}]}
#   {"tool_calls": [{"index": 0, "function": {"arguments": 'okyo"}'}}]}
# Accumulator produces complete: {"city": "Tokyo"}
```

### 4. FanOut

Para respuestas multicandidato (`n > 1`), expande en flujos por candidato.

### 5. EventMapper

Tres implementaciones de mapeador:

| Mapper | Description |
|--------|-------------|
| `ProtocolEventMapper` | Usa reglas event_map del manifiesto (JSONPath → tipo de evento) |
| `DefaultEventMapper` | Respaldo para proveedores compatibles con OpenAI |
| `AnthropicEventMapper` | Maneja la estructura de eventos única de Anthropic |

## Iteración asíncrona

La canalización expone los eventos como un iterador asíncrono:

```python
async for event in client.chat().user("Hello").stream():
    if event.is_content_delta:
        text = event.as_content_delta.text
        print(text, end="")
    elif event.is_tool_call_started:
        call = event.as_tool_call_started
        print(f"\nTool: {call.name}")
    elif event.is_stream_end:
        end = event.as_stream_end
        print(f"\nFinish: {end.finish_reason}")
```

## Cancelación

Los flujos soportan cancelación elegante:

```python
from ai_lib_python import CancelToken

token = CancelToken()

async for event in client.chat().user("...").stream(cancel_token=token):
    # Cancel after receiving enough content
    if total_chars > 1000:
        token.cancel()
        break
```

## Próximos pasos

- **[Resiliencia](/python/resilience/)** — Patrones de confiabilidad
- **[Características avanzadas](/python/advanced/)** — Telemetría, enrutamiento, plugins
