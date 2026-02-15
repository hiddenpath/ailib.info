---
title: 规范详情
description: 深入 AI-Protocol 核心规范 —— 标准参数、事件、错误类型与重试策略。
---

# 核心规范

核心规范（`v1/spec.yaml`）定义了所有供应商清单和运行时共享的标准词汇。

## 标准参数

以下参数在所有供应商中含义一致：

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `temperature` | float | 随机性控制（0.0 – 2.0） |
| `max_tokens` | integer | 最大响应 token 数 |
| `top_p` | float | 核采样阈值 |
| `stream` | boolean | 启用流式响应 |
| `stop` | string[] | 停止序列 |
| `tools` | object[] | 工具/函数定义 |
| `tool_choice` | string/object | 工具选择模式 |
| `response_format` | object | 结构化输出格式 |

供应商清单将这些标准名称映射到供应商特定的参数名。例如，OpenAI 使用 `max_completion_tokens`，而 Anthropic 使用 `max_tokens`。

## 流式事件

规范定义了运行时发出的统一流式事件类型：

| 事件 | 描述 |
|-------|-------------|
| `PartialContentDelta` | 文本内容片段 |
| `ThinkingDelta` | 推理/思考块（扩展思考模型） |
| `ToolCallStarted` | 函数/工具调用开始 |
| `PartialToolCall` | 工具调用参数流式传输 |
| `ToolCallEnded` | 工具调用完成 |
| `StreamEnd` | 响应流结束 |
| `StreamError` | 流级错误 |
| `Metadata` | 使用统计、模型信息 |

供应商清单声明基于 JSONPath 的规则，将供应商特定事件映射到这些标准类型。

## 错误类型（V2 标准码）

V2 定义了 13 个标准化错误码。供应商特定错误会映射到这些代码，以便在各运行时中一致处理：

| 代码 | 名称 | 类别 | 可重试 | 可回退 |
|------|------|----------|-----------|--------------|
| E1001 | `invalid_request` | Client | No | No |
| E1002 | `authentication` | Client | No | No |
| E1003 | `permission_denied` | Client | No | No |
| E1004 | `not_found` | Client | No | No |
| E1005 | `request_too_large` | Client | No | Yes |
| E2001 | `rate_limited` | Rate | Yes | Yes |
| E2002 | `quota_exhausted` | Quota | No | Yes |
| E3001 | `server_error` | Server | Yes | Yes |
| E3002 | `overloaded` | Server | Yes | Yes |
| E3003 | `timeout` | Server | Yes | Yes |
| E4001 | `conflict` | Conflict | No | No |
| E4002 | `cancelled` | Conflict | No | No |
| E9999 | `unknown` | Unknown | No | Yes |

- **可重试** — 运行时可为临时故障重试请求（带退避）
- **可回退** — 运行时可在回退链中尝试备选供应商或模型

## 重试策略

规范定义标准重试策略：

```yaml
retry_policy:
  strategy: "exponential_backoff"
  max_retries: 3
  initial_delay_ms: 1000
  max_delay_ms: 30000
  backoff_multiplier: 2.0
  retryable_errors:
    - "rate_limited"
    - "overloaded"
    - "server_error"
    - "timeout"
```

## 终止原因

响应完成时的标准化结束原因：

| 原因 | 描述 |
|--------|-------------|
| `end_turn` | 正常结束 |
| `max_tokens` | 达到 token 限制 |
| `tool_use` | 模型希望调用工具 |
| `stop_sequence` | 遇到停止序列 |
| `content_filter` | 被内容策略过滤 |

## API 系列

供应商按 API 系列分类，以避免请求/响应格式混淆：

- `openai` — OpenAI 兼容 API（也用于 Groq、Together、DeepSeek 等）
- `anthropic` — Anthropic Messages API
- `gemini` — Google Gemini API
- `custom` — 供应商特定格式

## 下一步

- **[供应商清单](/protocol/providers/)** — 供应商配置工作原理
- **[模型注册表](/protocol/models/)** — 模型配置详情
