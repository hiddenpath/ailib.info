---
title: Rust SDK 概览
description: ai-lib-rust 的架构与设计 — AI-Protocol 的高性能 Rust 运行时。
---

# Rust SDK 概览

**ai-lib-rust**（v0.7.1）是 AI-Protocol 规范的高性能 Rust 运行时。它采用协议驱动架构，所有提供商行为均来自配置而非代码。

## V2 协议对齐

ai-lib-rust v0.7.1 与 AI-Protocol V2 规范对齐：

- **标准错误码**：13 种变体的 `StandardErrorCode` 枚举（E1001–E9999），已集成到所有错误路径
- **功能标志**：7 种能力特性（`embeddings`、`batch`、`guardrails`、`tokens`、`telemetry`、`routing_mvp`、`interceptors`）以及 `full` 元特性
- **合规测试**：20/20 跨运行时测试用例通过
- **结构化输出**：支持模式验证的 JSON 模式

## 架构

SDK 划分为不同的层级：

### 客户端层（`client/`）
面向用户的 API：
- **AiClient** — 主入口，从模型标识符创建
- **AiClientBuilder** — 带弹性配置的构建器
- **ChatRequestBuilder** — 用于构建聊天请求的流式 API
- **CallStats** — 请求/响应统计（tokens、延迟）
- **CancelHandle** — 优雅的流取消

### 协议层（`protocol/`）
加载并解析 AI-Protocol 清单：
- **ProtocolLoader** — 从本地文件、环境变量或 GitHub 加载
- **ProtocolManifest** — 解析后的提供商配置
- **Validator** — JSON Schema 验证
- **UnifiedRequest** — 编译为提供商特定 JSON 的标准请求格式

### 管道层（`pipeline/`）
流式处理的核心 — 基于算子的管道：
- **Decoder** — 将字节流转换为 JSON 帧（SSE、JSON Lines）
- **Selector** — 使用 JSONPath 表达式过滤帧
- **Accumulator** — 有状态地组装来自部分块的工具调用
- **FanOut** — 展开多候选响应
- **EventMapper** — 将帧转换为统一的 `StreamingEvent` 类型
- **Retry/Fallback** — 管道级重试与回退算子

### 传输层（`transport/`）
HTTP 通信：
- **HttpTransport** — 基于 reqwest 的 HTTP 客户端
- **Auth** — API 密钥解析（OS keyring → 环境变量）
- **Middleware** — 用于日志、指标的传输中间件

### 弹性层（`resilience/`）
生产级可靠性模式：
- **CircuitBreaker** — 开/半开/闭故障隔离
- **RateLimiter** — 令牌桶算法
- **Backpressure** — max_inflight 信号量

### 额外模块
- **embeddings/** — 带向量操作的 EmbeddingClient
- **cache/** — 带 TTL 的响应缓存（MemoryCache）
- **batch/** — BatchCollector 与 BatchExecutor
- **tokens/** — Token 计数与成本估算
- **plugins/** — 插件 trait、注册表、钩子、中间件
- **guardrails/** — 内容过滤、PII 检测
- **routing/** — 模型路由与负载均衡（功能门控）
- **telemetry/** — 用户反馈收集的反馈接收器

## 核心依赖

| Crate | 用途 |
|-------|---------|
| `tokio` | 异步运行时 |
| `reqwest` | HTTP 客户端 |
| `serde` / `serde_json` / `serde_yaml` | 序列化 |
| `jsonschema` | 清单验证 |
| `tracing` | 结构化日志 |
| `arc-swap` | 热重载支持 |
| `notify` | 文件监听 |
| `keyring` | OS 密钥环集成 |

## 功能标志

通过 Cargo 启用可选功能（使用 `full` 启用全部）：

| 功能 | 启用内容 |
|---------|----------------|
| `embeddings` | EmbeddingClient、向量操作 |
| `batch` | BatchCollector、BatchExecutor |
| `guardrails` | 内容过滤、PII 检测 |
| `tokens` | Token 计数、成本估算 |
| `telemetry` | 高级可观测性接收器 |
| `routing_mvp` | CustomModelManager、ModelArray、负载均衡策略 |
| `interceptors` | 用于日志、指标、审计的 InterceptorPipeline |

## 环境变量

| 变量 | 用途 |
|----------|---------|
| `AI_PROTOCOL_DIR` | 协议清单目录 |
| `<PROVIDER>_API_KEY` | 提供商 API 密钥（如 `OPENAI_API_KEY`） |
| `AI_LIB_RPS` | 速率限制（每秒请求数） |
| `AI_LIB_BREAKER_FAILURE_THRESHOLD` | 熔断器阈值 |
| `AI_LIB_MAX_INFLIGHT` | 最大并发请求数 |
| `AI_HTTP_TIMEOUT_SECS` | HTTP 超时 |

## 下一步

- **[快速开始](/rust/quickstart/)** — 数分钟即可运行
- **[AiClient API](/rust/client/)** — 客户端使用详情
- **[流式管道](/rust/streaming/)** — 管道深入解析
- **[弹性](/rust/resilience/)** — 可靠性模式
