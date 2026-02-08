---
title: 实用示例
group: 示例
order: 10
status: stable
---

# 实用示例

常见AI应用场景的实用代码模式和示例。

## 实用配方

### 1. 聊天机器人循环与回退链

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};
use std::collections::VecDeque;

pub struct Chatbot {
    clients: Vec<AiClient>,
    conversation_history: VecDeque<Message>,
    max_history: usize,
}

impl Chatbot {
    pub fn new(providers: Vec<Provider>) -> Result<Self, Box<dyn std::error::Error>> {
        let clients = providers
            .into_iter()
            .map(|provider| AiClient::new(provider))
            .collect::<Result<Vec<_>, _>>()?;
        
        Ok(Self {
            clients,
            conversation_history: VecDeque::new(),
            max_history: 10,
        })
    }
    
    pub async fn chat(&mut self, user_input: &str) -> Result<String, Box<dyn std::error::Error>> {
        // 添加用户消息到历史
        self.conversation_history.push_back(Message::user(Content::new_text(user_input.to_string())));
        
        // 保持历史长度
        if self.conversation_history.len() > self.max_history {
            self.conversation_history.pop_front();
        }
        
        // 尝试每个客户端，直到成功
        for client in &self.clients {
            let request = ChatCompletionRequest::new(
                client.default_chat_model(),
                self.conversation_history.iter().cloned().collect()
            );
            
            match client.chat_completion(request).await {
                Ok(response) => {
                    let assistant_message = response.first_text()?;
                    
                    // 添加助手回复到历史
                    self.conversation_history.push_back(Message {
                        role: Role::Assistant,
                        content: Content::new_text(assistant_message.clone()),
                        function_call: None,
                    });
                    
                    return Ok(assistant_message);
                }
                Err(e) => {
                    eprintln!("Provider failed: {}", e);
                    continue;
                }
            }
        }
        
        Err("All providers failed".into())
    }
}
```

### 2. 工具调用执行循环

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content, Tool, FunctionCallPolicy};
use serde_json::Value;

pub struct ToolExecutor {
    client: AiClient,
    tools: Vec<Tool>,
}

impl ToolExecutor {
    pub fn new(provider: Provider) -> Result<Self, Box<dyn std::error::Error>> {
        let client = AiClient::new(provider)?;
        Ok(Self {
            client,
            tools: Vec::new(),
        })
    }
    
    pub fn add_tool(&mut self, tool: Tool) {
        self.tools.push(tool);
    }
    
    pub async fn execute_with_tools(&self, user_input: &str) -> Result<String, Box<dyn std::error::Error>> {
        let mut conversation = vec![Message::user(Content::new_text(user_input.to_string()))];
        
        loop {
            let request = ChatCompletionRequest::new(
                self.client.default_chat_model(),
                conversation.clone()
            )
            .with_functions(self.tools.clone())
            .with_function_call(FunctionCallPolicy::Auto);
            
            let response = self.client.chat_completion(request).await?;
            
            if let Some(choice) = response.choices.first() {
                if let Some(function_call) = &choice.message.function_call {
                    // 执行工具调用
                    let tool_result = self.execute_tool(function_call).await?;
                    
                    // 添加工具调用和结果到对话
                    conversation.push(choice.message.clone());
                    conversation.push(Message {
                        role: Role::Assistant,
                        content: Content::new_json(tool_result),
                        function_call: None,
                    });
                } else {
                    // 没有工具调用，返回最终答案
                    return Ok(choice.message.content.as_text());
                }
            } else {
                return Err("No response from model".into());
            }
        }
    }
    
    async fn execute_tool(&self, function_call: &FunctionCall) -> Result<Value, Box<dyn std::error::Error>> {
        match function_call.name.as_str() {
            "get_weather" => {
                let location = function_call.arguments
                    .get("location")
                    .and_then(|v| v.as_str())
                    .unwrap_or("unknown");
                
                // 模拟天气API调用
                Ok(serde_json::json!({
                    "temperature": 22.5,
                    "condition": "sunny",
                    "location": location
                }))
            }
            "get_news" => {
                let topic = function_call.arguments
                    .get("topic")
                    .and_then(|v| v.as_str())
                    .unwrap_or("general");
                
                Ok(serde_json::json!({
                    "headlines": [
                        format!("Breaking: {} news update 1", topic),
                        format!("Latest: {} news update 2", topic),
                    ]
                }))
            }
            _ => Err(format!("Unknown tool: {}", function_call.name).into()),
        }
    }
}
```

### 3. 多模态图像+文本请求

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};

pub struct MultimodalAnalyzer {
    client: AiClient,
}

impl MultimodalAnalyzer {
    pub fn new(provider: Provider) -> Result<Self, Box<dyn std::error::Error>> {
        let client = AiClient::new(provider)?;
        Ok(Self { client })
    }
    
    pub async fn analyze_image(&self, image_url: &str, prompt: &str) -> Result<String, Box<dyn std::error::Error>> {
        let message = Message::user(Content::new_image(
            Some(image_url.to_string()),
            Some("image/jpeg".to_string()),
            Some("image.jpg".to_string())
        ));
        
        let text_message = Message::user(Content::new_text(prompt.to_string()));
        
        let request = ChatCompletionRequest::new(
            self.client.default_chat_model(),
            vec![message, text_message]
        );
        
        let response = self.client.chat_completion(request).await?;
        Ok(response.first_text()?)
    }
    
    pub async fn compare_images(&self, image1_url: &str, image2_url: &str) -> Result<String, Box<dyn std::error::Error>> {
        let message1 = Message::user(Content::new_image(
            Some(image1_url.to_string()),
            Some("image/jpeg".to_string()),
            Some("image1.jpg".to_string())
        ));
        
        let message2 = Message::user(Content::new_image(
            Some(image2_url.to_string()),
            Some("image/jpeg".to_string()),
            Some("image2.jpg".to_string())
        ));
        
        let text_message = Message::user(Content::new_text("请比较这两张图片的相似性和差异"));
        
        let request = ChatCompletionRequest::new(
            self.client.default_chat_model(),
            vec![message1, message2, text_message]
        );
        
        let response = self.client.chat_completion(request).await?;
        Ok(response.first_text()?)
    }
}
```

### 4. 延迟竞争（对冲）示例

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};
use tokio::time::{timeout, Duration};
use futures::future::select_all;

pub struct HedgingClient {
    primary_client: AiClient,
    fallback_clients: Vec<AiClient>,
    hedge_delay: Duration,
}

impl HedgingClient {
    pub fn new(primary: Provider, fallbacks: Vec<Provider>) -> Result<Self, Box<dyn std::error::Error>> {
        let primary_client = AiClient::new(primary)?;
        let fallback_clients = fallbacks
            .into_iter()
            .map(|provider| AiClient::new(provider))
            .collect::<Result<Vec<_>, _>>()?;
        
        Ok(Self {
            primary_client,
            fallback_clients,
            hedge_delay: Duration::from_millis(100),
        })
    }
    
    pub async fn chat_with_hedging(&self, user_input: &str) -> Result<String, Box<dyn std::error::Error>> {
        let request = ChatCompletionRequest::new(
            self.primary_client.default_chat_model(),
            vec![Message::user(Content::new_text(user_input.to_string()))]
        );
        
        // 立即启动主请求
        let primary_future = self.primary_client.chat_completion(request.clone());
        
        // 延迟启动回退请求
        let hedge_future = async {
            tokio::time::sleep(self.hedge_delay).await;
            
            let mut futures = Vec::new();
            for client in &self.fallback_clients {
                let future = client.chat_completion(request.clone());
                futures.push(future);
            }
            
            select_all(futures).await
        };
        
        // 选择最快完成的请求
        tokio::select! {
            result = primary_future => {
                match result {
                    Ok(response) => Ok(response.first_text()?),
                    Err(e) => {
                        eprintln!("Primary request failed: {}", e);
                        Err(e.into())
                    }
                }
            }
            result = hedge_future => {
                match result {
                    Ok((response, _, _)) => {
                        println!("Hedged request succeeded");
                        Ok(response.first_text()?)
                    }
                    Err(e) => {
                        eprintln!("All hedged requests failed: {}", e);
                        Err(e.into())
                    }
                }
            }
        }
    }
}
```

### 5. 成本感知路由策略

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content, ModelArray, LoadBalancingStrategy};
use std::collections::HashMap;

pub struct CostAwareRouter {
    model_array: ModelArray,
    cost_per_token: HashMap<String, f64>,
}

impl CostAwareRouter {
    pub fn new() -> Self {
        let mut model_array = ModelArray::new("cost-aware")
            .with_strategy(LoadBalancingStrategy::Weighted);
        
        // 添加不同成本的模型
        model_array.add_endpoint(ModelEndpoint {
            name: "gpt-4".into(),
            url: "https://api.openai.com".into(),
            weight: 0.3, // 高成本，低权重
            healthy: true,
        });
        
        model_array.add_endpoint(ModelEndpoint {
            name: "gpt-3.5-turbo".into(),
            url: "https://api.openai.com".into(),
            weight: 0.7, // 低成本，高权重
            healthy: true,
        });
        
        let mut cost_per_token = HashMap::new();
        cost_per_token.insert("gpt-4".to_string(), 0.00003);
        cost_per_token.insert("gpt-3.5-turbo".to_string(), 0.000002);
        
        Self {
            model_array,
            cost_per_token,
        }
    }
    
    pub async fn route_request(&self, request: &ChatCompletionRequest) -> Result<String, Box<dyn std::error::Error>> {
        // 根据请求复杂度选择模型
        let complexity = self.estimate_complexity(request);
        let model = self.select_model_by_complexity(complexity);
        
        let client = AiClient::with_model_array(self.model_array.clone())?;
        let response = client.chat_completion(request.clone()).await?;
        
        // 记录成本
        let cost = self.calculate_cost(&model, &response);
        println!("Request cost: ${:.4}", cost);
        
        Ok(response.first_text()?)
    }
    
    fn estimate_complexity(&self, request: &ChatCompletionRequest) -> f64 {
        let total_tokens = request.messages
            .iter()
            .map(|msg| msg.content.as_text().len())
            .sum::<usize>() as f64;
        
        // 简单的复杂度估算：基于令牌数量
        total_tokens / 1000.0
    }
    
    fn select_model_by_complexity(&self, complexity: f64) -> String {
        if complexity > 0.5 {
            "gpt-4".to_string() // 复杂请求使用GPT-4
        } else {
            "gpt-3.5-turbo".to_string() // 简单请求使用GPT-3.5
        }
    }
    
    fn calculate_cost(&self, model: &str, response: &ChatCompletionResponse) -> f64 {
        let cost_per_token = self.cost_per_token.get(model).unwrap_or(&0.0);
        let total_tokens = response.usage.total_tokens as f64;
        cost_per_token * total_tokens
    }
}
```

### 6. 批量处理优化

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};
use tokio::sync::Semaphore;
use std::sync::Arc;

pub struct BatchProcessor {
    client: AiClient,
    semaphore: Arc<Semaphore>,
    batch_size: usize,
}

impl BatchProcessor {
    pub fn new(provider: Provider, max_concurrency: usize, batch_size: usize) -> Result<Self, Box<dyn std::error::Error>> {
        let client = AiClient::new(provider)?;
        let semaphore = Arc::new(Semaphore::new(max_concurrency));
        
        Ok(Self {
            client,
            semaphore,
            batch_size,
        })
    }
    
    pub async fn process_batch(&self, requests: Vec<ChatCompletionRequest>) -> Result<Vec<String>, Box<dyn std::error::Error>> {
        let mut results = Vec::new();
        let mut chunks = requests.chunks(self.batch_size);
        
        for chunk in chunks {
            let chunk_results = self.process_chunk(chunk.to_vec()).await?;
            results.extend(chunk_results);
        }
        
        Ok(results)
    }
    
    async fn process_chunk(&self, requests: Vec<ChatCompletionRequest>) -> Result<Vec<String>, Box<dyn std::error::Error>> {
        let mut handles = Vec::new();
        
        for request in requests {
            let permit = self.semaphore.clone().acquire_owned().await?;
            let client = self.client.clone();
            
            let handle = tokio::spawn(async move {
                let _permit = permit;
                client.chat_completion(request).await
            });
            
            handles.push(handle);
        }
        
        let mut results = Vec::new();
        for handle in handles {
            let response = handle.await??;
            results.push(response.first_text()?);
        }
        
        Ok(results)
    }
}
```

### 7. 流式处理优化

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};
use futures::stream::{self, StreamExt};
use tokio::io::{AsyncWrite, AsyncWriteExt};

pub struct StreamingProcessor {
    client: AiClient,
}

impl StreamingProcessor {
    pub fn new(provider: Provider) -> Result<Self, Box<dyn std::error::Error>> {
        let client = AiClient::new(provider)?;
        Ok(Self { client })
    }
    
    pub async fn stream_to_writer<W: AsyncWrite + Unpin>(
        &self,
        request: ChatCompletionRequest,
        writer: &mut W,
    ) -> Result<(), Box<dyn std::error::Error>> {
        let mut stream = self.client.chat_completion_stream(request).await?;
        
        while let Some(chunk) = stream.next().await {
            let chunk = chunk?;
            if let Some(delta) = chunk.choices[0].delta.content.clone() {
                writer.write_all(delta.as_bytes()).await?;
                writer.flush().await?;
            }
        }
        
        Ok(())
    }
    
    pub async fn stream_with_callback<F>(
        &self,
        request: ChatCompletionRequest,
        mut callback: F,
    ) -> Result<(), Box<dyn std::error::Error>>
    where
        F: FnMut(&str) -> Result<(), Box<dyn std::error::Error>>,
    {
        let mut stream = self.client.chat_completion_stream(request).await?;
        
        while let Some(chunk) = stream.next().await {
            let chunk = chunk?;
            if let Some(delta) = chunk.choices[0].delta.content.clone() {
                callback(&delta)?;
            }
        }
        
        Ok(())
    }
}
```

## 最佳实践

### 错误处理

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};
use std::time::Duration;

pub async fn robust_chat_completion(
    client: &AiClient,
    request: ChatCompletionRequest,
    max_retries: usize,
) -> Result<String, Box<dyn std::error::Error>> {
    let mut last_error = None;
    
    for attempt in 0..max_retries {
        match timeout(Duration::from_secs(30), client.chat_completion(request.clone())).await {
            Ok(Ok(response)) => return Ok(response.first_text()?),
            Ok(Err(e)) => {
                last_error = Some(e);
                if attempt < max_retries - 1 {
                    tokio::time::sleep(Duration::from_millis(1000 * (attempt + 1) as u64)).await;
                }
            }
            Err(_) => {
                last_error = Some("Request timeout".into());
                if attempt < max_retries - 1 {
                    tokio::time::sleep(Duration::from_millis(1000 * (attempt + 1) as u64)).await;
                }
            }
        }
    }
    
    Err(last_error.unwrap_or("All retries failed".into()))
}
```

### 性能监控

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};
use std::time::Instant;

pub async fn monitored_chat_completion(
    client: &AiClient,
    request: ChatCompletionRequest,
) -> Result<(String, Duration), Box<dyn std::error::Error>> {
    let start = Instant::now();
    
    let response = client.chat_completion(request).await?;
    let duration = start.elapsed();
    
    println!("Request completed in {:?}", duration);
    
    Ok((response.first_text()?, duration))
}
```

## 下一步

- 查看[高级示例](/docs/advanced-examples)了解更多实现模式
- 探索[可靠性功能](/docs/reliability-overview)了解生产级配置
- 学习[可观测性](/docs/observability)了解监控和指标
