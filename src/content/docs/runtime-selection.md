---
title: Choosing a Runtime
group: guides
order: 1
---

# Choosing the Right Runtime

The AI-Protocol ecosystem offers two production-ready runtimes: **ai-lib-rust** and **ai-lib-python**. Both implement the AI-Protocol specification and provide access to 30+ AI providers, but they excel in different scenarios.

## Quick Decision Guide

### Choose ai-lib-rust if you:

✅ Require maximum performance
✅ Need compile-time type safety
✅ Target embedded devices
✅ Build systems programming applications
✅ Want minimal runtime overhead
✅ Need rigorous memory control

### Choose ai-lib-python if you:

✅ Work in data science or ML
✅ Need rapid prototyping
✅ Use Jupyter notebooks
✅ Integrate with existing Python codebase
✅ Prefer runtime type validation
✅ Value ecosystem integration

## Detailed Comparison

| Feature | ai-lib-rust | ai-lib-python |
|---------|-------------|---------------|
| **Version** | v0.6.6 | v0.5.0 |
| **Performance** | <1ms overhead | ~10-50ms |
| **Type Safety** | Compile-time | Runtime (Pydantic v2) |
| **Memory** | Minimal overhead | Managed by Python |
| **Feature Parity** | 100% (reference) | ~95% |
| **Async Support** | tokio-based | httpx-based |
| **Distribution** | crates.io | PyPI |
| **Learning Curve** | Medium | Low |
| **Ecosystem** | Growing | Mature (data science) |

**Note**: Python SDK has 95% feature parity with Rust SDK. Missing features are typically performance-critical optimizations.

## Use Case Analysis

### Use Case 1: High-Performance API Service

**Setup**: Microservice that needs to process 1000+ requests/second with <10ms SLA

**Recommendation**: **ai-lib-rust**

**Why**:
- Minimal request overhead
- No garbage collection pauses
- Better resource utilization
- Predictable latency

### Use Case 2: Data Science Experimentation

**Setup**: Research team experimenting with different models and parameters

**Recommendation**: **ai-lib-python**

**Why**:
- Jupyter notebook support
- Integration with pandas, numpy
- Easy to iterate and prototype
- Familiar Python ecosystem

### Use Case 3: Machine Learning Pipeline

**Setup**: Production ML pipeline with scoring endpoints

**Recommendation**: **ai-lib-rust** OR **ai-lib-python**

**Why**:
- If latency-critical: Rust
- If integration with existing Python stack: Python
- Consider using Python for experimentation, Rust for production

### Use Case 4: CLI Application

**Setup**: Command-line tool that calls AI models

**Recommendation**: **ai-lib-rust**

**Why**:
- Fast startup time
- Minimal dependencies
- Easy cross-platform compilation
- Single binary distribution

### Use Case 5: Web Application (Python Framework)

**Setup**: Django/FastAPI web app with AI features

**Recommendation**: **ai-lib-python**

**Why**:
- Seamless framework integration
- Shared type system
- Same deployment process
- Familiar debugging tools

### Use Case 6: Embedded Device

**Setup**: AI assistant on IoT device with limited resources

**Recommendation**: **ai-lib-rust** (and possibly cross-compiled)

**Why**:
- Smaller binary size
- No runtime dependencies
- Memory-efficient
- Can be cross-compiled to ARM

## Migration Path

### From ai-lib-rust to ai-lib-python

The APIs are intentionally similar, so migration is straightforward:

```rust
// Rust
let client = AiClient::new(Provider::Groq)?;
let req = ChatCompletionRequest::new(model, messages);
let resp = client.chat_completion(req).await?;
```

```python
# Python
client = AIClient(Provider.GROQ)
req = ChatCompletionRequest(model, messages)
resp = client.chat_completion(req)
```

### From ai-lib-python to ai-lib-rust

Similar structure, but with Rust's ownership model:

```python
# Python
async for chunk in client.chat_completion_stream(req):
    print(chunk.choices[0].delta.content)
```

```rust
// Rust
let mut stream = client.chat_completion_stream(req).await?;
while let Some(chunk) = stream.next().await {
    println!("{}", chunk.choices[0].delta.content);
}
```

## Conclusion

Both runtimes are production-ready and implement the AI-Protocol specification:

- **ai-lib-rust** - Choose when performance, type safety, and systems-level control are priorities
- **ai-lib-python** - Choose when flexibility, ecosystem integration, and rapid development are priorities

For most applications, either runtime will work well. Start with the language you're most comfortable with and only optimize later if needed.

If you're still unsure, try both! The APIs are designed to be similar, and you can easily switch.

## Additional Resources

- [ai-lib-rust Documentation](/rust/)
- [ai-lib-python Documentation](/python/)
- [AI-Protocol Specification](/protocol/)
- [Example Projects](/examples/)
