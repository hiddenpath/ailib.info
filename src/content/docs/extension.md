---
title: Extending the SDK
group: Guide
order: 90
---

# Extending the SDK

Add a new provider by implementing translation + transport mapping layers. High-level outline (adjust to actual trait names):

1. Define capability & endpoint metadata (`ModelInfo`, `ModelCapabilities`).
2. Implement a translator that converts `ChatCompletionRequest` -> provider HTTP payload.
3. Implement response parser mapping provider JSON -> unified `ChatCompletionResponse` (and chunks for streaming).
4. Register provider config (`ProviderConfigs`).
5. Add optional pricing / performance metadata for routing heuristics.

Planned docs: full code template & test harness for a mock provider.
