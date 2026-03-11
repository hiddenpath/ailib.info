---
title: 简介
description: AI-Lib 生态系统概览 —— AI-Protocol 规范及其 Rust、Python、TypeScript、Go 运行时实现。
---

# 欢迎使用 AI-Lib

**AI-Lib** 是一个开源生态系统，用于标准化应用程序与 AI 模型的交互方式。您无需为每个 AI 服务编写特定于供应商的代码，只需使用统一的 API —— 协议配置会处理其余一切。

## 核心理念

> **所有逻辑都是运算符，所有配置都是协议。**

传统 AI SDK 将供应商特定逻辑嵌入代码：不同的 HTTP 端点、不同的参数名、不同的流式格式、不同的错误码。切换供应商时，您需要重写代码。

AI-Lib 采用了不同的方法：

- **AI-Protocol** 在 YAML 清单中定义如何与每个供应商通信
- **运行时实现**（Rust、Python、TypeScript、Go）读取这些清单并执行请求
- **零硬编码逻辑** — 代码中没有任何 `if provider == "openai"` 之类的分支

## 六个项目，一个生态系统

- **ai-protocol** (v0.8.3)：与提供商无关的规范库。核心 schemas、V2 manifests 和验证工具。
- **ai-lib-rust** (v0.9.3)：高性能 Rust 运行时，发布于 crates.io。
- **ai-lib-python** (v0.8.3)：对开发者友好的 Python 运行时，发布于 PyPI。
- **ai-lib-ts** (v0.5.3)： 面向 npm 生态的 TypeScript/Node.js 运行时。
- **ai-lib-go** (v0.0.1)： 面向高并发的 Go 运行时，直接映射 V2 规范。
- **ai-protocol-mock** (v0.1.11)：为所有运行时提供集成测试的统一 Mock 服务器。

当前发布周期在 V2 架构能力基础上，补齐了执行治理门禁：`drift`、`manifest-consumption`、`compliance-matrix`、`fullchain`、`release-gate`，并支持 `--report-only` 分级治理。

### AI-Protocol（规范）

自从 v0.8.x 里程碑以来，**AI-Protocol V2** 高度依赖声明式配置 (`v2/providers/*.yaml`)。这避免了在代码中隐藏提供商的具体细节，并且通过 Schema 映射，整个生态已经支持超过 37 家提供商（10 家 V2 + 27 家 V1）。

### ai-lib-rust（Rust 运行时）

高性能运行时。基于运算符的流式管道通过可组合的阶段（Decoder → Selector → Accumulator → EventMapper）处理响应。内置熔断器、限流器和背压等弹性机制。发布于 Crates.io。

### ai-lib-python（Python 运行时）

开发者友好的运行时。完整的 async/await 支持、Pydantic v2 类型安全、生产级遥测（OpenTelemetry + Prometheus）以及智能模型路由。发布于 PyPI。

### ai-lib-ts（TypeScript 运行时）

面向 Node.js/npm 的运行时实现。支持 V2 清单加载、统一错误语义、流式处理、弹性模块与跨运行时合规矩阵执行。

### ai-lib-go（Go 运行时）

面向服务器端部署优化的高并发运行时。直接映射 V2 规范，具备上下文感知的弹性机制与高效的流式接口。

## 核心特性

- **37 供应商**（10 家 V2 + 27 家 V1）— OpenAI、Anthropic、Gemini、DeepSeek、Qwen 等
- **统一流式** — 无论供应商如何，都使用相同的 `StreamingEvent` 类型
- **协议驱动** — 所有行为在 YAML 中定义，而非代码中
- **热重载** — 更新供应商配置无需重启
- **弹性** — 熔断器、限流、重试、回退
- **工具调用** — 跨供应商的统一函数调用
- **嵌入** — 向量运算与相似度搜索
- **类型安全** — 编译时（Rust/Go）与运行时（Pydantic/TS）验证
- **V2 新特性** — MCP 工具桥接、Computer Use 抽象、扩展多模态、ProviderDriver、能力注册表、CLI 工具

## 运行时对比表

| 能力         | 协议标准      | Rust SDK            | Python SDK               | TypeScript SDK              | Go SDK                       |
| ------------ | ------------- | ------------------- | ------------------------ | --------------------------- | ---------------------------- |
| **类型系统** | JSON Schema   | 编译时验证          | 运行时验证 (Pydantic v2) | 编译时验证 (TypeScript)     | 编译时验证 (Go Structs)      |
| **流式传输** | SSE / NDJSON  | tokio async streams | async generators         | AsyncIterator + fetch       | Iterators (iter.Seq2)        |
| **弹性设计** | 重试策略规范  | 熔断器、背压控制    | ResilientExecutor        | RetryPolicy, CircuitBreaker | Context timeouts, auto-retry |
| **MCP**      | mcp.json 规范 | McpToolBridge       | McpToolBridge            | McpToolBridge               | 开发中                       |
| **分发方式** | GitHub / npm  | Crates.io           | PyPI                     | npm                         | goproxy                      |

## 下一步

- **[快速入门](/zh-cn/quickstart/)** — 几分钟内上手
- **[生态系统架构](/zh-cn/ecosystem/)** — 了解各组件如何协同
- **[AI-Protocol](/zh-cn/protocol/overview/)** — 深入了解规范
- **[Rust SDK](/zh-cn/rust/overview/)** — 从 Rust 开始
- **[Python SDK](/zh-cn/python/overview/)** — 从 Python 开始
- **[TypeScript SDK](/zh-cn/ts/overview/)** — 从 TypeScript 开始
- **[Go SDK](/zh-cn/go/overview/)** — 从 Go 开始
