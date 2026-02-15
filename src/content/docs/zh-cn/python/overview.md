---
title: Python SDK 概览
description: ai-lib-python 的架构与设计 — AI-Protocol 的开发者友好型 Python 运行时。
---

# Python SDK 概览

**ai-lib-python**（v0.6.0）是 AI-Protocol 的官方 Python 运行时。它提供开发者友好、 fully async 的接口，具备 Pydantic v2 类型安全与生产级 telemetry。

## 架构

Python SDK 镜像 Rust 运行时的分层架构：

### 客户端层（`client/`）
- **AiClient** — 带工厂方法的主入口
- **AiClientBuilder** — 流式配置构建器
- **ChatRequestBuilder** — 请求构建
- **ChatResponse** / **CallStats** — 响应类型
- **CancelToken** / **CancellableStream** — 流取消

### 协议层（`protocol/`）
- **ProtocolLoader** — 从本地/env/GitHub 加载清单并缓存
- **ProtocolManifest** — 提供商配置的 Pydantic 模型
- **Validator** — JSON Schema 验证（fastjsonschema）

### 管道层（`pipeline/`）
- **Decoder** — SSE、JSON Lines、Anthropic SSE 解码器
- **Selector** — 基于 JSONPath 的帧选择（jsonpath-ng）
- **Accumulator** — 工具调用组装
- **FanOut** — 多候选展开
- **EventMapper** — 协议驱动、Default 与 Anthropic mapper

### 传输层（`transport/`）
- **HttpTransport** — 基于 httpx 的异步 HTTP 与流式
- **Auth** — 从环境变量和 keyring 解析 API 密钥
- **ConnectionPool** — 性能优化的连接池

### 弹性层（`resilience/`）
- **ResilientExecutor** — 整合所有模式
- **RetryPolicy** — 指数退避
- **RateLimiter** — 令牌桶
- **CircuitBreaker** — 故障隔离
- **Backpressure** — 并发限制
- **FallbackChain** — 多目标故障转移
- **PreflightChecker** — 统一请求门控

### 路由层（`routing/`）
- **ModelManager** — 模型注册与选择
- **ModelArray** — 跨端点的负载均衡
- **Selection strategies** — 轮询、加权、成本优先、质量优先

### Telemetry 层（`telemetry/`）
- **MetricsCollector** — Prometheus 指标导出
- **Tracer** — OpenTelemetry 分布式追踪
- **Logger** — 结构化日志
- **HealthChecker** — 服务健康监控
- **FeedbackCollector** — 用户反馈

### 额外模块
- **embeddings/** — 带向量操作的 EmbeddingClient
- **cache/** — 多后端缓存（内存、磁盘）
- **tokens/** — TokenCounter（tiktoken）与成本估算
- **batch/** — 带并发控制的 BatchCollector/Executor
- **plugins/** — 插件基类、注册表、钩子、中间件
- **structured/** — JSON 模式、schema 生成、输出验证
- **guardrails/** — 内容过滤、验证器

## 核心依赖

| 包 | 用途 |
|---------|---------|
| `httpx` | 异步 HTTP 客户端 |
| `pydantic` | 数据验证与类型 |
| `pydantic-settings` | 配置管理 |
| `fastjsonschema` | 清单验证 |
| `jsonpath-ng` | JSONPath 表达式 |
| `pyyaml` | YAML 解析 |

### 可选

| Extra | 包 |
|-------|----------|
| `[telemetry]` | OpenTelemetry、Prometheus |
| `[tokenizer]` | tiktoken |
| `[full]` | 以上全部 + watchdog、keyring |

## V2 协议对齐

v0.6.0 与 AI-Protocol V2 规范对齐：

- **标准错误码** — `errors/standard_codes.py` 中的 13 个 frozen dataclass 码（E1001–E9999）
- **Capability Extras** — 8 个 pip extras（vision、audio、embeddings、structured、batch、agentic、telemetry、tokenizer）及 "full" 元 extra
- **合规测试** — 20/20 跨运行时测试用例通过
- **协议版本支持** — 支持协议版本 1.0、1.1、1.5、2.0

## Python 版本

需要 **Python 3.10+**。

## 下一步

- **[快速开始](/python/quickstart/)** — 快速运行
- **[AiClient API](/python/client/)** — 详细 API 指南
- **[流式管道](/python/streaming/)** — 管道内部实现
- **[弹性](/python/resilience/)** — 可靠性模式
