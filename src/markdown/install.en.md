## Install & Quick Start

Add the dependency, then call any supported provider immediately via `quick_chat_text()`.

```toml
[dependencies]
ai-lib = "0.2.12"
tokio = { version = "1", features = ["full"] }
futures = "0.3"
```

```rust
use ai_lib::Provider;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let reply = ai_lib::AiClient::quick_chat_text(Provider::Groq, "Ping?").await?;
    println!("Reply: {}", reply);
    Ok(())
}
```