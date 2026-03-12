---
title: Function Calling
description: Guide to using function calling (tool use) with AI-Lib across providers.
---

# Function Calling

Function calling (tool use) lets AI models invoke external functions. AI-Lib provides a unified interface for tool calling across all providers that support it.

## Defining Tools

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

### Go

```go
import "github.com/hiddenpath/ai-lib-go/client"

getWeather := client.ToolDefinition{
    Name:        "get_weather",
    Description: "Get current weather for a city",
    Parameters: map[string]interface{}{
        "type": "object",
        "properties": map[string]interface{}{
            "city": map[string]interface{}{
                "type":        "string",
                "description": "City name",
            },
            "unit": map[string]interface{}{
                "type": "string",
                "enum": []string{"celsius", "fahrenheit"},
            },
        },
        "required": []string{"city"},
    },
}
```

## Non-Streaming Tool Calls

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

### Go

```go
response, _ := aiClient.Chat().
    User("What's the weather in Tokyo?").
    Tools([]client.ToolDefinition{getWeather}).
    Execute(ctx)

for _, call := range response.ToolCalls {
    fmt.Printf("Function: %s\n", call.Name)
    fmt.Printf("Arguments: %s\n", call.Arguments)
}
```

## Streaming Tool Calls

Tool calls stream as partial events that the pipeline's Accumulator assembles:

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
for await (const event of client.chat().user("What's the weather?").tools([getWeather]).stream()) {
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

### Go

```go
stream, _ := aiClient.Chat().
    User("What's the weather?").
    Tools([]client.ToolDefinition{getWeather}).
    ExecuteStream(ctx)
defer stream.Close()

for stream.Next() {
    event := stream.Event()
    if event.Type == "tool_call_started" {
        fmt.Printf("Starting: %s\n", event.ToolCall.Name)
    } else if event.Type == "partial_tool_call" {
        fmt.Print(event.ToolCall.Arguments)
    } else if event.Type == "content" {
        fmt.Print(event.Text)
    }
}
```

## How It Works

1. You define tools and pass them in the request
2. The protocol manifest maps `tools` to the provider-specific format
3. The model decides to call a tool (or respond with text)
4. For streaming, the pipeline's **Accumulator** assembles partial tool call chunks
5. You receive unified `ToolCallStarted`, `PartialToolCall`, and `ToolCallEnded` events

## Provider Support

Check the provider's capabilities before using tools:

| Provider  | Tool Calling |
| --------- | ------------ |
| OpenAI    | Supported    |
| Anthropic | Supported    |
| Gemini    | Supported    |
| DeepSeek  | Supported    |
| Groq      | Supported    |
| Mistral   | Supported    |
| Qwen      | Supported    |

The manifest's `capabilities.tools: true` flag indicates support.
