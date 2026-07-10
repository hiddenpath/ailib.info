---
title: Rust SDK 概述
description: ai-lib-rust v1.0.1 架构与公开 API — AI-Protocol 的高性能 Rust 运行时。
---

# Rust SDK 概述

**ai-lib-rust**（v1.0.1）是 [AI-Protocol](https://github.com/ailib-official/ai-protocol) 的 Rust 运行时。发布的 crate 是覆盖两个 workspace crate 的**门面**：

| Crate | 职责 |
|-------|------|
| `ai-lib-core` | 执行层：`AiClient`、`pipeline`、`protocol`、`transport`、`types`、`structured` |
| `ai-lib-contact` | 策略层：`resilience`、`cache`、`routing`、`plugins`、`guardrails`、`batch`、`telemetry` |

## 主要执行路径

聊天场景下，**`AiClient` 不会调用 `ProviderDriver`**。流程为：

1. 加载提供商清单（`ProtocolLoader`）
2. 根据清单算子构建 **`Pipeline`**
3. 通过 **`HttpTransport`** 发送 HTTP
4. 产出统一的 **`StreamingEvent`**

提供商特有逻辑仍然存在（SSE 解码器、可选 driver、独立服务客户端），但默认集成路径是清单 + pipeline。

## 公开 API 一览

**始终从 `ai_lib_rust` 导出：**

- `AiClient`、`AiClientBuilder`、`ChatBatchRequest`、`CancelHandle`、`CallStats`
- `Message`、`MessageRole`、`StreamingEvent`、`ToolCall`
- `StandardErrorCode`、`Error`、`Result`
- `structured`（JSON 模式 / schema 校验）
- 文本工具辅助：`StandardTextToolParser`、`ToolCallingPolicy`、…
- 策略模块：`cache`、`context`、`plugins`、`resilience`

**按 feature 门控**（见 [Feature 标志](#feature-标志)）：

- Core：`embeddings`、`mcp`、`computer_use`、`multimodal`、`stt`、`tts`、`rerank`
- Contact：`batch`、`guardrails`、`telemetry`、`tokens`、`routing_mvp`、`interceptors`

## V2 对齐（当前真实能力）

- **清单加载：** V1 + V2 路径（`dist/v2/providers/*.json`、`v2/providers/*.yaml`、…）
- **标准错误码：** 13 变体 `StandardErrorCode`（E1001–E9999）
- **结构化输出：** `JsonModeConfig`、`OutputValidator`（始终可用）
- **文本工具 / TTC：** crate 根部的 `StandardTextToolParser` 与策略类型
- **能力注册表：** `registry::CapabilityRegistry`（feature 缺口检测）

### 能力边界（如实描述）

| 领域 | 运行时提供 | 不包含 |
|------|------------|--------|
| **MCP**（`mcp` feature） | `McpToolBridge` 格式转换 | 接入 `AiClient` 的 MCP 服务端传输 |
| **Computer Use**（`computer_use`） | `ComputerAction`、`SafetyPolicy` 校验 | 截图 / 输入执行环境 |
| **Embeddings / STT / TTS / Rerank** | 独立 HTTP 客户端 | 各模态的完整 pipeline 算子 |
| **热更新** | 清单内存缓存 | 文件监听 / 自动重载 |
| **`ProviderDriver`** | 公开 `drivers` 模块 | 默认 `AiClient` 聊天路径 |

## 架构（workspace 路径）

### Client（`crates/ai-lib-core/src/client/`）

- `AiClient` — 入口（`"provider/model"` id）
- `ChatRequestBuilder` — `.messages()`、`.stream()`、`.execute()`、`.execute_stream()`
- `chat_batch` / `chat_batch_smart` — 始终在 `AiClient` 上（不依赖 `batch` feature）

### Protocol（`crates/ai-lib-core/src/protocol/`）

- `ProtocolLoader`、`ProtocolManifest`、校验器
- V2 类型位于 `protocol::v2`

### Pipeline（`crates/ai-lib-core/src/pipeline/`）

Decoder → Selector → Accumulator → FanOut → EventMapper（由清单配置）。

### Transport（`crates/ai-lib-core/src/transport/`）

`HttpTransport`、凭证解析（`keyring` 或 `<PROVIDER>_API_KEY`）。

### Policy（`crates/ai-lib-contact/src/`）

按需启用的模块 — 在 `AiClient` 旁导入并接线；`AiClient::new` 不会自动开启。

## Feature 标志

| Feature | 启用内容 |
|---------|----------|
| `embeddings` | `EmbeddingClient` |
| `stt` / `tts` / `reranking` | `SttClient`、`TtsClient`、`RerankerClient` |
| `mcp` | `McpToolBridge` |
| `computer_use` | `ComputerAction`、`SafetyPolicy` |
| `multimodal` | `MultimodalCapabilities` |
| `batch` | `BatchExecutor`（contact）；`chat_batch` 始终可用 |
| `guardrails` | 内容过滤器 |
| `telemetry` | 高级反馈 sink |
| `routing_mvp` | `CustomModelManager`、`ModelArray` |
| `full` | 以上全部 |

```toml
ai-lib-rust = { version = "1.0.1", features = ["embeddings"] }
```

## 韧性

- **`AiClient`：** `max_inflight` 背压（`AI_LIB_MAX_INFLIGHT`）
- **`ai_lib_rust::resilience`：** 重试、限流、熔断 — 需显式配置
- **默认客户端未内置：** 每次 `AiClient::new` 不会自动挂载熔断 / 限流

## 环境变量

| 变量 | 用途 |
|------|------|
| `AI_PROTOCOL_DIR` / `AI_PROTOCOL_PATH` | 本地或远程清单根路径 |
| `<PROVIDER>_API_KEY` | API 密钥（如 `OPENAI_API_KEY`） |
| `AI_LIB_MAX_INFLIGHT` | 并发请求上限 |
| `AI_LIB_BATCH_CONCURRENCY` | 批处理 worker 数量 |
| `AI_HTTP_TIMEOUT_SECS` | HTTP 超时 |
| `AI_PROXY_URL` | 显式代理覆盖 |

## 下一步

- **[快速开始](/zh-cn/rust/quickstart/)** — 安装与首次聊天
- **[AiClient API](/zh-cn/rust/client/)** — builder 方法
- **[流式处理](/zh-cn/rust/streaming/)** — pipeline 与事件
- **[韧性模式](/zh-cn/rust/resilience/)** — 策略层
- **[高级功能](/zh-cn/rust/advanced/)** — embeddings、缓存、插件

权威来源：[ai-lib-rust README](https://github.com/ailib-official/ai-lib-rust/blob/main/README.md)。
