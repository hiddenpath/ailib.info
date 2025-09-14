---
title: 特性开关（Features）与可选模块
group: 概述
order: 15
status: stable
---

# 特性开关（Features）与可选模块

本文说明如何在 Cargo 项目中按需引入 `ai-lib` 的可选特性，并给出不同场景的推荐组合。

## 基础依赖

```toml
[dependencies]
ai-lib = "0.3.3"
tokio = { version = "1", features = ["full"] }
```

## 启用特性

`ai-lib` 默认保持精简。根据需要开启特性：

```toml
[dependencies]
ai-lib = { version = "0.3.3", features = ["resilience", "streaming"] }
```

### 友好别名（提高易用性）

- resilience → 启用 `interceptors`（重试/限流/熔断等拦截链）
- streaming → 启用 `unified_sse`（统一流式解析）
- transport → 启用 `unified_transport`（共享 reqwest 客户端工厂）
- hot_reload → 启用 `config_hot_reload`（配置提供者/监听接口）
- all → 打开大多数 OSS 特性：`interceptors`、`unified_transport`、`unified_sse`、`cost_metrics`、`routing_mvp`、`observability`、`config_hot_reload`

这些别名只是聚合启用粒度特性，本身不增加额外代码。

## 推荐组合

- 最小化应用：不开启（按需增加）
- 生产应用：`resilience`、`transport`、`streaming`
- 运维增强：`resilience`、`transport`、`streaming`、`observability`
- 动态配置：加上 `hot_reload`

## 示例：生产简化配置

```toml
[dependencies]
ai-lib = { version = "0.3.3", features = [
  "resilience",
  "transport",
  "streaming"
] }
```

## 导入风格

推荐使用根级导入，提升开发者体验：

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Role, Content};
use ai_lib::{Tool, FunctionCallPolicy};
```

## 说明

- 尽量保持依赖面最小：只启用你用到的特性。
- 特性前向兼容；我们避免破坏性重命名。
- 参考：[快速开始](/docs/getting-started)、[聊天与流式处理](/docs/chat)。


