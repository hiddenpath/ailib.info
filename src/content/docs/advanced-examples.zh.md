---
title: 高级示例
group: 指南
order: 95
status: partial
description: 批处理、取消、指标、可靠性、提供商切换示例。
---

# 高级示例

结合核心API的实用模式。如果版本不同，请替换方法名称。

## 1. 带超时的取消（流式处理）

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content, CancelHandle};
use futures::StreamExt;
use tokio::time::{timeout, Duration};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = AiClient::new(Provider::OpenAI)?;
    let req = ChatCompletionRequest::new(
        client.default_chat_model(),
        vec![Message::user(Content::new_text("写一首关于Rust生命周期的长诗"))]
    );
    let (mut stream, handle) = client.chat_completion_stream_with_cancel(req).await?;
    let res = timeout(Duration::from_millis(500), async {
        let mut out = String::new();
        while let Some(chunk) = stream.next().await {
            if let Ok(c) = chunk { 
                if let Some(delta) = c.choices[0].delta.content.clone() {
                    out.push_str(&delta);
                }
            }
        }
        out
    }).await;
    if res.is_err() { 
        handle.cancel(); 
        eprintln!("超时并取消"); 
    }
    Ok(())
}
```

## 2. 并行批处理与Join + 简单聚合

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};
use tokio::task;

fn prompt(q: &str) -> ChatCompletionRequest {
    ChatCompletionRequest::new(
        "gpt-4o".into(),
        vec![Message::user(Content::new_text(q.into()))]
    )
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = AiClient::new(Provider::OpenAI)?;
    let questions = ["什么是RAII？", "生命周期是什么？", "Send vs Sync的区别？"];
    let mut handles = Vec::new();
    for q in questions {
        let c = client.clone(); // 假设实现了Clone
        let req = prompt(q);
        handles.push(task::spawn(async move { c.chat_completion(req).await }));
    }
    for h in handles { 
        let result = h.await??;
        println!("结果: {}", result.first_text()?);
    }
    Ok(())
}
```

## 3. 回退策略（伪代码）

```rust
// let chain = FallbackChain::new()
//   .primary("gpt-4o")
//   .on_timeout("claude-3-haiku")
//   .always("mistral-medium");
// let client = AiClient::builder(Provider::OpenAI).fallback(chain).build()?;
```

## 4. 竞争/对冲

```rust
// let race = RacePolicy::new()
//   .contender("gpt-4o", Duration::from_millis(0))
//   .contender("claude-3-haiku", Duration::from_millis(120))
//   .cancel_others(true);
// let client = AiClient::builder(Provider::OpenAI).race(race).build()?;
```

## 5. 提供商切换 + 模型列表

```rust
use ai_lib::{AiClient, Provider};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let groq = AiClient::new(Provider::Groq)?;
    let openai = AiClient::new(Provider::OpenAI)?;
    // let models = openai.list_models().await?; // 迭代并选择
    // println!("OpenAI模型数量: {}", models.len());
    // let text = groq.quick_chat_text("llama3-8b-8192", "来自Groq的问候").await?;
    // println!("Groq: {text}");
    Ok(())
}
```

## 6. 指标集成（框架）

```rust
use ai_lib::{AiClient, Provider};
use ai_lib::metrics::{Metrics, Timer};
use std::time::Instant;

struct MyMetrics;
impl Metrics for MyMetrics {
    async fn incr_counter(&self, name: &str, v: u64) { 
        println!("指标 {} += {}", name, v); 
    }
    async fn start_timer(&self, name: &str) -> Option<Box<dyn Timer + Send>> { 
        Some(Box::new(MyTimer { 
            start: Instant::now(), 
            name: name.to_string() 
        })) 
    }
}

struct MyTimer { 
    start: Instant, 
    name: String 
}

impl Timer for MyTimer { 
    fn stop(&mut self) { 
        let d = self.start.elapsed(); 
        println!("计时器 {} {}ms", self.name, d.as_millis()); 
    } 
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let metrics = std::sync::Arc::new(MyMetrics);
    let client = AiClient::new_with_metrics(Provider::OpenAI, metrics)?; // 假设的构造函数
    // let resp = client.quick_chat_text("gpt-4o", "带指标的调用").await?;
    Ok(())
}
```

## 7. 智能批处理（如果提供）

```rust
// let reqs = vec![ ... ];
// let results = client.chat_completion_batch_smart(reqs).await?;
```

## 8. 超时包装器

```rust
use tokio::time::{timeout, Duration};

async fn chat_with_timeout(client: &AiClient, req: ChatCompletionRequest) -> Result<String, Box<dyn std::error::Error>> {
    let fut = client.chat_completion(req);
    match timeout(Duration::from_secs(3), fut).await {
        Ok(Ok(r)) => Ok(r.first_text()?),
        Ok(Err(e)) => Err(e.into()),
        Err(_) => Err("请求超时".into()),
    }
}
```

## 9. 将流式处理聚合为最终字符串

```rust
async fn stream_to_string(client: &AiClient, req: ChatCompletionRequest) -> Result<String, Box<dyn std::error::Error>> {
    let mut stream = client.chat_completion_stream(req).await?;
    let mut answer = String::new();
    while let Some(chunk) = stream.next().await { 
        if let Ok(c) = chunk { 
            if let Some(delta) = c.choices[0].delta.content.clone() {
                answer.push_str(&delta);
            }
        } 
    }
    Ok(answer)
}
```

## 10. 结构化工具调用循环（前瞻性）

查看[函数与工具](/docs/functions)了解检测函数/工具意图、本地执行然后继续对话的循环。

## 11. 多提供商负载均衡

```rust
use ai_lib::{AiClient, Provider, ModelArray, LoadBalancingStrategy};

async fn load_balanced_chat() -> Result<(), Box<dyn std::error::Error>> {
    let mut array = ModelArray::new("production")
        .with_strategy(LoadBalancingStrategy::HealthBased);
    
    // 添加多个提供商端点
    array.add_endpoint(ModelEndpoint {
        name: "groq-1".into(),
        url: "https://api.groq.com".into(),
        weight: 1.0,
        healthy: true,
    });
    
    array.add_endpoint(ModelEndpoint {
        name: "openai-1".into(),
        url: "https://api.openai.com".into(),
        weight: 0.8,
        healthy: true,
    });
    
    // 使用负载均衡的客户端
    let client = AiClient::with_model_array(array)?;
    let req = ChatCompletionRequest::new(
        "auto", // 自动选择模型
        vec![Message::user(Content::new_text("你好"))]
    );
    
    let resp = client.chat_completion(req).await?;
    println!("响应: {}", resp.first_text()?);
    Ok(())
}
```

## 12. 错误重试策略

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};
use tokio::time::{sleep, Duration};

async fn retry_with_backoff(client: &AiClient, req: ChatCompletionRequest) -> Result<String, Box<dyn std::error::Error>> {
    let mut retries = 0;
    let max_retries = 3;
    
    loop {
        match client.chat_completion(req.clone()).await {
            Ok(resp) => return Ok(resp.first_text()?),
            Err(e) if e.is_retryable() && retries < max_retries => {
                retries += 1;
                let delay = Duration::from_millis(1000 * retries as u64);
                println!("重试 {} 次，等待 {:?}", retries, delay);
                sleep(delay).await;
            }
            Err(e) => return Err(e.into()),
        }
    }
}
```

## 13. 并发控制

```rust
use tokio::sync::Semaphore;
use std::sync::Arc;

async fn controlled_concurrency() -> Result<(), Box<dyn std::error::Error>> {
    let client = AiClient::new(Provider::OpenAI)?;
    let semaphore = Arc::new(Semaphore::new(5)); // 限制并发数为5
    
    let mut handles = Vec::new();
    for i in 0..10 {
        let permit = semaphore.clone().acquire_owned().await?;
        let client = client.clone();
        
        let handle = tokio::spawn(async move {
            let _permit = permit;
            let req = ChatCompletionRequest::new(
                client.default_chat_model(),
                vec![Message::user(Content::new_text(format!("问题 {}", i)))]
            );
            client.chat_completion(req).await
        });
        
        handles.push(handle);
    }
    
    for handle in handles {
        let result = handle.await??;
        println!("结果: {}", result.first_text()?);
    }
    
    Ok(())
}
```

## 14. 推理大模型集成

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role};
use ai_lib::Content;
use ai_lib::types::function_call::{Tool, FunctionCallPolicy};
use serde_json::json;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = AiClient::new(Provider::Groq)?;
    
    // 创建推理工具
    let reasoning_tool = Tool {
        name: "step_by_step_reasoning".to_string(),
        description: Some("执行步骤化推理解决复杂问题".to_string()),
        parameters: Some(json!({
            "type": "object",
            "properties": {
                "problem": {"type": "string", "description": "要解决的问题"},
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
            content: Content::Text("解决这个数学问题：一个班级有30个学生，60%是女生，40%是男生。如果25%的女生戴眼镜，20%的男生戴眼镜，总共有多少学生戴眼镜？".to_string()),
            function_call: None,
        }],
    )
    .with_functions(vec![reasoning_tool])
    .with_function_call(FunctionCallPolicy::Auto("auto".to_string()));

    let response = client.chat_completion(request).await?;
    
    // 处理推理结果
    for choice in response.choices {
        if let Some(function_call) = choice.message.function_call {
            if function_call.name == "step_by_step_reasoning" {
                if let Some(args) = function_call.arguments {
                    println!("结构化推理结果:");
                    println!("{}", serde_json::to_string_pretty(&args)?);
                }
            }
        }
    }
    
    Ok(())
}
```

## 15. 流式推理配置

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role};
use ai_lib::Content;
use futures_util::StreamExt;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = AiClient::new(Provider::Groq)?;
    
    let mut request = ChatCompletionRequest::new(
        "qwen-qwq-32b".to_string(),
        vec![Message {
            role: Role::User,
            content: Content::Text("解释量子计算原理，并提供步骤化推理".to_string()),
            function_call: None,
        }],
    );
    
    // 添加推理配置
    request = request
        .with_provider_specific("reasoning_format", serde_json::Value::String("parsed".to_string()))
        .with_provider_specific("reasoning_effort", serde_json::Value::String("high".to_string()));

    let mut stream = client.chat_completion_stream(request).await?;
    
    println!("推理过程（流式输出）:");
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
                println!("\n流式错误: {}", e);
                break;
            }
        }
    }
    
    Ok(())
}
```

---

如果方法名称更改或新原语（熔断器、自适应路由）从部分→稳定，请更新此页面。
