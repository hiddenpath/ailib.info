---
title: Function Calling
description: AI-Lib でプロバイダーをまたいで function calling（ツール使用）を使用するガイド。
---

# Function Calling

Function calling（ツール使用）により、AI モデルが外部関数を呼び出せるようになります。AI-Lib は、それをサポートするすべてのプロバイダーで function calling の統一インターフェースを提供します。

## ツールの定義

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

## 非ストリーミングツール呼び出し

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
    // 関数を実行し、結果を返送する
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

## ストリーミングツール呼び出し

ツール呼び出しは部分イベントとしてストリームされ、パイプラインの Accumulator が組み立てます：

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
            print!("{arguments}"); // 部分的な JSON 引数
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

## 仕組み

1. ツールを定義し、リクエストに渡します
2. プロトコルマニフェストが `tools` をプロバイダー固有の形式にマッピングします
3. モデルがツールを呼び出す（またはテキストで応答する）ことを決定します
4. ストリーミングの場合、パイプラインの **Accumulator** が部分的なツール呼び出しチャンクを組み立てます
5. 統一された `ToolCallStarted`、`PartialToolCall`、`ToolCallEnded` イベントを受信します

## プロバイダーサポート

ツールを使用する前にプロバイダーの機能を確認してください：

| プロバイダー | ツール呼び出し |
|--------------|----------------|
| OpenAI | サポート |
| Anthropic | サポート |
| Gemini | サポート |
| DeepSeek | サポート |
| Groq | サポート |
| Mistral | サポート |
| Qwen | サポート |

マニフェストの `capabilities.tools: true` フラグがサポートを示します。
