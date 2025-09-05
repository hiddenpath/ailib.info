---
title: 扩展SDK
group: 指南
order: 90
---

# 扩展SDK

通过实现转换和传输映射层来添加新的提供商。高级概述（根据实际特征名称调整）：

1. 定义能力和端点元数据（`ModelInfo`、`ModelCapabilities`）
2. 实现将`ChatCompletionRequest`转换为提供商HTTP负载的转换器
3. 实现响应解析器，将提供商JSON映射为统一的`ChatCompletionResponse`（以及流式处理的块）
4. 注册提供商配置（`ProviderConfigs`）
5. 添加可选的定价/性能元数据用于路由启发式

计划文档：模拟提供商的完整代码模板和测试工具。

## 扩展架构

### 核心组件

ai-lib的扩展架构基于以下核心组件：

- **Provider Trait**：定义提供商接口
- **Transport Layer**：HTTP传输抽象
- **Model Management**：模型元数据管理
- **Configuration**：提供商配置系统

### 扩展点

#### 1. 自定义提供商

```rust
use ai_lib::provider::{ProviderAdapter, ProviderConfig};
use ai_lib::types::{ChatCompletionRequest, ChatCompletionResponse};

pub struct CustomProvider {
    config: ProviderConfig,
    transport: Box<dyn HttpTransport>,
}

impl ProviderAdapter for CustomProvider {
    async fn chat_completion(
        &self,
        request: ChatCompletionRequest,
    ) -> Result<ChatCompletionResponse, AiLibError> {
        // 实现自定义提供商的聊天完成逻辑
        let http_request = self.translate_request(request)?;
        let http_response = self.transport.post(&self.config.endpoint, &http_request).await?;
        let response = self.parse_response(http_response)?;
        Ok(response)
    }
    
    async fn chat_completion_stream(
        &self,
        request: ChatCompletionRequest,
    ) -> Result<impl Stream<Item = Result<ChatCompletionChunk, AiLibError>>, AiLibError> {
        // 实现流式处理逻辑
        todo!()
    }
}
```

#### 2. 自定义传输

```rust
use ai_lib::transport::{DynHttpTransport, TransportError};

pub struct CustomTransport {
    client: reqwest::Client,
    base_url: String,
}

#[async_trait]
impl DynHttpTransport for CustomTransport {
    async fn post(
        &self,
        url: &str,
        body: &[u8],
    ) -> Result<Vec<u8>, TransportError> {
        let response = self.client
            .post(url)
            .header("Content-Type", "application/json")
            .body(body.to_vec())
            .send()
            .await?;
        
        let bytes = response.bytes().await?;
        Ok(bytes.to_vec())
    }
    
    async fn get(&self, url: &str) -> Result<Vec<u8>, TransportError> {
        let response = self.client.get(url).send().await?;
        let bytes = response.bytes().await?;
        Ok(bytes.to_vec())
    }
}
```

#### 3. 自定义指标

```rust
use ai_lib::metrics::{Metrics, Timer};
use std::time::Instant;

pub struct CustomMetrics {
    // 自定义指标存储
}

impl Metrics for CustomMetrics {
    async fn incr_counter(&self, name: &str, value: u64) {
        // 实现自定义计数器逻辑
        println!("Counter {}: {}", name, value);
    }
    
    async fn start_timer(&self, name: &str) -> Option<Box<dyn Timer + Send>> {
        Some(Box::new(CustomTimer::new(name)))
    }
}

struct CustomTimer {
    start: Instant,
    name: String,
}

impl Timer for CustomTimer {
    fn stop(&mut self) {
        let duration = self.start.elapsed();
        println!("Timer {}: {:?}", self.name, duration);
    }
}
```

## 实现步骤

### 步骤1：定义模型元数据

```rust
use ai_lib::provider::models::{ModelInfo, ModelCapabilities, QualityTier, SpeedTier};

fn create_model_info() -> ModelInfo {
    ModelInfo {
        name: "custom-model-v1".to_string(),
        provider: "custom".to_string(),
        capabilities: ModelCapabilities {
            chat: true,
            streaming: true,
            multimodal: false,
            function_calling: true,
        },
        quality_tier: QualityTier::High,
        speed_tier: SpeedTier::Fast,
        max_tokens: 4096,
        input_cost_per_token: 0.0001,
        output_cost_per_token: 0.0002,
    }
}
```

### 步骤2：实现请求转换

```rust
use ai_lib::types::{ChatCompletionRequest, Message, Role, Content};
use serde_json::json;

impl CustomProvider {
    fn translate_request(&self, request: ChatCompletionRequest) -> Result<Vec<u8>, AiLibError> {
        let messages: Vec<serde_json::Value> = request.messages
            .into_iter()
            .map(|msg| {
                json!({
                    "role": match msg.role {
                        Role::User => "user",
                        Role::Assistant => "assistant",
                        Role::System => "system",
                    },
                    "content": msg.content.as_text(),
                })
            })
            .collect();
        
        let payload = json!({
            "model": request.model,
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7,
        });
        
        Ok(serde_json::to_vec(&payload)?)
    }
}
```

### 步骤3：实现响应解析

```rust
use ai_lib::types::{ChatCompletionResponse, Choice, Usage};

impl CustomProvider {
    fn parse_response(&self, response: Vec<u8>) -> Result<ChatCompletionResponse, AiLibError> {
        let json: serde_json::Value = serde_json::from_slice(&response)?;
        
        let choices = json["choices"]
            .as_array()
            .unwrap_or(&vec![])
            .iter()
            .map(|choice| {
                Choice {
                    index: choice["index"].as_u64().unwrap_or(0) as u32,
                    message: Message {
                        role: Role::Assistant,
                        content: Content::new_text(
                            choice["message"]["content"].as_str().unwrap_or("").to_string()
                        ),
                        function_call: None,
                    },
                    finish_reason: choice["finish_reason"].as_str().map(|s| s.to_string()),
                }
            })
            .collect();
        
        let usage = Usage {
            prompt_tokens: json["usage"]["prompt_tokens"].as_u64().unwrap_or(0) as u32,
            completion_tokens: json["usage"]["completion_tokens"].as_u64().unwrap_or(0) as u32,
            total_tokens: json["usage"]["total_tokens"].as_u64().unwrap_or(0) as u32,
        };
        
        Ok(ChatCompletionResponse {
            id: json["id"].as_str().unwrap_or("").to_string(),
            object: "chat.completion".to_string(),
            created: json["created"].as_u64().unwrap_or(0),
            model: json["model"].as_str().unwrap_or("").to_string(),
            choices,
            usage: Some(usage),
        })
    }
}
```

### 步骤4：注册提供商配置

```rust
use ai_lib::provider::configs::ProviderConfigs;

fn register_custom_provider() -> Result<(), AiLibError> {
    let config = ProviderConfig {
        name: "custom".to_string(),
        base_url: "https://api.custom-provider.com".to_string(),
        api_key_header: "Authorization".to_string(),
        api_key_format: "Bearer {key}".to_string(),
        models: vec![create_model_info()],
    };
    
    let mut configs = ProviderConfigs::new();
    configs.add_provider(config);
    
    // 注册到全局配置
    configs.register()?;
    
    Ok(())
}
```

### 步骤5：实现流式处理

```rust
use futures::stream::{self, Stream};
use ai_lib::api::ChatCompletionChunk;

impl CustomProvider {
    async fn chat_completion_stream(
        &self,
        request: ChatCompletionRequest,
    ) -> Result<impl Stream<Item = Result<ChatCompletionChunk, AiLibError>>, AiLibError> {
        let http_request = self.translate_request(request)?;
        let response = self.transport.post(&self.config.endpoint, &http_request).await?;
        
        // 解析SSE流
        let chunks = self.parse_streaming_response(response)?;
        
        Ok(stream::iter(chunks))
    }
    
    fn parse_streaming_response(&self, response: Vec<u8>) -> Result<Vec<ChatCompletionChunk>, AiLibError> {
        let text = String::from_utf8(response)?;
        let mut chunks = Vec::new();
        
        for line in text.lines() {
            if line.starts_with("data: ") {
                let data = &line[6..];
                if data == "[DONE]" {
                    break;
                }
                
                if let Ok(chunk) = serde_json::from_str::<ChatCompletionChunk>(data) {
                    chunks.push(Ok(chunk));
                }
            }
        }
        
        Ok(chunks)
    }
}
```

## 测试和验证

### 单元测试

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use ai_lib::{AiClient, Provider};

    #[tokio::test]
    async fn test_custom_provider() {
        let provider = CustomProvider::new("test-config".to_string())?;
        let client = AiClient::with_custom_provider(provider)?;
        
        let request = ChatCompletionRequest::new(
            "custom-model-v1".to_string(),
            vec![Message::user(Content::new_text("Hello"))]
        );
        
        let response = client.chat_completion(request).await?;
        assert!(!response.first_text()?.is_empty());
    }
}
```

### 集成测试

```rust
#[tokio::test]
async fn test_custom_provider_integration() {
    // 设置测试环境
    let test_config = TestConfig::new();
    let provider = CustomProvider::new(test_config)?;
    
    // 测试基本功能
    let client = AiClient::with_custom_provider(provider)?;
    
    // 测试聊天完成
    let request = ChatCompletionRequest::new(
        "custom-model-v1".to_string(),
        vec![Message::user(Content::new_text("Test message"))]
    );
    
    let response = client.chat_completion(request).await?;
    assert_eq!(response.model, "custom-model-v1");
    
    // 测试流式处理
    let stream = client.chat_completion_stream(request).await?;
    let mut chunks = Vec::new();
    let mut stream = stream;
    while let Some(chunk) = stream.next().await {
        chunks.push(chunk?);
    }
    assert!(!chunks.is_empty());
}
```

## 最佳实践

### 错误处理

```rust
use ai_lib::error::AiLibError;

impl CustomProvider {
    fn handle_error(&self, error: reqwest::Error) -> AiLibError {
        if error.is_timeout() {
            AiLibError::Timeout(error.to_string())
        } else if error.is_connect() {
            AiLibError::ConnectionFailed(error.to_string())
        } else {
            AiLibError::ProviderError(error.to_string())
        }
    }
}
```

### 配置管理

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CustomProviderConfig {
    pub base_url: String,
    pub api_key: String,
    pub timeout: Option<u64>,
    pub retry_count: Option<u32>,
}

impl Default for CustomProviderConfig {
    fn default() -> Self {
        Self {
            base_url: "https://api.custom-provider.com".to_string(),
            api_key: String::new(),
            timeout: Some(30),
            retry_count: Some(3),
        }
    }
}
```

### 性能优化

```rust
use std::sync::Arc;
use tokio::sync::RwLock;

pub struct CustomProvider {
    config: Arc<RwLock<CustomProviderConfig>>,
    transport: Arc<dyn DynHttpTransport>,
    metrics: Arc<dyn Metrics>,
}

impl CustomProvider {
    pub fn new(config: CustomProviderConfig) -> Result<Self, AiLibError> {
        let transport = Arc::new(CustomTransport::new(&config)?);
        let metrics = Arc::new(NoopMetrics::new());
        
        Ok(Self {
            config: Arc::new(RwLock::new(config)),
            transport,
            metrics,
        })
    }
}
```

## 下一步

- 查看[高级示例](/docs/advanced-examples)了解实际应用
- 探索[架构设计](/docs/architecture)了解系统结构
- 学习[可靠性功能](/docs/reliability-overview)了解生产级配置
