---
title: 模型注册表
description: AI-Protocol 模型注册表如何将模型标识符映射到包含能力与定价的供应商配置。
---

# 模型注册表

模型注册表（`v1/models/*.yaml`）将模型标识符映射到供应商配置，记录每个模型的能力、上下文窗口和定价。

## 模型文件结构

模型按系列组织（GPT、Claude、Gemini 等）：

```
v1/models/
├── gpt.yaml          # OpenAI GPT models
├── claude.yaml        # Anthropic Claude models
├── gemini.yaml        # Google Gemini models
├── deepseek.yaml      # DeepSeek models
├── qwen.yaml          # Alibaba Qwen models
├── mistral.yaml       # Mistral models
├── llama.yaml         # Meta Llama models
└── ...                # 28+ model files
```

## 模型定义

每个模型条目包含：

```yaml
models:
  gpt-4o:
    provider: openai
    model_id: "gpt-4o"
    context_window: 128000
    max_output_tokens: 16384
    capabilities:
      - chat
      - streaming
      - tools
      - vision
      - json_mode
    pricing:
      input_per_token: 0.0000025
      output_per_token: 0.00001
    release_date: "2024-05-13"
```

## 模型标识符

运行时使用 `provider/model` 格式标识模型：

```
anthropic/claude-3-5-sonnet
openai/gpt-4o
deepseek/deepseek-chat
gemini/gemini-2.0-flash
qwen/qwen-plus
```

运行时将其拆分为：
1. **Provider ID**（`anthropic`）→ 加载供应商清单
2. **Model name**（`claude-3-5-sonnet`）→ 在模型注册表中查找

## 能力

标准能力标志：

| 能力 | 描述 |
|-----------|-------------|
| `chat` | 基础聊天补全 |
| `streaming` | 流式响应 |
| `tools` | 函数/工具调用 |
| `vision` | 图像理解 |
| `audio` | 音频输入/输出 |
| `reasoning` | 扩展思考（CoT） |
| `agentic` | 多步代理工作流 |
| `json_mode` | 结构化 JSON 输出 |

## 定价

按 token 定价使运行时能够进行成本估算：

```yaml
pricing:
  input_per_token: 0.000003      # $3 per 1M input tokens
  output_per_token: 0.000015     # $15 per 1M output tokens
  cached_input_per_token: 0.0000003  # Cached prompt discount
```

Rust 和 Python 运行时均使用此数据进行 `CostEstimate` 计算。

## 验证

模型可包含生产部署的验证状态：

```yaml
verification:
  status: "verified"
  last_checked: "2025-01-15"
  verified_capabilities:
    - chat
    - streaming
    - tools
```

## 下一步

- **[贡献供应商](/protocol/contributing/)** — 添加新供应商和模型
- **[快速入门](/quickstart/)** — 使用运行时开始使用模型
