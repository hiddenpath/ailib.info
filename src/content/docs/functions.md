---
title: Functions & Tools
group: Guide
order: 30
status: stable
---

# Functions & Tools

If/when the crate exposes structured function/tool calling (similar to OpenAI function calls), you typically:

1. Define a schema (name + JSON description) in a model/provider-specific way.
2. Send messages including your tool declarations.
3. Inspect response for a function/tool invocation and then execute locally.
4. Append the tool result as a new `Message` with role=Tool (if supported) and continue.

> NOTE: At version 0.2.12, verify in docs.rs whether a first‑class function calling abstraction is stabilized. The following is a forward‑looking pattern sketch.

## Hypothetical Pattern

```rust
// PSEUDOCODE: adapt to actual API surface once available.
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role};
use ai_lib::types::common::Content;

struct ToolDef {
  name: &'static str,
  json_schema: serde_json::Value,
}

fn weather_schema() -> serde_json::Value {
  serde_json::json!({
    "name": "get_weather",
    "description": "Get current weather for a city",
    "parameters": {
    "type": "object",
    "properties": { "city": { "type": "string" } },
    "required": ["city"]
    }
  })
}

async fn maybe_call_tool(name: &str, args: &serde_json::Value) -> serde_json::Value {
  match name {
    "get_weather" => {
      let city = args["city"].as_str().unwrap_or("unknown");
      serde_json::json!({ "temp_c": 23.4, "city": city })
    }
    _ => serde_json::json!({ "error": "unknown tool" })
  }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
  let client = AiClient::new(Provider::OpenAI)?;

  let tools = vec![ToolDef { name: "get_weather", json_schema: weather_schema() }];

  let mut conversation = vec![Message { role: Role::User, content: Content::Text("What's the weather in Paris?".into()), function_call: None }];

  // Pseudocode loop: send -> detect tool request -> execute -> append -> send again.
  // while need_more_rounds {
  //    let req = ChatCompletionRequest::new("gpt-4o".into(), conversation.clone());
  //    let resp = client.chat(req).await?;
  //    if let Some(call) = resp.first_tool_call() { // hypothetical helper
  //        let result = maybe_call_tool(&call.name, &call.args).await;
  //        conversation.push(Message { role: Role::Tool, content: Content::Text(result.to_string()), function_call: None });
  //        continue;
  //    }
  //    println!("Final: {}", resp.first_text().unwrap_or("<no text>"));
  //    break;
  // }

  Ok(())
}
```

## Execution Flow Recap

1. Model emits a tool/function call intent.
2. You parse the name + arguments (JSON).
3. Execute server-side; produce JSON result.
4. Feed result back to the model as a tool response message.
5. Model produces final user-facing answer.

Parallel tool execution, richer argument validation, and typed wrappers can be layered atop this loop.
