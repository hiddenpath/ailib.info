## Install & Quick Start

Add the dependency, then use the unified API to call any supported provider immediately.

```toml
[dependencies]
ai-lib = "0.4.0"
tokio = { version = "1", features = ["full"] }
futures = "0.3"
```

### Quick Start

```rust
use ai_lib::prelude::*;

#[tokio::main]
async fn main() -> Result<(), AiLibError> {
    let client = AiClient::new(Provider::Groq)?;
    let req = ChatCompletionRequest::new(
        client.default_chat_model(),
        vec![Message {
            role: Role::User,
            content: Content::new_text("Hello, world!"),
            function_call: None,
        }]
    );
    let resp = client.chat_completion(req).await?;
    println!("Answer: {}", resp.choices[0].message.content.as_text());
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

### Multimodal Content

```rust
use ai_lib::prelude::*;

// Image content from file
let image_content = Content::from_image_file("path/to/image.png");

// Audio content from file  
let audio_content = Content::from_audio_file("path/to/audio.mp3");

// Mixed content message
let messages = vec![
    Message {
        role: Role::User,
        content: Content::new_text("Analyze this image"),
        function_call: None,
    },
    Message {
        role: Role::User,
        content: image_content,
        function_call: None,
    },
];
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
