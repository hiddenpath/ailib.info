---
title: 贡献供应商
description: 向 AI-Protocol 规范添加新 AI 供应商的分步指南。
---

# 贡献供应商

向 AI-Protocol 添加新的 AI 供应商后，它将立即在所有运行时（Rust、Python 以及任何未来实现）中可用。

## 步骤

> **V2-alpha 格式**：协议 v0.5.0 版本引入了采用 Ring 1/2/3 清单结构的 v2-alpha 供应商格式。新供应商可选择采用 v2-alpha，以获得标准化错误码、特性标志和能力扩展。V2 架构详情请参阅[协议概览](/protocol/overview/)。

### 1. 研究供应商 API

记录以下有关供应商的信息：

- 基础 URL 和聊天端点路径
- 认证方式（Bearer token、API key 头部等）
- 请求参数格式
- 流式响应格式（SSE、NDJSON、自定义）
- 错误响应结构
- 可用模型及其能力

### 2. 创建供应商清单

创建 `v1/providers/<provider-id>.yaml`：

```yaml
id: <provider-id>
name: "<Provider Name>"
protocol_version: "1.5"

endpoint:
  base_url: "https://api.example.com/v1"
  chat_path: "/chat/completions"

auth:
  type: bearer
  token_env: "<PROVIDER_ID>_API_KEY"

parameter_mappings:
  temperature: "temperature"
  max_tokens: "max_tokens"
  stream: "stream"
  tools: "tools"

streaming:
  decoder:
    format: "sse"
    done_signal: "[DONE]"
  event_map:
    - match: "$.choices[0].delta.content"
      emit: "PartialContentDelta"
      extract:
        content: "$.choices[0].delta.content"

error_classification:
  by_http_status:
    "401": "authentication"
    "429": "rate_limited"
    "500": "server_error"

capabilities:
  streaming: true
  tools: true
  vision: false
```

### 3. 添加模型

创建或更新 `v1/models/<family>.yaml`：

```yaml
models:
  example-model:
    provider: <provider-id>
    model_id: "example-model-v1"
    context_window: 128000
    capabilities: [chat, streaming, tools]
    pricing:
      input_per_token: 0.000001
      output_per_token: 0.000002
```

### 4. 验证

```bash
npm run validate
```

这将对照 JSON Schema 检查您的清单并报告任何错误。

### 5. 构建

```bash
npm run build
```

这将把 YAML 编译为 `dist/` 目录中的 JSON。

### 6. 提交 Pull Request

- Fork 仓库
- 创建分支
- 添加供应商清单和模型条目
- 确保验证通过
- 提交附带供应商文档的 PR

## 验证规则

JSON Schema 强制要求：

- 必填字段（`id`、`endpoint`、`auth`、`parameter_mappings`）
- URL、环境变量名的有效格式
- 流式配置的正确结构
- 有效的错误分类类型
- 能力标志为布尔值

## 提示

- 若供应商遵循 OpenAI API 结构，请使用 **OpenAI 兼容格式** —— 许多供应商如此（Groq、Together AI、DeepSeek）
- 仔细测试流式配置 —— 这是大多数供应商差异所在
- 准确设置 `capabilities` 标志 —— 运行时用于预检验证
