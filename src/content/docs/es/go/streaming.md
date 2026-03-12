---
title: Canalización de streaming (Go)
description: Profundice en la canalización de streaming basada en operadores en ai-lib-go v0.5.0.
---

# Canalización de streaming

La canalización de streaming es el núcleo de ai-lib-go. Procesa las respuestas del proveedor a través de operadores composables, cada uno impulsado por la configuración del protocolo.

## Arquitectura de la canalización

```
Raw Bytes → Decoder → Selector → Accumulator → FanOut → EventMapper → StreamingEvent
```

Cada operador es una etapa en la canalización:

### 1. Decoder

Convierte flujos de bytes sin procesar en frames JSON.

| Format          | Description                             |
| --------------- | --------------------------------------- |
| `sse`           | Server-Sent Events (OpenAI, Groq, etc.) |
| `ndjson`        | JSON delimitado por líneas nuevas       |
| `anthropic_sse` | Formato SSE personalizado de Anthropic  |

El formato del decodificador se especifica en el manifiesto del proveedor:

```yaml
streaming:
  decoder:
    format: 'sse'
    done_signal: '[DONE]'
```

### 2. Selector

Filtra frames JSON usando expresiones JSONPath definidas en `event_map` del manifiesto:

```yaml
event_map:
  - match: '$.choices[0].delta.content'
    emit: 'PartialContentDelta'
```

### 3. Accumulator

Ensambla statefulmente las llamadas a herramientas parciales. Cuando un proveedor transmite argumentos de llamadas a herramientas en fragmentos, el accumulator los recopila en llamadas completas:

```
PartialToolCall("get_we") → PartialToolCall("ather") → PartialToolCall("(\"Tokyo\")")
```

### 4. FanOut

Maneja respuestas multicandidato (cuando `n > 1`). Expande candidatos en flujos de eventos separados.

### 5. EventMapper

La etapa final — convierte frames procesados en tipos `StreamingEvent` unificados.

## Construcción impulsada por protocolo

La canalización se construye automáticamente a partir del manifiesto del proveedor. No se necesita configuración manual:

```go
// La canalización se construye internamente basada en el manifiesto del protocolo
stream, err := aiClient.Chat().
    User("Hola").
    ExecuteStream(ctx)
if err != nil {
    panic(err)
}
defer stream.Close()

for stream.Next() {
    event := stream.Event()
    // Procesar evento
}
```

El tiempo de ejecución lee la sección `streaming` del manifiesto y conecta el decodificador apropiado, las reglas del selector y el mapeador de eventos.

## Operadores de reintento y fallback

La canalización también incluye operadores de resiliencia:

- **Retry** — Reintenta flujos fallidos según la política de reintento del manifiesto
- **Fallback** — Cambia a proveedores/modelos alternativos ante fallos

## Próximos pasos

- **[Resiliencia](/go/resilience/)** — Circuit breaker, limitador de velocidad
- **[Características avanzadas](/go/advanced/)** — Embeddings, caché, batch
