---
title: Reasoning Models
group: Core Features
order: 25
status: stable
description: Built-in support for reasoning models with structured output and step-by-step reasoning.
---

# Reasoning Models

ai-lib provides comprehensive support for reasoning models through existing API capabilities, requiring no additional interface abstractions. This guide demonstrates best practices for interacting with reasoning models from providers like Groq.

## Supported Reasoning Models

### Groq Reasoning Models
- **qwen-qwq-32b**: Qwen reasoning model with structured reasoning support
- **deepseek-r1-distill-llama-70b**: DeepSeek R1 reasoning model
- **openai/gpt-oss-20b**: OpenAI OSS reasoning model
- **openai/gpt-oss-120b**: OpenAI OSS large reasoning model

## Reasoning Modes

### 1. Structured Reasoning
Use function calls for step-by-step reasoning, suitable for scenarios requiring structured output.

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role};
use ai_lib::Content;
use ai_lib::types::function_call::{Tool, FunctionCallPolicy};
use serde_json::json;

let client = AiClient::new(Provider::Groq)?;

let reasoning_tool = Tool {
    name: "step_by_step_reasoning".to_string(),
    description: Some("Execute step-by-step reasoning to solve complex problems".to_string()),
    parameters: Some(json!({
        "type": "object",
        "properties": {
            "problem": {"type": "string", "description": "The problem to solve"},
            "steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "step_number": {"type": "integer"},
                        "description": {"type": "string"},
                        "reasoning": {"type": "string"},
                        "conclusion": {"type": "string"}
                    }
                }
            },
            "final_answer": {"type": "string"}
        }
    })),
};

let request = ChatCompletionRequest::new(
    "qwen-qwq-32b".to_string(),
    vec![Message {
        role: Role::User,
        content: Content::Text("Solve this math problem: 2x + 3 = 11".to_string()),
        function_call: None,
    }],
)
.with_functions(vec![reasoning_tool])
.with_function_call(FunctionCallPolicy::Auto("auto".to_string()));

let response = client.chat_completion(request).await?;
```

### 2. Streaming Reasoning
Observe real-time output of the reasoning process, suitable for scenarios requiring step-by-step display.

```rust
let request = ChatCompletionRequest::new(
    "qwen-qwq-32b".to_string(),
    vec![Message {
        role: Role::User,
        content: Content::Text("Explain how photosynthesis works and show your reasoning process".to_string()),
        function_call: None,
    }],
);

let mut stream = client.chat_completion_stream(request).await?;

while let Some(chunk) = stream.next().await {
    match chunk {
        Ok(chunk) => {
            if let Some(choice) = chunk.choices.first() {
                if let Some(content) = &choice.delta.content {
                    print!("{}", content);
                    std::io::stdout().flush().unwrap();
                }
            }
        }
        Err(e) => {
            println!("Streaming error: {}", e);
            break;
        }
    }
}
```

### 3. JSON Format Reasoning
Get structured reasoning results, suitable for programmatic processing scenarios.

```rust
let request = ChatCompletionRequest::new(
    "qwen-qwq-32b".to_string(),
    vec![Message {
        role: Role::System,
        content: Content::Text("You are a reasoning assistant. Always respond with valid JSON format containing your reasoning process and final answer.".to_string()),
        function_call: None,
    }, Message {
        role: Role::User,
        content: Content::Text("What is the capital of France and why is it important? Please provide your reasoning process.".to_string()),
        function_call: None,
    }],
);

let response = client.chat_completion(request).await?;

// Parse JSON reasoning results
for choice in response.choices {
    let content = choice.message.content.as_text();
    if let Ok(reasoning_json) = serde_json::from_str::<serde_json::Value>(&content) {
        println!("Structured reasoning result: {}", serde_json::to_string_pretty(&reasoning_json)?);
    }
}
```

### 4. Reasoning Configuration
Use escape hatch to pass provider-specific reasoning parameters.

```rust
let mut request = ChatCompletionRequest::new(
    "qwen-qwq-32b".to_string(),
    vec![Message {
        role: Role::User,
        content: Content::Text("Solve this complex math problem: x² + 5x + 6 = 0".to_string()),
        function_call: None,
    }],
);

// Add Groq-specific reasoning parameters
request = request
    .with_provider_specific("reasoning_format", serde_json::Value::String("parsed".to_string()))
    .with_provider_specific("reasoning_effort", serde_json::Value::String("high".to_string()))
    .with_provider_specific("parallel_tool_calls", serde_json::Value::Bool(true))
    .with_provider_specific("service_tier", serde_json::Value::String("flex".to_string()));

let response = client.chat_completion(request).await?;
```

## Reasoning Parameters

### Groq Reasoning Parameters

| Parameter | Type | Description | Values |
|-----------|------|-------------|--------|
| `reasoning_format` | string | Reasoning format | `parsed`, `raw`, `hidden` |
| `reasoning_effort` | string | Reasoning effort level | `low`, `medium`, `high`, `none`, `default` |
| `parallel_tool_calls` | boolean | Parallel tool calls | `true`, `false` |
| `service_tier` | string | Service tier | `on_demand`, `flex`, `auto` |

### Reasoning Format Options

- **parsed**: Parsed reasoning process, suitable for human reading
- **raw**: Raw reasoning process, including internal thinking
- **hidden**: Hidden reasoning process, only showing final results

### Reasoning Effort Levels

- **low**: Low effort level, fast reasoning
- **medium**: Medium effort level, balanced speed and depth
- **high**: High effort level, deep reasoning
- **none**: No reasoning
- **default**: Default effort level

## Best Practices

### 1. Choose Appropriate Reasoning Mode

- **Structured reasoning**: When you need programmatic processing of results
- **Streaming reasoning**: When you need real-time display of reasoning process
- **JSON format**: When you need structured data
- **Configuration reasoning**: When you need fine-grained control of reasoning behavior

### 2. Optimize Reasoning Performance

```rust
// Use high effort level for better reasoning quality
let config = ReasoningConfig {
    format: ReasoningFormat::Structured,
    effort: ReasoningEffort::High,
    parallel_tool_calls: Some(true),
    service_tier: Some(ServiceTier::Flex),
};
```

### 3. Error Handling

```rust
match client.chat_completion(request).await {
    Ok(response) => {
        // Process successful response
        for choice in response.choices {
            println!("Reasoning result: {}", choice.message.content.as_text());
        }
    }
    Err(e) => {
        match e {
            ai_lib::AiLibError::UnsupportedFeature(msg) => {
                println!("Model doesn't support reasoning: {}", msg);
            }
            ai_lib::AiLibError::ProviderError(msg) => {
                println!("Reasoning request failed: {}", msg);
            }
            _ => {
                println!("Other error: {}", e);
            }
        }
    }
}
```

### 4. Reasoning Result Validation

```rust
use examples::reasoning_utils::ReasoningUtils;

let result = ReasoningUtils::parse_reasoning_result(&content);
match result {
    Ok(reasoning_result) => {
        let validation = ReasoningUtils::validate_reasoning_result(&reasoning_result);
        match validation {
            ValidationResult::Valid => println!("Reasoning result is valid"),
            ValidationResult::Invalid(msg) => println!("Reasoning result is invalid: {}", msg),
        }
    }
    Err(e) => println!("Failed to parse reasoning result: {}", e),
}
```

## Example Code

Complete example code can be found in:

- `examples/reasoning_best_practices.rs` - Reasoning model best practices examples
- `examples/reasoning_utils.rs` - Reasoning utilities library

Run examples:

```bash
# Set environment variables
export GROQ_API_KEY=your_api_key_here

# Run reasoning examples
cargo run --example reasoning_best_practices

# Run reasoning utilities examples
cargo run --example reasoning_utils
```

## Summary

ai-lib provides perfect support for reasoning models through existing API capabilities without requiring additional interface abstractions. Developers can choose appropriate reasoning modes and interact with reasoning models through function calls, streaming processing, JSON format, and other methods. The reasoning utilities library provides convenient helper functions to simplify the use of reasoning models.

This design maintains ai-lib's simplicity while providing developers with powerful reasoning capabilities.
