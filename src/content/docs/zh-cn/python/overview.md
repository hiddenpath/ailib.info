---
title: Python SDK 概述
description: ai-lib-python v1.0.0 架构与公开 API — AI-Protocol 的异步 Python 运行时。
---

# Python SDK 概述

**ai-lib-python**（v1.0.0）是 [AI-Protocol](https://github.com/ailib-official/ai-protocol) 的 Python 运行时。与 Rust 的 workspace crate 不同，Python 以**单一包**发布，并清晰划分**执行 / 策略模块**：

| 层级 | 模块 | 职责 |
|------|------|------|
| 执行层（E） | `client`、`protocol`、`pipeline`、`transport`、`types`、`structured`、可选能力模块 | 清单加载、算子 pipeline、httpx transport |
| 策略层（P） | `resilience`、`cache`、`routing`、`plugins`、`guardrails`、`batch`、`telemetry`、`tokens` | 重试、限流、路由 — 在客户端旁按需启用 |

## 主要执行路径

聊天场景下，**`AiClient` 不会调用 `ProviderDriver`**。流程为：

1. 加载提供商清单（`ProtocolLoader`）
2. 根据清单算子构建 **`Pipeline`**
3. 通过 **`HttpTransport`**（httpx）发送 HTTP
4. 产出统一的 **`StreamingEvent`**（Pydantic 模型）

提供商特有逻辑仍然存在（SSE 解码器、可选 driver、独立服务客户端），但默认集成路径是清单 + pipeline。

## 公开 API 一览

**始终从 `ai_lib_python` 导出：**

- `AiClient`、`AiClientBuilder`、`ChatResponse`、`CallStats`
- `Message`、`MessageRole`、`MessageContent`、`ContentBlock`、`StreamingEvent`、`ToolCall`、`ToolDefinition`
- `AiLibError`、`ProtocolError`、`TransportError`
- 能力探测：`HAS_VISION`、`HAS_AUDIO`、`HAS_TELEMETRY`、`HAS_TOKENIZER`、`HAS_WATCHDOG`、`HAS_KEYRING`、`require_extra`

需要时**显式导入子包**：`resilience`、`structured`、`embeddings`、`mcp`、`computer_use`、`drivers` 等。

## V2 对齐（当前真实能力）

- **清单加载：** V1 + V2 路径（`dist/v2/providers/*.json`、`v2/providers/*.yaml`、…）
- **标准错误码：** 13 个码（E1001–E9999）
- **结构化输出：** `structured` 模块
- **文本工具 / TTC：** `ai_lib_python.types.text_tool` 下的类型
- **能力注册表：** `registry.CapabilityRegistry`，含 pip-extra 检测

### 能力边界（如实描述）

| 领域 | 包内提供 | 不包含 |
|------|----------|--------|
| **MCP** | `McpToolBridge` 格式转换 | 接入 `AiClient` 的 MCP 服务端传输 |
| **Computer Use** | `ComputerAction`、`SafetyPolicy` 校验 | 截图 / 输入执行环境 |
| **Embeddings / STT / TTS / Rerank** | 独立 HTTP 客户端 | 各模态的完整 pipeline 算子 |
| **热更新** | Builder 标志 + 内存缓存 | 自动文件监听（需 `watchdog`；未端到端接线） |
| **`ProviderDriver`** | 公开 `drivers` 模块 | 默认 `AiClient` 聊天路径 |

## 架构（包布局）

### Client（`client/`）

- `AiClient` — 异步入口（`await AiClient.create("provider/model")`）
- `ChatRequestBuilder` — `.messages()`、`.system()`、`.user()`、`.stream()`、`.execute()`、`.execute_with_stats()`
- `AiClientBuilder` — `.production_ready()`、`.hot_reload()`、韧性相关旋钮

### Protocol（`protocol/`）

- `ProtocolLoader`、`ProtocolManifest`、校验器
- V2 类型位于 `protocol.v2`

### Pipeline（`pipeline/`）

Decoder → Selector → Accumulator → FanOut → EventMapper（由清单配置）。

### Transport（`transport/`）

`HttpTransport`、凭证解析（`keyring` 或 `<PROVIDER>_API_KEY`）。

### Policy（`resilience/`、`routing/`、…）

按需启用的模块 — 使用 `AiClientBuilder.production_ready()` 或显式接线 `ResilientConfig`；`AiClient.create()` 不会自动开启。

## Pip 可选依赖

| Extra | 启用内容 |
|-------|----------|
| `vision` / `audio` | 多模态辅助（`HAS_VISION`、`HAS_AUDIO`） |
| `embeddings` | `EmbeddingClient` |
| `stt` / `tts` / `reranking` | 独立服务客户端 |
| `batch` | 批处理收集器 / 执行器 |
| `telemetry` | OpenTelemetry 集成 |
| `tokenizer` | 基于 tiktoken 的计数 |
| `full` | 全部可选能力 + `watchdog`、`keyring` |

```bash
pip install ai-lib-python[full]
```

## 下一步

- [快速开始](/zh-cn/python/quickstart/) — 安装与首次聊天
- [AiClient API](/zh-cn/python/client/) — builder 参考
- [流式处理](/zh-cn/python/streaming/) — 事件处理
- [韧性模式](/zh-cn/python/resilience/) — 按需策略层
