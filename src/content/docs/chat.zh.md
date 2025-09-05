---
title: 聊天与流式处理
group: 指南
order: 20
status: stable
---

# 聊天与流式处理

本节展示核心API：`chat_completion`、流式变体、取消、批处理、快速助手和模型列表。请始终对照docs.rs上的crate版本进行验证。

## 基本聊天完成

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role, Content};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = AiClient::new(Provider::OpenAI)?;
    let req = ChatCompletionRequest::new(
        client.default_chat_model(),
        vec![Message::user(Content::new_text("简洁地总结Rust所有权。"))]
    );
    let resp = client.chat_completion(req).await?;
    println!("回答: {}", resp.first_text()?);
    Ok(())
}
```

## 流式令牌

方法假设：`chat_completion_stream(request)`返回`Result<ChatCompletionChunk, AiLibError>`的异步流。

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};
use futures::StreamExt;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = AiClient::new(Provider::Groq)?;
    let req = ChatCompletionRequest::new(
        client.default_chat_model(),
        vec![Message::user(Content::new_text("流式输出一首关于并发的俳句。"))]
    );
    let mut stream = client.chat_completion_stream(req).await?;
    while let Some(chunk) = stream.next().await {
        match chunk {
            Ok(c) => {
                if let Some(delta) = c.choices[0].delta.content.clone() {
                    print!("{delta}");
                }
            }
            Err(e) => { 
                eprintln!("流式错误: {e}"); 
                break; 
            }
        }
    }
    Ok(())
}
```

## 流式处理 + 取消

假设助手：`chat_completion_stream_with_cancel(req)` → `(impl Stream, CancelHandle)`。

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content, CancelHandle};
use futures::StreamExt;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = AiClient::new(Provider::OpenAI)?;
    let req = ChatCompletionRequest::new(
        client.default_chat_model(),
        vec![Message::user(Content::new_text("慢慢解释借用检查器。"))]
    );
    let (mut stream, handle) = client.chat_completion_stream_with_cancel(req).await?;
    tokio::select! {
        _ = async {
            while let Some(chunk) = stream.next().await {
                if let Ok(c) = chunk { 
                    if let Some(delta) = c.choices[0].delta.content.clone() {
                        print!("{delta}");
                    }
                }
            }
        } => {},
        _ = sleep(Duration::from_millis(400)) => {
            handle.cancel();
            eprintln!("400毫秒后取消");
        }
    }
    Ok(())
}
```

## 批处理请求

两种模式（假设名称）：

1. `chat_completion_batch(Vec<ChatCompletionRequest>)` – 并发执行，返回结果向量。
2. `chat_completion_batch_smart` – 可能应用内部启发式/路由。

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};

fn prompt(p: &str) -> ChatCompletionRequest {
    ChatCompletionRequest::new(
        "gpt-4o".into(),
        vec![Message::user(Content::new_text(p.into()))]
    )
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = AiClient::new(Provider::OpenAI)?;
    let batch = vec![
        prompt("定义RAII"), 
        prompt("用一句话说明生命周期"), 
        prompt("解释Send vs Sync")
    ];
    let results = client.chat_completion_batch(batch).await?;
    for (i, r) in results.iter().enumerate() {
        if let Some(c) = r.choices.first() { 
            println!("{}: {}", i, c.message.content.as_text()); 
        }
    }
    Ok(())
}
```

如果存在更智能的变体：

```rust
// let results = client.chat_completion_batch_smart(batch).await?;
```

## 快速助手

一些crate暴露了符合人体工程学的快捷方式，如`quick_chat_text(model, prompt)`返回`String`。

```rust
// let text = client.quick_chat_text("gpt-4o", "什么是所有权？").await?;
// println!("{text}");
```

## 列出模型

```rust
// let models = client.list_models().await?;
// for m in models { println!("{}", m.name); }
```

## 多模态内容

ai-lib支持文本、图像和音频内容：

```rust
use ai_lib::{Message, Content};

// 文本消息
let text_msg = Message::user(Content::new_text("描述这张图片"));

// 图像消息
let image_msg = Message::user(Content::new_image(
    Some("https://example.com/image.jpg".to_string()),
    Some("image/jpeg".to_string()),
    Some("example.jpg".to_string())
));

// 音频消息
let audio_msg = Message::user(Content::new_audio(
    Some("https://example.com/audio.mp3".to_string()),
    Some("audio/mpeg".to_string())
));
```

## 错误处理

处理不同类型的错误：

```rust
match client.chat_completion(req).await {
    Ok(response) => {
        println!("成功: {}", response.first_text()?);
    }
    Err(e) if e.is_retryable() => {
        // 处理可重试错误（网络、速率限制）
        println!("可重试错误: {}", e);
        // 实现重试逻辑
    }
    Err(e) => {
        // 处理永久错误（认证、无效请求）
        println!("永久错误: {}", e);
    }
}
```

## 性能优化

### 连接池配置

```rust
use ai_lib::{AiClient, Provider, ConnectionOptions};

let client = AiClient::with_options(
    Provider::Groq,
    ConnectionOptions {
        // 配置连接池大小
        pool_size: Some(16),
        // 设置空闲超时
        idle_timeout: Some(Duration::from_secs(30)),
        ..Default::default()
    }
)?;
```

### 并发控制

```rust
use tokio::sync::Semaphore;

let semaphore = Arc::new(Semaphore::new(10)); // 限制并发数为10

for request in requests {
    let permit = semaphore.clone().acquire_owned().await?;
    let client = client.clone();
    
    tokio::spawn(async move {
        let _permit = permit;
        let result = client.chat_completion(request).await;
        // 处理结果
    });
}
```

## 注意事项

提示：

- 检查docs.rs是否有任何重命名（例如`chat` vs `chat_completion`）。
- 如果需要最终答案，将流式增量收集到`String`中。
- 批处理+流式处理一起使用？启动多个`chat_completion_stream`任务并聚合。
- 更多模式：[高级示例](/docs/advanced-examples)
