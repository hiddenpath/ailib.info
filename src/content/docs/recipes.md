---
title: Recipes
group: Recipes
order: 10
status: stable
---

# Recipes

Practical code patterns and examples for common AI application scenarios.

## Basic Patterns

### Simple Chat Loop
```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};

async fn simple_chat_loop(client: &AiClient) -> Result<(), Box<dyn std::error::Error>> {
    let mut messages = vec![Message {
        role: Role::System,
        content: Content::Text("You are a helpful assistant.".to_string()),
    }];
    
    loop {
        let user_input = read_user_input().await?;
        if user_input == "quit" { break; }
        
        messages.push(Message {
            role: Role::User,
            content: Content::Text(user_input),
        });
        
        let request = ChatCompletionRequest {
            model: "gpt-4o".to_string(),
            messages: messages.clone(),
            ..Default::default()
        };
        
        let response = client.chat_completion(request).await?;
        let assistant_message = response.first_text()?;
        
        println!("Assistant: {}", assistant_message);
        messages.push(Message {
            role: Role::Assistant,
            content: Content::Text(assistant_message),
        });
    }
    
    Ok(())
}
```

### Streaming Response
```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};
use futures::StreamExt;

async fn streaming_chat(client: &AiClient) -> Result<(), Box<dyn std::error::Error>> {
    let request = ChatCompletionRequest {
        model: "gpt-4o".to_string(),
        messages: vec![Message {
            role: Role::User,
            content: Content::Text("Tell me a story".to_string()),
        }],
        stream: Some(true),
        ..Default::default()
    };
    
    let mut stream = client.chat_completion_stream(request).await?;
    
    while let Some(chunk) = stream.next().await {
        let chunk = chunk?;
        if let Some(content) = chunk.first_text() {
            print!("{}", content);
            std::io::stdout().flush()?;
        }
    }
    
    Ok(())
}
```

## Advanced Patterns

### Fallback Chain
```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};

async fn resilient_chat(client: &AiClient, request: ChatCompletionRequest) -> Result<String, Box<dyn std::error::Error>> {
    let providers = [Provider::OpenAI, Provider::Anthropic, Provider::Mistral];
    
    for provider in &providers {
        match client.with_provider(*provider).chat_completion(request.clone()).await {
            Ok(response) => return Ok(response.first_text()?),
            Err(error) => {
                eprintln!("Provider {:?} failed: {}", provider, error);
                continue;
            }
        }
    }
    
    Err("All providers failed".into())
}
```

### Tool Calling Loop
```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content, Tool, FunctionCallPolicy};

async fn tool_calling_loop(client: &AiClient) -> Result<(), Box<dyn std::error::Error>> {
    let mut messages = vec![Message {
        role: Role::System,
        content: Content::Text("You are a helpful assistant with access to tools.".to_string()),
    }];
    
    let tools = vec![
        Tool::Function {
            name: "get_weather".to_string(),
            description: Some("Get current weather for a location".to_string()),
            parameters: serde_json::json!({
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"}
                },
                "required": ["location"]
            }),
        }
    ];
    
    loop {
        let user_input = read_user_input().await?;
        if user_input == "quit" { break; }
        
        messages.push(Message {
            role: Role::User,
            content: Content::Text(user_input),
        });
        
        let request = ChatCompletionRequest {
            model: "gpt-4o".to_string(),
            messages: messages.clone(),
            tools: Some(tools.clone()),
            function_call_policy: Some(FunctionCallPolicy::Auto),
            ..Default::default()
        };
        
        let response = client.chat_completion(request).await?;
        
        // Handle function calls
        if let Some(tool_calls) = response.tool_calls {
            for tool_call in tool_calls {
                let result = execute_tool(&tool_call).await?;
                messages.push(Message {
                    role: Role::Tool,
                    content: Content::Text(result),
                });
            }
        } else {
            let assistant_message = response.first_text()?;
            println!("Assistant: {}", assistant_message);
            messages.push(Message {
                role: Role::Assistant,
                content: Content::Text(assistant_message),
            });
        }
    }
    
    Ok(())
}
```

### Multimodal Request
```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};

async fn multimodal_chat(client: &AiClient, image_path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let image_data = std::fs::read(image_path)?;
    let image_base64 = base64::encode(&image_data);
    
    let request = ChatCompletionRequest {
        model: "gpt-4o".to_string(),
        messages: vec![
            Message {
                role: Role::User,
                content: Content::Text("What do you see in this image?".to_string()),
            },
            Message {
                role: Role::User,
                content: Content::Image {
                    url: format!("data:image/jpeg;base64,{}", image_base64),
                    detail: Some("high".to_string()),
                },
            },
        ],
        ..Default::default()
    };
    
    let response = client.chat_completion(request).await?;
    println!("Assistant: {}", response.first_text()?);
    
    Ok(())
}
```

### Race/Hedging Pattern
```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};
use futures::future::select_all;

async fn race_chat(client: &AiClient, request: ChatCompletionRequest) -> Result<String, Box<dyn std::error::Error>> {
    let providers = [Provider::OpenAI, Provider::Anthropic, Provider::Mistral];
    
    let mut futures = Vec::new();
    for provider in &providers {
        let future = client.with_provider(*provider).chat_completion(request.clone());
        futures.push(future);
    }
    
    let (result, _index, _remaining) = select_all(futures).await;
    result.map(|r| r.first_text()).map_err(|e| e.into())
}
```

## Best Practices

1. **Error Handling**: Always handle errors gracefully with fallbacks
2. **Resource Management**: Use appropriate timeouts and limits
3. **Cost Optimization**: Choose models based on task complexity
4. **Performance**: Use streaming for long responses
5. **Security**: Validate inputs and sanitize outputs

## Next Steps

- Check [Advanced Examples](/docs/advanced-examples) for more complex patterns
- Learn about [Reliability Features](/docs/reliability-overview) for production use
- Explore [Function Calling](/docs/functions) for tool integration
