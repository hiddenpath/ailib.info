---
title: 简介
description: AI-Lib 生态系统概览 —— AI-Protocol 规范及其 Rust 与 Python 运行时实现。
---

# 欢迎使用 AI-Lib

**AI-Lib** 是一个开源生态系统，用于标准化应用程序与 AI 模型的交互方式。您无需为每个 AI 服务编写特定于供应商的代码，只需使用统一的 API —— 协议配置会处理其余一切。

## 核心理念

> **所有逻辑都是运算符，所有配置都是协议。**

传统 AI SDK 将供应商特定逻辑嵌入代码：不同的 HTTP 端点、不同的参数名、不同的流式格式、不同的错误码。切换供应商时，您需要重写代码。

AI-Lib 采用了不同的方法：

- **AI-Protocol** 在 YAML 清单中定义如何与每个供应商通信
- **运行时实现**（Rust、Python）读取这些清单并执行请求
- **零硬编码逻辑** — 代码中没有任何 `if provider == "openai"` 之类的分支

## 三个项目，一个生态系统

| 项目 | 角色 | 语言 | 版本 | 分发渠道 |
|---------|------|----------|---------|---------------|
| **[AI-Protocol](/protocol/)** | 规范层 | YAML/JSON | v0.7.0 | GitHub |
| **[ai-lib-rust](/rust/)** | 运行时实现 | Rust | v0.8.0 | [Crates.io](https://crates.io/crates/ai-lib) |
| **[ai-lib-python](/python/)** | 运行时实现 | Python | v0.7.0 | [PyPI](https://pypi.org/project/ai-lib-python/) |

协议 v0.7.0 版本引入了 **V2 协议特性**：三层架构、标准化错误码、用于能力扩展的特性标志，以及确保各运行时行为一致的一致性测试套件。

### AI-Protocol（规范）

基础层。YAML 清单描述了 37 个 AI 供应商（6 个 V2 + 36 个 V1）：它们的端点、认证、参数映射、流式解码器配置、错误分类规则以及能力。JSON Schema 验证所有内容。

### ai-lib-rust（Rust 运行时）

高性能运行时。基于运算符的流式管道通过可组合的阶段（Decoder → Selector → Accumulator → EventMapper）处理响应。内置熔断器、限流器和背压等弹性机制。发布于 Crates.io。

### ai-lib-python（Python 运行时）

开发者友好的运行时。完整的 async/await 支持、Pydantic v2 类型安全、生产级遥测（OpenTelemetry + Prometheus）以及智能模型路由。发布于 PyPI。

## 核心特性

- **37 供应商**（6 个 V2 + 36 个 V1）— OpenAI、Anthropic、Gemini、DeepSeek、Qwen 等
- **统一流式** — 无论供应商如何，都使用相同的 `StreamingEvent` 类型
- **协议驱动** — 所有行为在 YAML 中定义，而非代码中
- **热重载** — 更新供应商配置无需重启
- **弹性** — 熔断器、限流、重试、回退
- **工具调用** — 跨供应商的统一函数调用
- **嵌入** — 向量运算与相似度搜索
- **类型安全** — 编译时（Rust）与运行时（Pydantic）验证
- **V2 新特性** — MCP 工具桥接、Computer Use 抽象、扩展多模态、ProviderDriver、能力注册表、CLI 工具

## 下一步

- **[快速入门](/quickstart/)** — 几分钟内上手
- **[生态系统架构](/ecosystem/)** — 了解各组件如何协同
- **[AI-Protocol](/protocol/overview/)** — 深入了解规范
- **[Rust SDK](/rust/overview/)** — 从 Rust 开始
- **[Python SDK](/python/overview/)** — 从 Python 开始
