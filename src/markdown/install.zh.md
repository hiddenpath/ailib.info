## 安装与快速开始

添加依赖后，可使用统一的API立即调用任意受支持的提供商。

```toml
[dependencies]
ai-lib = "0.2.21"
tokio = { version = "1", features = ["full"] }
futures = "0.3"
```

### 快速开始

```rust
use ai_lib::{AiClient, Provider, Message, Role, Content, ChatCompletionRequest};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = AiClient::new(Provider::Groq)?;
    let req = ChatCompletionRequest::new(
        client.default_chat_model(),
        vec![Message {
            role: Role::User,
            content: Content::Text("你好，世界！".to_string()),
            function_call: None,
        }]
    );
    let resp = client.chat_completion(req).await?;
    println!("回答: {}", resp.choices[0].message.content.as_text());
    Ok(())
}
```

### 环境变量配置

```bash
# 设置API密钥
export GROQ_API_KEY=your_groq_api_key
export OPENAI_API_KEY=your_openai_api_key
export ANTHROPIC_API_KEY=your_anthropic_api_key

# 代理配置（可选）
export AI_PROXY_URL=http://proxy.example.com:8080
```

### 流式处理

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
