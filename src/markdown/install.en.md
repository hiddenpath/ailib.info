## Install & Quick Start

Add the dependency, then use the unified API to call any supported provider immediately.

```toml
[dependencies]
ai-lib = "0.2.20"
tokio = { version = "1", features = ["full"] }
futures = "0.3"
```

### Quick Start

```rust
use ai_lib::{AiClient, Provider, Message, Content, ChatCompletionRequest};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = AiClient::new(Provider::Groq)?;
    let req = ChatCompletionRequest::new(
        client.default_chat_model(),
        vec![Message::user(Content::new_text("Hello, world!"))]
    );
    let resp = client.chat_completion(req).await?;
    println!("Answer: {}", resp.first_text()?);
    Ok(())
}
```

### Environment Variables Configuration

```bash
# Set API keys
export GROQ_API_KEY=your_groq_api_key
export OPENAI_API_KEY=your_openai_api_key
export ANTHROPIC_API_KEY=your_anthropic_api_key

# Proxy configuration (optional)
export AI_PROXY_URL=http://proxy.example.com:8080
```

### Streaming

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
