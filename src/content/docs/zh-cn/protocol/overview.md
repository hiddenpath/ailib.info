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
│   ├── spec.yaml          # Core specification
│   ├── providers/          # V1 provider manifests
│   │   ├── openai.yaml
│   │   ├── anthropic.yaml
│   │   ├── gemini.yaml
│   │   ├── deepseek.yaml
│   │   └── ...
│   └── models/             # Model instance registry
│       ├── gpt.yaml
│       ├── claude.yaml
│       └── ...
├── v2/
│   └── providers/          # V2 provider manifests（P0 生成式集合）
├── schemas/                # JSON Schema validation
│   ├── v1.json
│   ├── v2/
│   │   ├── provider.json
│   │   ├── provider-contract.json
│   │   ├── mcp.json
│   │   ├── computer-use.json
│   │   ├── multimodal.json
│   │   └── context-policy.json
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

1. **规范版本**（`v1/spec.yaml`）— 模式结构版本
2. **协议版本**（在清单中）— 清单使用的协议能力（`1.x` / `2.x`）
3. **发布版本**（`package.json`）— 规范包的 SemVer（当前：**v0.8.1**）

## V2 协议架构

协议在 **v0.8.1** 阶段完成了 V2 架构能力与执行治理门禁的一体化闭环。

### 三层金字塔

- **L1 核心协议** — 消息格式、标准错误码（E1001–E9999）、版本声明。所有供应商必须实现此层。
- **L2 能力扩展** — 流式、视觉、工具。每个扩展由特性标志控制；供应商按能力选择加入。
- **L3 环境配置** — API 密钥、端点、重试策略。环境特定配置，可在不改变供应商逻辑的情况下覆盖。

### 同心圆清单模型

- **环 1 核心骨架**（必需）— 有效清单的最小字段：endpoint、auth、parameter mappings
- **环 2 能力映射**（条件）— 流式配置、工具映射、视觉参数 —— 供应商支持时提供
- **环 3 高级扩展**（可选）— 自定义头部、限流头部、高级重试策略

### V2 生成式供应商集合（P0）

当前 P0 生成式供应商集合已在 V2 清单中对齐：

- OpenAI
- Anthropic
- Google Gemini
- DeepSeek
- Qwen
- Doubao

### 执行治理门禁（Release Governance）

`ai-protocol` 提供了可执行门禁脚本：

- `npm run drift:check`
- `npm run gate:manifest-consumption`
- `npm run gate:compliance-matrix`
- `npm run gate:fullchain`
- `npm run release:gate`

并支持 `--report-only` 模式，用于从“报告优先”逐步升级到“强阻断”治理。

### 标准错误码

V2 定义了 13 个标准化错误码（E1001–E9999），分为 5 类：客户端错误（E1xxx）、速率/配额（E2xxx）、服务端（E3xxx）、冲突/取消（E4xxx）和未知（E9999）。完整代码列表请参阅[规范](/protocol/spec/)。

### 跨运行时一致性

跨运行时一致性已扩展到 Rust / Python / TypeScript，重点覆盖 protocol loading、error classification、retry、message、stream、request 等合规维度。

## 下一步

- **[规范详情](/protocol/spec/)** — 核心规范详解
- **[供应商清单](/protocol/providers/)** — 清单工作原理
- **[模型注册表](/protocol/models/)** — 模型配置
- **[贡献供应商](/protocol/contributing/)** — 添加新供应商
