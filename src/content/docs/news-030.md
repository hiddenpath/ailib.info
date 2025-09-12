---
title: Release v0.3.2
group: News
order: 1
status: stable
---

# ai-lib v0.3.2

Highlights:

- **Enhanced Reliability Features**: Improved streaming performance and error handling
- **JSONL Streaming Protocol**: Complete implementation with delta/final types for structured streaming
- **Unified Transport APIs**: Standardized HTTP client factory and configuration across all providers
- **Function Calling Compatibility**: Cross-provider support for OpenAI-style `tool_calls` and auto-parse of stringified JSON arguments
- **Interceptor Pipeline**: Pluggable `InterceptorPipeline` with default/minimal presets for retry, timeout, and circuit breaker patterns
- **Enterprise-Ready Architecture**: Foundation for ai-lib-pro enterprise features

New Features:

- **Incremental JSON Parser**: High-performance streaming content extraction with proper error handling
- **Enhanced Examples**: Comprehensive examples for all major providers and use cases
- **Golden Test Cases**: Extensive SSE streaming test coverage with MD5 consistency validation
- **Configurable Streaming Demos**: Model override support via environment variables
- **Builder UX Improvements**: `AiClientBuilder` with enhanced configuration options

Quick links:

- Routing guide: /docs/reliability-routing
- Observability: /docs/observability
- Enterprise features: /docs/enterprise-pro
- GitHub Releases: https://github.com/hiddenpath/ai-lib/releases

