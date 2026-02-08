---
title: Ecosystem Architecture
group: introduction
order: 1
description: Visual guide to the AI-Protocol ecosystem architecture
---

# AI-Protocol Ecosystem Architecture

This document provides visual architecture diagrams and detailed explanations of how the AI-Protocol ecosystem components interact.

## Ecosystem Overview

```mermaid
flowchart TB
    subgraph Apps["Your Applications"]
        App1["Web App"]
        App2["CLI Tool"]
        App3["ML Pipeline"]
    end

    subgraph Runtimes["Runtime Implementations"]
        Rust["<b>ai-lib-rust</b><br/>v0.6.6<br/>High Performance"]
        Python["<b>ai-lib-python</b><br/>v0.5.0<br/>ML Focused"]
    end

    subgraph Protocol["AI-Protocol Specification"]
        Manifests["Provider Manifests"]
        Models["Model Registry"]
        Operators["Operator System"]
    end

    subgraph Providers["30+ AI Providers"]
        Global["Global: OpenAI, Anthropic, Groq, Gemini"]
        China["China: Qwen, DeepSeek, Zhipu, Moonshot"]
        Local["Local: Ollama, vLLM, LocalAI"]
    end

    Apps --> Runtimes
    Runtimes --> Protocol
    Protocol --> Providers

    style Rust fill:#f97316,color:#fff
    style Python fill:#22c55e,color:#fff
    style Protocol fill:#8b5cf6,color:#fff
```

## Runtime Architecture Comparison

```mermaid
graph LR
    subgraph ai-lib-rust["ai-lib-rust (14 Layers)"]
        direction TB
        R1["Protocol Layer"]
        R2["Manifest Loader"]
        R3["Model Registry"]
        R4["Pipeline Engine"]
        R5["Interceptors"]
        R6["Retry/Circuit Breaker"]
        R7["Rate Limiter"]
        R8["Request Builder"]
        R9["Transport (HTTP)"]
        R1 --> R2 --> R3 --> R4 --> R5 --> R6 --> R7 --> R8 --> R9
    end

    subgraph ai-lib-python["ai-lib-python (7 Layers)"]
        direction TB
        P1["Protocol Layer"]
        P2["Client Interface"]
        P3["Provider Adapters"]
        P4["Retry Logic"]
        P5["Transport (httpx)"]
        P1 --> P2 --> P3 --> P4 --> P5
    end

    style ai-lib-rust fill:#1e293b,color:#fff
    style ai-lib-python fill:#1e3a2f,color:#fff
```

## Request Flow

```mermaid
sequenceDiagram
    participant App as Application
    participant RT as Runtime
    participant Proto as Protocol
    participant Prov as Provider API

    App->>RT: chat.complete(model, messages)
    RT->>Proto: Validate & Route
    Proto->>Proto: Select Provider
    Proto->>RT: Provider Config
    RT->>Prov: HTTP Request
    Prov-->>RT: Response
    RT->>Proto: Parse Response
    Proto-->>RT: Normalized Data
    RT-->>App: Unified Response
```

## Provider Support Matrix

| Category | Providers | Status |
|----------|-----------|--------|
| **Global Tier 1** | OpenAI, Anthropic, Gemini | ✅ Full |
| **Global Tier 2** | Groq, Mistral, Cohere, Perplexity | ✅ Full |
| **China Region** | Qwen, DeepSeek, Zhipu, Moonshot | ✅ Full |
| **Self-Hosted** | Ollama, vLLM, LocalAI | ✅ Full |
| **Specialized** | Together, Fireworks, DeepInfra | ✅ Full |

## Key Design Principles

### 1. Protocol-First
All behavior is defined by the protocol specification, not hard-coded in runtimes.

### 2. Zero Lock-In
Switch providers without code changes - just update configuration.

### 3. Type Safety
Both runtimes provide strong typing:
- **Rust**: Compile-time guarantees
- **Python**: Pydantic v2 runtime validation

### 4. Performance
- **Rust**: <1ms overhead, zero-copy parsing
- **Python**: Async-first, connection pooling

## Getting Started

Choose your path:

- 🦀 **Rust developers**: [Get Started with ai-lib-rust](/rust/quick-start/)
- 🐍 **Python developers**: [Get Started with ai-lib-python](/python/quick-start/)
- 📋 **Protocol implementers**: [View AI-Protocol Spec](/protocol/)
