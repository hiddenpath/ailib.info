---
title: Intelligent Routing
group: Reliability
order: 40
status: stable
---

# Intelligent Routing (Stable)

Select models via `ModelArray` with load‑balancing strategy, minimal health checks, and routing metrics.

## Basic usage (routing_mvp)

```rust
use ai_lib::{AiClientBuilder, ChatCompletionRequest, Message, Provider, Role};
use ai_lib::Content;
use ai_lib::provider::models::{ModelArray, ModelEndpoint, LoadBalancingStrategy};

let mut array = ModelArray::new("prod").with_strategy(LoadBalancingStrategy::RoundRobin);
array.add_endpoint(ModelEndpoint {
    name: "groq-70b".to_string(),
    model_name: "llama-3.3-70b-versatile".to_string(),
    url: "https://api.groq.com".to_string(),
    weight: 1.0,
    healthy: true,
    connection_count: 0,
});

let client = AiClientBuilder::new(Provider::Groq)
    .with_routing_array(array)
    .build()?;

// Use sentinel model "__route__" to trigger routing
let req = ChatCompletionRequest::new(
    "__route__".to_string(),
    vec![Message { role: Role::User, content: Content::new_text("Say hi"), function_call: None }]
);
let resp = client.chat_completion(req).await?;
println!("selected model: {}", resp.model);
```

## Health checks & metrics

- Minimal health check: probe `{base_url}` (or OpenAI‑compatible `{base_url}/models`) before selection.
- Routing metrics (when `routing_mvp` enabled):
  - `routing_mvp.request`
  - `routing_mvp.selected`
  - `routing_mvp.health_fail`
  - `routing_mvp.fallback_default`
  - `routing_mvp.no_endpoint`
  - `routing_mvp.missing_array`

## Notes

- This is an MVP: round‑robin/weighted/minimal health checks; adaptive feedback loops can evolve in PRO.
