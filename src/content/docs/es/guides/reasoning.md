---
title: Modelos de razonamiento
description: Uso de modelos de pensamiento extendido y razonamiento con AI-Lib.
---

# Modelos de razonamiento

Algunos modelos de IA soportan pensamiento extendido (razonamiento cadena de pensamiento), donde el modelo muestra su proceso de razonamiento antes de proporcionar la respuesta final.

## Modelos compatibles

| Model | Provider | Reasoning |
|-------|----------|-----------|
| o1, o1-mini, o3 | OpenAI | Extended thinking |
| Claude 3.5 Sonnet | Anthropic | Extended thinking |
| DeepSeek R1 | DeepSeek | Chain-of-thought |
| Gemini 2.0 Flash Thinking | Google | Thinking mode |

## Uso

Los modelos de razonamiento funcionan a través de la misma API. La diferencia clave es que pueden emitir eventos `ThinkingDelta` durante el streaming:

### Rust

```rust
let mut stream = client.chat()
    .user("Solve this step by step: What is 127 * 43?")
    .stream()
    .execute_stream()
    .await?;

while let Some(event) = stream.next().await {
    match event? {
        StreamingEvent::ThinkingDelta { text, .. } => {
            // Model's reasoning process
            print!("[thinking] {text}");
        }
        StreamingEvent::ContentDelta { text, .. } => {
            // Final answer
            print!("{text}");
        }
        _ => {}
    }
}
```

### Python

```python
async for event in client.chat() \
    .user("Solve this step by step: What is 127 * 43?") \
    .stream():
    if event.is_thinking_delta:
        print(f"[thinking] {event.text}", end="")
    elif event.is_content_delta:
        print(event.as_content_delta.text, end="")
```

### TypeScript

```typescript
for await (const event of client
  .chat()
  .user('Solve this step by step: What is 127 * 43?')
  .stream()) {
  if (event.isThinkingDelta) {
    process.stdout.write(`[thinking] ${event.text}`);
  } else if (event.isContentDelta) {
    process.stdout.write(event.asContentDelta.text);
  }
}
```

## Cómo funciona

1. El manifiesto del proveedor declara `capabilities.reasoning: true`
2. El decodificador de streaming reconoce eventos específicos de pensamiento
3. El EventMapper emite `ThinkingDelta` para contenido de razonamiento
4. Los eventos `ContentDelta` contienen la respuesta final

El manifiesto del protocolo maneja las diferencias de formato específicas del proveedor:

- **OpenAI o1**: Usa tokens de razonamiento internos
- **Anthropic Claude**: Usa bloques de contenido `thinking`
- **DeepSeek R1**: Usa etiquetas `<think>` en el contenido

## Consejos

- Los modelos de razonamiento generalmente producen mejores resultados para tareas complejas
- Utilizan más tokens (los tokens de razonamiento se cuentan)
- La temperatura puede estar restringida (algunos modelos de razonamiento la ignoran)
- No todos los proveedores soportan razonamiento — verifique `capabilities.reasoning`
