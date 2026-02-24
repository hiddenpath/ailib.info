---
title: Llamadas a funciones
description: Guía para usar llamadas a funciones (uso de herramientas) con AI-Lib entre proveedores.
---

# Llamadas a funciones

Las llamadas a funciones (uso de herramientas) permiten que los modelos de IA invoquen funciones externas. AI-Lib proporciona una interfaz unificada para llamadas a herramientas en todos los proveedores que las soportan.

## Definir herramientas

### Rust

```rust
use ai_lib_rust::ToolDefinition;
use serde_json::json;

let get_weather = ToolDefinition {
    name: "get_weather".into(),
    description: Some("Get current weather for a city".into()),
    parameters: json!({
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City name"
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"]
            }
        },
        "required": ["city"]
    }),
};
```

### Python

```python
get_weather = {
    "name": "get_weather",
    "description": "Get current weather for a city",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "City name",
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
            },
        },
        "required": ["city"],
    },
}
```

### TypeScript

```typescript
import { ToolDefinition } from '@hiddenpath/ai-lib-ts';

const getWeather: ToolDefinition = {
  name: 'get_weather',
  description: 'Get current weather for a city',
  parameters: {
    type: 'object',
    properties: {
      city: {
        type: 'string',
        description: 'City name',
      },
      unit: {
        type: 'string',
        enum: ['celsius', 'fahrenheit'],
      },
    },
    required: ['city'],
  },
};
```

## Llamadas a herramientas sin streaming

### Rust

```rust
let response = client.chat()
    .user("What's the weather in Tokyo?")
    .tools(vec![get_weather])
    .execute()
    .await?;

for call in &response.tool_calls {
    println!("Function: {}", call.name);
    println!("Arguments: {}", call.arguments);
    // Execute the function and send results back
}
```

### Python

```python
response = await client.chat() \
    .user("What's the weather in Tokyo?") \
    .tools([get_weather]) \
    .execute()

for call in response.tool_calls:
    print(f"Function: {call.name}")
    print(f"Arguments: {call.arguments}")
```

### TypeScript

```typescript
const response = await client
  .chat()
  .user("What's the weather in Tokyo?")
  .tools([getWeather])
  .execute();

for (const call of response.toolCalls) {
  console.log(`Function: ${call.name}`);
  console.log(`Arguments: ${call.arguments}`);
}
```

## Llamadas a herramientas en streaming

Las llamadas a herramientas se transmiten como eventos parciales que el Accumulator de la canalización ensambla:

### Rust

```rust
let mut stream = client.chat()
    .user("What's the weather?")
    .tools(vec![get_weather])
    .stream()
    .execute_stream()
    .await?;

while let Some(event) = stream.next().await {
    match event? {
        StreamingEvent::ToolCallStarted { name, id, .. } => {
            println!("Starting tool: {name} (id: {id})");
        }
        StreamingEvent::PartialToolCall { arguments, .. } => {
            print!("{arguments}"); // Partial JSON arguments
        }
        StreamingEvent::ToolCallEnded { id, .. } => {
            println!("\nTool call {id} complete");
        }
        StreamingEvent::ContentDelta { text, .. } => {
            print!("{text}");
        }
        _ => {}
    }
}
```

### Python

```python
async for event in client.chat() \
    .user("What's the weather?") \
    .tools([get_weather]) \
    .stream():
    if event.is_tool_call_started:
        call = event.as_tool_call_started
        print(f"Starting: {call.name}")
    elif event.is_partial_tool_call:
        print(event.as_partial_tool_call.arguments, end="")
    elif event.is_content_delta:
        print(event.as_content_delta.text, end="")
```

### TypeScript

```typescript
for await (const event of client
  .chat()
  .user("What's the weather?")
  .tools([getWeather])
  .stream()) {
  if (event.isToolCallStarted) {
    const call = event.asToolCallStarted;
    console.log(`Starting: ${call.name}`);
  } else if (event.isPartialToolCall) {
    process.stdout.write(event.asPartialToolCall.arguments);
  } else if (event.isContentDelta) {
    process.stdout.write(event.asContentDelta.text);
  }
}
```

## Cómo funciona

1. Define herramientas y las pasa en la solicitud
2. El manifiesto del protocolo mapea `tools` al formato específico del proveedor
3. El modelo decide llamar a una herramienta (o responder con texto)
4. Para streaming, el **Accumulator** de la canalización ensambla los fragmentos parciales de llamadas a herramientas
5. Recibe eventos unificados `ToolCallStarted`, `PartialToolCall` y `ToolCallEnded`

## Soporte por proveedor

Verifique las capacidades del proveedor antes de usar herramientas:

| Provider | Tool Calling |
|----------|-------------|
| OpenAI | Supported |
| Anthropic | Supported |
| Gemini | Supported |
| DeepSeek | Supported |
| Groq | Supported |
| Mistral | Supported |
| Qwen | Supported |

La bandera `capabilities.tools: true` del manifiesto indica soporte.
