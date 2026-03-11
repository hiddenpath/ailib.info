---
title: 生态系统架构
description: AI-Protocol、ai-lib-rust、ai-lib-python、ai-lib-ts 与 ai-lib-go 如何作为一体化生态系统协同工作。
---

# 生态系统架构

AI-Lib 生态系统建立在清晰的三层架构之上，每一层都有明确的职责。当前版本：**AI-Protocol v0.8.3**、**ai-lib-rust v0.9.3**、**ai-lib-python v0.8.3**、**ai-lib-ts v0.5.3**、**ai-lib-go v0.0.1**、**ai-protocol-mock v0.1.11**。

## 三层架构

### 1. 协议层 — AI-Protocol

**规范**层。YAML 清单定义：

- **供应商清单**（`providers/*.yaml`）— 37 供应商（6 个 V2 + 36 个 V1）的端点、认证、参数映射、流式解码器、错误分类
- **模型注册表**（`models/*.yaml`）— 包含上下文窗口、能力、定价的模型实例
- **核心规范**（`spec.yaml`）— 标准参数、事件、错误类型、重试策略
- **模式**（`schemas/`）— 所有配置的 JSON Schema 验证

协议层**与语言无关**。可被任意语言的任何运行时使用。

### 2. 运行时层 — Rust、Python、TypeScript 与 Go SDK

**执行**层。运行时实现：

- **协议加载** — 从本地文件、环境变量或 GitHub 读取并验证清单
- **请求编译** — 将统一请求转换为供应商特定的 HTTP 调用
- **流式管道** — 解码、选择、累积，并将供应商响应映射为统一事件
- **弹性** — 熔断器、限流、重试、回退
- **扩展** — 嵌入、缓存、批处理、插件

三个运行时共享同一套协议驱动架构：

| 概念 | Rust | Python | TypeScript |
|---------|------|--------|------------|
| Client | `AiClient` | `AiClient` | `AiClient` |
| Builder | `AiClientBuilder` | `AiClientBuilder` | `AiClientBuilder` |
| Request | `ChatRequestBuilder` | `ChatRequestBuilder` | `ChatBuilder` |
| Events | `StreamingEvent` enum | `StreamingEvent` class | 统一流式事件 |
| Transport | reqwest (tokio) | httpx (asyncio) | fetch (Node.js) |
| Types | Rust structs | Pydantic v2 models | TypeScript interfaces |

### 3. 应用层 — 您的代码

应用程序使用统一的运行时 API。单一的 `AiClient` 接口适用于所有供应商：

```
Your App → AiClient → Protocol Manifest → Provider API
```

只需更改一个模型标识符即可切换供应商。无需修改代码。

## 数据流

当您调用 `client.chat().user("Hello").stream()` 时，会发生以下过程：

1. **AiClient** 接收请求
2. **ProtocolLoader** 提供供应商清单
3. **请求编译器** 将标准参数映射为供应商特定的 JSON
4. **Transport** 使用正确的认证/头部发送 HTTP 请求
5. **管道** 处理流式响应：
   - **Decoder** 将字节转换为 JSON 帧（SSE 或 NDJSON）
   - **Selector** 使用 JSONPath 过滤相关帧
   - **Accumulator** 组装部分工具调用
   - **EventMapper** 将帧转换为统一的 `StreamingEvent`
6. **应用程序** 遍历统一事件

## 协议加载

三个运行时按以下顺序搜索协议清单：

1. **自定义路径** — 在构建器中显式设置
2. **环境变量** — `AI_PROTOCOL_DIR` 或 `AI_PROTOCOL_PATH`
3. **相对路径** — 工作目录下的 `ai-protocol/` 或 `../ai-protocol/`
4. **GitHub 回退** — 从 `hiddenpath/ai-protocol` 仓库下载

这意味着您可以在无本地配置的情况下开始开发 —— 运行时会自动从 GitHub 获取清单。

## V2 协议演进与治理增强

V2 基线在 `v0.8.2` 完成了生成式全链路治理闭环：

- **L1 核心协议** — 消息格式、标准错误码（E1001–E9999）、版本声明
- **L2 能力扩展** — 流式、视觉、工具、MCP、Computer Use、多模态
- **L3 环境配置** — API 密钥、端点、重试策略 —— 环境特定配置

新增执行治理门禁脚本：

- `npm run drift:check`
- `npm run gate:manifest-consumption`
- `npm run gate:compliance-matrix`
- `npm run gate:fullchain`
- `npm run release:gate`

并支持 `--report-only` 分级治理模式。

`ai-protocol-mock` 视频异步生命周期支持确定性终态：

- `succeeded`
- `failed`
- `cancelled`

可通过 `X-Mock-Video-Terminal` 或 `terminal_state` 控制。

跨 Rust/Python/TypeScript 的 compliance 矩阵现已覆盖 protocol loading、error classification、retry、message、stream、request 等关键语义维度。

## 与 MCP 的关系

AI-Protocol 与 MCP（Model Context Protocol）是**互补**的：

- **MCP** 处理高层关注 — 工具注册、上下文管理、代理协调
- **AI-Protocol** 处理低层关注 — API 标准化、流式格式转换、错误分类

它们在不同的层面运行，可以一起使用。

## 下一步

- **[AI-Protocol 概览](/protocol/overview/)** — 深入了解规范
- **[Rust SDK](/rust/overview/)** — 探索 Rust 运行时
- **[Python SDK](/python/overview/)** — 探索 Python 运行时
- **[TypeScript SDK](/ts/overview/)** — 探索 TypeScript 运行时
