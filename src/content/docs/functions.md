---
title: Functions & Tools
group: Guide
order: 30
status: stable
---

# Functions & Tools

ai-lib provides unified function calling across all supported providers. This allows your AI models to call external functions and tools, enabling more interactive and capable applications.

## Basic Function Calling

Define tools using the `Tool` struct and attach them to your chat requests:

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role, Tool, FunctionCallPolicy};
use ai_lib::Content;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = AiClient::new(Provider::OpenAI)?;

    // Define a weather tool
    let weather_tool = Tool::new_json(
        "get_weather",
        Some("Get current weather information for a city"),
        serde_json::json!({
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city name"
                }
            },
            "required": ["location"]
        })
    );

    // Create a chat request with tools
    let req = ChatCompletionRequest::new(
        client.default_chat_model(),
        vec![Message {
            role: Role::User,
            content: Content::Text("What's the weather like in Paris?".to_string()),
            function_call: None,
        }]
    )
    .with_functions(vec![weather_tool])
    .with_function_call(FunctionCallPolicy::Auto);

    let resp = client.chat_completion(req).await?;
    println!("Response: {}", resp.choices[0].message.content.as_text());
    Ok(())
}
```

## Function Call Policies

Control when and how functions are called:

```rust
use ai_lib::{FunctionCallPolicy, Tool};

// Auto: Let the model decide when to call functions
let auto_policy = FunctionCallPolicy::Auto;

// None: Never call functions
let none_policy = FunctionCallPolicy::None;

// Required: Always call a specific function
let required_policy = FunctionCallPolicy::Required("get_weather".to_string());

let req = ChatCompletionRequest::new(model, messages)
    .with_functions(vec![weather_tool])
    .with_function_call(auto_policy);
```

## Handling Function Calls

When a model decides to call a function, you need to handle the execution:

```rust
use ai_lib::{Message, Role, Content, FunctionCall};

// Check if the response contains a function call
if let Some(choice) = resp.choices.first() {
    if let Some(function_call) = &choice.message.function_call {
        match function_call.name.as_str() {
            "get_weather" => {
                // Extract arguments
                let location = function_call.arguments
                    .get("location")
                    .and_then(|v| v.as_str())
                    .unwrap_or("unknown");

                // Execute your function
                let weather_data = get_weather_impl(location).await;

                // Create a tool response message
                let tool_message = Message {
                    role: Role::Assistant, // Note: ai-lib uses Assistant role for tool responses
                    content: Content::Json(serde_json::json!({
                        "temperature": weather_data.temp,
                        "condition": weather_data.condition,
                        "location": location
                    })),
                    function_call: None,
                };

                // Continue the conversation with the tool result
                let follow_up_req = ChatCompletionRequest::new(
                    model,
                    vec![
                        Message {
                            role: Role::User,
                            content: Content::Text("What's the weather in Paris?".to_string()),
                            function_call: None,
                        },
                        choice.message.clone(),
                        tool_message,
                    ]
                );

                let final_resp = client.chat_completion(follow_up_req).await?;
                println!("Final answer: {}", final_resp.choices[0].message.content.as_text());
            }
            _ => println!("Unknown function: {}", function_call.name),
        }
    } else {
        println!("No function call: {}", choice.message.content.as_text());
    }
}
```

## Multiple Tools

Define and use multiple tools in a single request:

```rust
let weather_tool = Tool::new_json(
    "get_weather",
    Some("Get weather information"),
    serde_json::json!({
        "type": "object",
        "properties": {
            "location": {"type": "string"}
        },
        "required": ["location"]
    })
);

let news_tool = Tool::new_json(
    "get_news",
    Some("Get latest news headlines"),
    serde_json::json!({
        "type": "object",
        "properties": {
            "topic": {"type": "string"},
            "count": {"type": "integer", "minimum": 1, "maximum": 10}
        },
        "required": ["topic"]
    })
);

let req = ChatCompletionRequest::new(model, messages)
    .with_functions(vec![weather_tool, news_tool])
    .with_function_call(FunctionCallPolicy::Auto);
```

## Streaming with Function Calls

Function calls work with streaming responses:

```rust
use futures::StreamExt;

let mut stream = client.chat_completion_stream(req).await?;
let mut full_response = String::new();

while let Some(chunk) = stream.next().await {
    let c = chunk?;
    if let Some(delta) = c.choices[0].delta.content.clone() {
        full_response.push_str(&delta);
        print!("{delta}");
    }
    
    // Check for function calls in the chunk
    if let Some(function_call) = &c.choices[0].delta.function_call {
        println!("\nFunction call detected: {}", function_call.name);
    }
}
```

## Tool Execution Helper

Here's a complete example with a tool execution helper:

```rust
async fn execute_tool_call(function_call: &FunctionCall) -> serde_json::Value {
    match function_call.name.as_str() {
        "get_weather" => {
            let location = function_call.arguments
                .get("location")
                .and_then(|v| v.as_str())
                .unwrap_or("unknown");
            
            // Simulate weather API call
            serde_json::json!({
                "temperature": 22.5,
                "condition": "sunny",
                "location": location
            })
        }
        "get_news" => {
            let topic = function_call.arguments
                .get("topic")
                .and_then(|v| v.as_str())
                .unwrap_or("general");
            
            serde_json::json!({
                "headlines": [
                    format!("Breaking: {} news update 1", topic),
                    format!("Latest: {} news update 2", topic),
                ]
            })
        }
        _ => serde_json::json!({"error": "Unknown function"})
    }
}

// Use in your conversation loop
let mut conversation = vec![Message {
    role: Role::User,
    content: Content::Text("What's the weather in Tokyo and any tech news?".to_string()),
    function_call: None,
}];

loop {
    let req = ChatCompletionRequest::new(model, conversation.clone())
        .with_functions(vec![weather_tool, news_tool])
        .with_function_call(FunctionCallPolicy::Auto);

    let resp = client.chat_completion(req).await?;
    
    if let Some(choice) = resp.choices.first() {
        if let Some(function_call) = &choice.message.function_call {
            // Execute the function
            let result = execute_tool_call(function_call).await;
            
            // Add the function call and result to conversation
            conversation.push(choice.message.clone());
            conversation.push(Message {
                role: Role::Assistant,
                content: Content::Json(result),
                function_call: None,
            });
        } else {
            // No function call, we're done
            println!("Final response: {}", choice.message.content.as_text());
            break;
        }
    }
}
```

## Provider Compatibility

Function calling is supported across all major providers:

- **OpenAI**: Full support with GPT-4 and GPT-3.5
- **Anthropic**: Claude 3 with tool use
- **Google Gemini**: Function calling support
- **Groq**: Limited function calling support
- **Mistral**: Function calling with compatible models

Check the [Providers](/docs/providers) page for specific capabilities.

## Best Practices

1. **Clear Descriptions**: Write detailed function descriptions to help the model understand when to use them
2. **Validate Arguments**: Always validate function arguments before execution
3. **Error Handling**: Handle function execution errors gracefully
4. **Rate Limiting**: Be mindful of API rate limits when calling external services
5. **Security**: Never execute untrusted code or make unsafe system calls

## Next Steps

- Learn about [Streaming](/docs/chat) for real-time function calling
- Explore [Advanced Examples](/docs/advanced-examples) for complex tool workflows
- Check [Reliability Features](/docs/reliability-overview) for production deployments
