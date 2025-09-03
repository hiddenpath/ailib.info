## 安装与快速开始

添加依赖后，可使用 `quick_chat_text()` 立即调用任意受支持的提供商。

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