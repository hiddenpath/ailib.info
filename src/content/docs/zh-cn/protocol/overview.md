---
title: AI-Protocol 概览
description: 了解 AI-Protocol 规范 —— AI-Lib 生态系统中与供应商无关的基础。
---

# AI-Protocol 概览

AI-Protocol 是一个**与供应商无关的规范**，用于标准化与 AI 模型的交互。它将运行时需要了解的有关供应商的信息（配置）与执行请求的方式（代码）分离。

## 核心哲学

> **所有逻辑都是运算符，所有配置都是协议。**

所有供应商特定的行为 —— 端点、认证、参数名、流式格式、错误码 —— 均在 YAML 配置文件中声明。运行时实现中**没有任何硬编码的供应商逻辑**。

## 仓库内容

```
ai-protocol/
├── v1/
│   ├── spec.yaml          # Core specification (v0.7.0)
│   ├── providers/          # 37 provider manifests (6 V2 + 36 V1)
│   │   ├── openai.yaml
│   │   ├── anthropic.yaml
│   │   ├── gemini.yaml
│   │   ├── deepseek.yaml
│   │   └── ...
│   └── models/             # Model instance registry
│       ├── gpt.yaml
│       ├── claude.yaml
│       └── ...
├── schemas/                # JSON Schema validation
│   ├── v1.json
│   └── spec.json
├── dist/                   # Pre-compiled JSON (generated)
├── scripts/                # Build & validation tools
└── examples/               # Usage examples
```

## 供应商清单

每个供应商都有一个 YAML 清单，声明运行时所需的全部信息：

| 部分 | 用途 |
|---------|---------|
| `endpoint` | 基础 URL、聊天路径、协议 |
| `auth` | 认证类型、token 环境变量、头部 |
| `parameter_mappings` | 标准 → 供应商特定参数名 |
| `streaming` | 解码器格式（SSE/NDJSON）、事件映射规则（JSONPath） |
| `error_classification` | HTTP 状态 → 标准错误类型 |
| `retry_policy` | 策略、延迟、重试条件 |
| `rate_limit_headers` | 限流信息的头部名称 |
| `capabilities` | 特性标志（流式、工具、视觉、推理） |

### 示例：Anthropic 供应商

```yaml
id: anthropic
protocol_version: "0.7"
endpoint:
  base_url: "https://api.anthropic.com/v1"
  chat_path: "/messages"
auth:
  type: bearer
  token_env: "ANTHROPIC_API_KEY"
  headers:
    anthropic-version: "2023-06-01"
parameter_mappings:
  temperature: "temperature"
  max_tokens: "max_tokens"
  stream: "stream"
  tools: "tools"
streaming:
  decoder:
    format: "anthropic_sse"
  event_map:
    - match: "$.type == 'content_block_delta'"
      emit: "PartialContentDelta"
      extract:
        content: "$.delta.text"
    - match: "$.type == 'message_stop'"
      emit: "StreamEnd"
error_classification:
  by_http_status:
    "429": "rate_limited"
    "401": "authentication"
    "529": "overloaded"
capabilities:
  streaming: true
  tools: true
  vision: true
  reasoning: true
```

## 模型注册表

模型在注册表中关联供应商引用、能力和定价：

```yaml
models:
  claude-3-5-sonnet:
    provider: anthropic
    model_id: "claude-3-5-sonnet-20241022"
    context_window: 200000
    capabilities: [chat, vision, tools, streaming, reasoning]
    pricing:
      input_per_token: 0.000003
      output_per_token: 0.000015
```

## 验证

所有清单均使用 AJV 针对 JSON Schema (2020-12) 进行验证。CI 流程确保正确性：

```bash
npm run validate    # Validate all configurations
npm run build       # Compile YAML → JSON
```

## 版本控制

AI-Protocol 使用分层版本控制：

1. **规范版本**（`v1/spec.yaml`）— 模式结构版本（当前为 v0.7.0）
2. **协议版本**（在清单中）— 使用的协议特性（当前为 0.7）
3. **发布版本**（`package.json`）— 规范包的 SemVer（v0.7.0）

## V2 协议架构

协议 v0.7.0 引入了 **V2 架构** —— 跨层关注点清晰分离，以及同心圆清单模型。

### 三层金字塔

- **L1 核心协议** — 消息格式、标准错误码（E1001–E9999）、版本声明。所有供应商必须实现此层。
- **L2 能力扩展** — 流式、视觉、工具。每个扩展由特性标志控制；供应商按能力选择加入。
- **L3 环境配置** — API 密钥、端点、重试策略。环境特定配置，可在不改变供应商逻辑的情况下覆盖。

### 同心圆清单模型

- **环 1 核心骨架**（必需）— 有效清单的最小字段：endpoint、auth、parameter mappings
- **环 2 能力映射**（条件）— 流式配置、工具映射、视觉参数 —— 供应商支持时提供
- **环 3 高级扩展**（可选）— 自定义头部、限流头部、高级重试策略

### V2-Alpha 供应商

OpenAI、Anthropic 和 Gemini 已提供 **v2-alpha** 格式。这些清单使用 Ring 1/2/3 结构，可与 v1 清单一起使用。

### V2 扩展能力

V2 架构引入了多项扩展能力：

- **MCP 工具桥接** — 与 Model Context Protocol 集成，支持工具注册和上下文管理
- **Computer Use 抽象** — 标准化计算机操作接口，支持跨供应商的统一计算机使用能力
- **扩展多模态** — 增强的多模态模式定义，支持更丰富的视觉和多媒体交互
- **ProviderDriver** — 可插拔的供应商驱动架构，便于扩展和自定义
- **能力注册表** — 统一的能力发现和管理机制
- **CLI 工具** — 命令行工具支持协议验证、清单管理和测试

### 标准错误码

V2 定义了 13 个标准化错误码（E1001–E9999），分为 5 类：客户端错误（E1xxx）、速率/配额（E2xxx）、服务端（E3xxx）、冲突/取消（E4xxx）和未知（E9999）。完整代码列表请参阅[规范](/protocol/spec/)。

### 跨运行时一致性

**一致性测试套件**确保 Rust 和 Python 运行时的行为一致。所有 V2 供应商在两个实现中均通过相同的测试矩阵。

## 下一步

- **[规范详情](/protocol/spec/)** — 核心规范详解
- **[供应商清单](/protocol/providers/)** — 清单工作原理
- **[模型注册表](/protocol/models/)** — 模型配置
- **[贡献供应商](/protocol/contributing/)** — 添加新供应商
