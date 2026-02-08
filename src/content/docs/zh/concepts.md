---
title: 核心概念
group: 指南
order: 10
description: Rust库中的基本抽象概念。
---

# 核心概念

理解这些核心概念将帮助你在应用程序中有效使用ai-lib。

## 消息抽象

`Message`结构体统一了所有提供商的对话角色和内容：

```rust
use ai_lib::{Message, Role, Content};

// 创建包含文本内容的用户消息（简便方法）
let user_msg = Message::user("你好，世界！");

// 或使用自定义内容（图片、音频等）
let user_msg_with_content = Message::user_with_content(Content::new_text("你好，世界！"));

// 创建系统消息
let system_msg = Message::system("你是一个有用的助手。");
```

`Content`枚举支持多种模态：
- **Text**：纯文本内容
- **Image**：图像引用，包含URL、MIME类型和可选名称
- **Audio**：音频内容，包含URL和MIME类型
- **Json**：用于函数调用的结构化JSON数据

## ChatProvider Trait

`ChatProvider` trait 是所有提供商实现的核心抽象。它定义了以下标准接口：
- `chat`: 单次聊天完成
- `stream`: 流式聊天完成
- `batch`: 批处理
- `list_models`: 获取可用模型
- `get_model_info`: 检索模型详情

## 提供商和模型管理

`Provider`枚举选择你的AI后端：

```rust
use ai_lib::{Provider, AiClient};

// 支持的提供商
let groq = AiClient::new(Provider::Groq)?;
let openai = AiClient::new(Provider::OpenAI)?;
let anthropic = AiClient::new(Provider::Anthropic)?;
```

模型元数据和选择策略通过以下方式管理：
- **ModelArray**：具有负载均衡的模型组
- **ModelSelectionStrategy**：基于性能、成本或健康的选择
- **LoadBalancingStrategy**：轮询、加权或基于健康的分布

## 函数调用

ai-lib为所有提供商提供统一的函数调用：

```rust
use ai_lib::{Tool, FunctionCallPolicy, FunctionCall};

// 定义工具
let weather_tool = Tool::new_json(
    "get_weather",
    Some("获取当前天气信息"),
    serde_json::json!({
        "type": "object",
        "properties": {
            "location": {"type": "string"}
        },
        "required": ["location"]
    })
);

// 在请求中使用
let req = ChatCompletionRequest::new(model, messages)
    .with_functions(vec![weather_tool])
    .with_function_call(FunctionCallPolicy::Auto);
```

## 可靠性原语

内置的可靠性功能包括：

- **重试逻辑**：带错误分类的指数退避
- **熔断器**：自动故障检测和恢复
- **速率限制**：令牌桶算法进行请求节流
- **回退策略**：多提供商故障转移
- **健康监控**：端点健康跟踪和避免

## 流式处理

跨所有提供商的一致流式处理：

```rust
use futures::StreamExt;

let mut stream = client.chat_completion_stream(req).await?;
while let Some(chunk) = stream.next().await {
    let c = chunk?;
    if let Some(delta) = c.choices[0].delta.content.clone() {
        print!("{delta}");
    }
}
```

## 配置模式

ai-lib支持渐进式配置复杂性：

1. **环境变量**：自动提供商密钥检测
2. **构建器模式**：使用`AiClientBuilder`进行显式配置
3. **连接选项**：代理、超时等的运行时覆盖
4. **自定义传输**：可插拔的HTTP传输实现
5. **自定义指标**：可观测性集成点

## 错误处理

全面的错误分类：

```rust
match client.chat_completion(req).await {
    Ok(response) => println!("成功: {}", response.first_text()?),
    Err(e) if e.is_retryable() => {
        // 处理可重试错误（网络、速率限制）
        println!("可重试错误: {}", e);
    }
    Err(e) => {
        // 处理永久错误（认证、无效请求）
        println!("永久错误: {}", e);
    }
}
```
