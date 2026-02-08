---
title: 函数与工具
group: 指南
order: 30
status: stable
---

# 函数与工具

ai-lib为所有支持的提供商提供统一的函数调用。这允许你的AI模型调用外部函数和工具，实现更具交互性和功能性的应用程序。

## 基本函数调用

使用`Tool`结构体定义工具并将其附加到聊天请求：

```rust
use ai_lib::prelude::*;

#[tokio::main]
async fn main() -> Result<(), AiLibError> {
    let client = AiClient::new(Provider::OpenAI)?;

    // 定义天气工具
    let weather_tool = Tool::new_json(
        "get_weather",
        Some("获取城市的当前天气信息"),
        serde_json::json!({
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "城市名称"
                }
            },
            "required": ["location"]
        })
    );

    // 创建带工具的聊天请求
    let req = ChatCompletionRequest::new(
        client.default_chat_model(),
        vec![Message {
            role: Role::User,
            content: Content::new_text("巴黎的天气怎么样？".to_string()),
            function_call: None,
        }]
    )
    .with_functions(vec![weather_tool])
    .with_function_call(FunctionCallPolicy::Auto);

    let resp = client.chat_completion(req).await?;
    println!("响应: {}", resp.choices[0].message.content.as_text());
    Ok(())
}
```

## 函数调用策略

控制何时以及如何调用函数：

```rust
use ai_lib::{FunctionCallPolicy, Tool};

// Auto：让模型决定何时调用函数
let auto_policy = FunctionCallPolicy::Auto;

// None：从不调用函数
let none_policy = FunctionCallPolicy::None;

// Required：总是调用特定函数
let required_policy = FunctionCallPolicy::Required("get_weather".to_string());

let req = ChatCompletionRequest::new(model, messages)
    .with_functions(vec![weather_tool])
    .with_function_call(auto_policy);
```

## 处理函数调用

当模型决定调用函数时，你需要处理执行：

```rust
use ai_lib::{Message, Role, Content, FunctionCall};

// 检查响应是否包含函数调用
if let Some(choice) = resp.choices.first() {
    if let Some(function_call) = &choice.message.function_call {
        match function_call.name.as_str() {
            "get_weather" => {
                // 提取参数
                let location = function_call.arguments
                    .get("location")
                    .and_then(|v| v.as_str())
                    .unwrap_or("unknown");

                // 执行你的函数
                let weather_data = get_weather_impl(location).await;

                // 创建工具响应消息
                let tool_message = Message {
                    role: Role::Assistant, // 注意：ai-lib使用Assistant角色进行工具响应
                    content: Content::Json(serde_json::json!({
                        "temperature": weather_data.temp,
                        "condition": weather_data.condition,
                        "location": location
                    })),
                    function_call: None,
                };

                // 使用工具结果继续对话
                let follow_up_req = ChatCompletionRequest::new(
                    model,
                    vec![
                        Message {
                            role: Role::User,
                            content: Content::new_text("巴黎的天气怎么样？".to_string()),
                            function_call: None,
                        },
                        choice.message.clone(),
                        tool_message,
                    ]
                );

                let final_resp = client.chat_completion(follow_up_req).await?;
                println!("最终答案: {}", final_resp.choices[0].message.content.as_text());
            }
            _ => println!("未知函数: {}", function_call.name),
        }
    } else {
        println!("无函数调用: {}", choice.message.content.as_text());
    }
}
```

## 多个工具

在单个请求中定义和使用多个工具：

```rust
let weather_tool = Tool::new_json(
    "get_weather",
    Some("获取天气信息"),
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
    Some("获取最新新闻标题"),
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

## 流式函数调用

函数调用与流式响应配合使用：

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
    
    // 检查块中的函数调用
    if let Some(function_call) = &c.choices[0].delta.function_call {
        println!("\n检测到函数调用: {}", function_call.name);
    }
}
```

## 工具执行助手

这是一个带有工具执行助手的完整示例：

```rust
async fn execute_tool_call(function_call: &FunctionCall) -> serde_json::Value {
    match function_call.name.as_str() {
        "get_weather" => {
            let location = function_call.arguments
                .get("location")
                .and_then(|v| v.as_str())
                .unwrap_or("unknown");
            
            // 模拟天气API调用
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
                    format!("突发: {} 新闻更新1", topic),
                    format!("最新: {} 新闻更新2", topic),
                ]
            })
        }
        _ => serde_json::json!({"error": "未知函数"})
    }
}

// 在你的对话循环中使用
let mut conversation = vec![Message {
    role: Role::User,
    content: Content::new_text("东京的天气和科技新闻怎么样？".to_string()),
    function_call: None,
}];

loop {
    let req = ChatCompletionRequest::new(model, conversation.clone())
        .with_functions(vec![weather_tool, news_tool])
        .with_function_call(FunctionCallPolicy::Auto);

    let resp = client.chat_completion(req).await?;
    
    if let Some(choice) = resp.choices.first() {
        if let Some(function_call) = &choice.message.function_call {
            // 执行函数
            let result = execute_tool_call(function_call).await;
            
            // 将函数调用和结果添加到对话中
            conversation.push(choice.message.clone());
            conversation.push(Message {
                role: Role::Assistant,
                content: Content::Json(result),
                function_call: None,
            });
        } else {
            // 无函数调用，完成
            println!("最终响应: {}", choice.message.content.as_text());
            break;
        }
    }
}
```

## 提供商兼容性

函数调用在所有主要提供商中都受支持：

- **OpenAI**：GPT-4和GPT-3.5的完整支持
- **Anthropic**：Claude 3工具使用
- **Google Gemini**：函数调用支持
- **Groq**：有限的函数调用支持
- **Mistral**：兼容模型的函数调用

查看[提供商](/docs/providers)页面了解具体能力。

## 最佳实践

1. **清晰的描述**：编写详细的函数描述，帮助模型理解何时使用它们
2. **验证参数**：执行前始终验证函数参数
3. **错误处理**：优雅地处理函数执行错误
4. **速率限制**：调用外部服务时注意API速率限制
5. **安全性**：永远不要执行不受信任的代码或进行不安全的系统调用

## 下一步

- 学习[流式处理](/docs/chat)了解实时函数调用
- 探索[高级示例](/docs/advanced-examples)了解复杂的工具工作流
- 查看[可靠性功能](/docs/reliability-overview)进行生产部署
