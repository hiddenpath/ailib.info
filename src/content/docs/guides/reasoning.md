---
title: Reasoning Models
description: Using extended thinking and reasoning models with AI-Lib.
---

# Reasoning Models

Some AI models support extended thinking (chain-of-thought reasoning), where the model shows its reasoning process before providing a final answer.

## Supported Models

| Model | Provider | Reasoning |
|-------|----------|-----------|
| o1, o1-mini, o3 | OpenAI | Extended thinking |
| Claude 3.5 Sonnet | Anthropic | Extended thinking |
| DeepSeek R1 | DeepSeek | Chain-of-thought |
| Gemini 2.0 Flash Thinking | Google | Thinking mode |

## Usage

Reasoning models work through the same API. The key difference is that they may emit `ThinkingDelta` events during streaming:

### Rust

```rust
let mut stream = client.chat()
    .user("Solve this step by step: What is 127 * 43?")
    .stream()
    .execute_stream()
    .await?;

while let Some(event) = stream.next().await {
    match event? {
        StreamingEvent::ThinkingDelta { text, .. } => {
            // Model's reasoning process
            print!("[thinking] {text}");
        }
        StreamingEvent::ContentDelta { text, .. } => {
            // Final answer
            print!("{text}");
        }
        _ => {}
    }
}
```

### Python

```python
async for event in client.chat() \
    .user("Solve this step by step: What is 127 * 43?") \
    .stream():
    if event.is_thinking_delta:
        print(f"[thinking] {event.text}", end="")
    elif event.is_content_delta:
        print(event.as_content_delta.text, end="")
```

## How It Works

1. The provider manifest declares `capabilities.reasoning: true`
2. The streaming decoder recognizes thinking-specific events
3. The EventMapper emits `ThinkingDelta` for reasoning content
4. `ContentDelta` events contain the final answer

The protocol manifest handles the provider-specific format differences:

- **OpenAI o1**: Uses internal reasoning tokens
- **Anthropic Claude**: Uses `thinking` content blocks
- **DeepSeek R1**: Uses `<think>` tags in content

## Tips

- Reasoning models generally produce better results for complex tasks
- They use more tokens (reasoning tokens are counted)
- Temperature may be restricted (some reasoning models ignore it)
- Not all providers support reasoning — check `capabilities.reasoning`
