---
title: Supported Providers
group: Overview
order: 30
description: Providers and models (Rust crate perspective).
---

# Supported Providers

`Provider` enum abstracts multiple backends (OpenAI, Groq, Anthropic, etc.). Configure credentials via environment variables expected by each backend (e.g. `OPENAI_API_KEY`, etc.).

| Provider    | Chat | Multimodal     | Notes                               |
| ----------- | ---- | -------------- | ----------------------------------- |
| OpenAI      | Yes  | Yes            | Broad model set (gpt‑4o, etc.)      |
| Groq        | Yes  | -              | Low latency llama variants          |
| Anthropic   | Yes  | Yes (Claude 3) | Strong reasoning, tool intents      |
| Gemini      | Yes  | Yes            | Native multimodal                   |
| Mistral     | Yes  | Partial        | Lightweight fast models             |
| Cohere      | Yes  | Limited        | Command models                      |
| HuggingFace | Yes  | Varies         | Community hub (capabilities differ) |

Check the crate source and docs.rs for the authoritative list and any new additions.
