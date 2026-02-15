---
title: 函数调用
description: 使用 AI-Lib 跨提供商使用函数调用（工具使用）的指南。
---

# 函数调用

函数调用（工具使用）允许 AI 模型调用外部函数。AI-Lib 为支持工具调用的所有提供商提供统一的工具调用接口。

## 定义工具

### Rust

```rust
use ai_lib::ToolDefinition;
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

## 非流式工具调用

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

## 流式工具调用

工具调用以部分事件流式传输，由管道的 Accumulator 组装：

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

## 工作原理

1. 定义工具并传入请求
2. 协议清单将 `tools` 映射到提供商特定格式
3. 模型决定调用工具（或以文本响应）
4. 对于流式，管道的 **Accumulator** 组装部分工具调用块
5. 收到统一的 `ToolCallStarted`、`PartialToolCall` 和 `ToolCallEnded` 事件

## 提供商支持

使用工具前请检查提供商的 capabilities：

| Provider | Tool Calling |
|----------|-------------|
| OpenAI | Supported |
| Anthropic | Supported |
| Gemini | Supported |
| DeepSeek | Supported |
| Groq | Supported |
| Mistral | Supported |
| Qwen | Supported |

清单中的 `capabilities.tools: true` 表示支持。
