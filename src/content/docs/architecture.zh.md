---
title: 架构
group: 概述
order: 40
description: Rust SDK模块的分层设计。
---

# 架构

ai-lib遵循分层架构，分离关注点并支持可扩展性。这种设计允许轻松的提供商集成、可靠性功能和自定义传输实现。

## 高级架构

```
┌─────────────────────────────────────────────────────────────┐
│                    你的应用程序                             │
└───────────────▲─────────────────────────▲───────────────────┘
                │                         │
        高级API                    高级控制
                │                         │
        AiClient / Builder   ←  模型管理 / 指标 / 批处理 / 工具
                │
        ┌────────── 统一抽象层 ────────────┐
        │  提供商适配器（混合：配置+独立）  │
        └──────┬────────────┬────────────┬────────────────┘
               │            │            │
        OpenAI / Groq   Gemini / Mistral  Ollama / 区域 / 其他
               │
        传输（HTTP + 流式 + 重试 + 代理 + 超时）
               │
        通用类型（请求 / 消息 / 内容 / 工具 / 错误）
```

## 模块结构

| 层级 | 模块 | 职责 |
|------|------|------|
| **公共门面** | `AiClient`, `AiClientBuilder`, `Provider` | 入口点和配置 |
| **领域类型** | `types::request`, `types::response`, `types::common` | 消息、角色、内容枚举 |
| **API特征** | `api::chat` | 聊天抽象+流式块类型 |
| **提供商适配器** | `provider::*` | 提供商特定实现 |
| **模型管理** | `provider::models`, `provider::configs` | 能力元数据、选择策略 |
| **可靠性** | `circuit_breaker`, `rate_limiter`, `error_handling` | 重试、回退、熔断器、速率限制 |
| **传输** | `transport::*` | HTTP执行、代理、抽象 |
| **指标** | `metrics` | 可扩展的仪表化 |
| **工具** | `utils::file` | 多模态内容的文件助手 |

## 核心组件

### 1. AiClient & Builder

所有AI操作的主要入口点：

```rust
use ai_lib::{AiClient, Provider, ConnectionOptions};

// 简单使用
let client = AiClient::new(Provider::Groq)?;

// 高级配置
let client = AiClient::with_options(
    Provider::OpenAI,
    ConnectionOptions {
        proxy: Some("http://proxy:8080".into()),
        timeout: Some(Duration::from_secs(30)),
        ..Default::default()
    }
)?;
```

### 2. 提供商适配器

两种类型的提供商适配器：

**配置驱动提供商**（Groq、Anthropic等）：
- 使用统一配置系统
- 自动API密钥检测
- 一致的错误处理

**独立适配器**（OpenAI、Gemini等）：
- 自定义集成逻辑
- 提供商特定优化
- 高级功能支持

### 3. 传输层

具有内置功能的可插拔HTTP传输：

```rust
use ai_lib::transport::{HttpTransport, DynHttpTransport};

// 内置传输，支持重试和代理
let transport = HttpTransport::new()?;

// 自定义传输实现
struct CustomTransport;
impl DynHttpTransport for CustomTransport {
    // 自定义实现
}
```

### 4. 可靠性功能

内置的可靠性原语：

- **熔断器**：自动故障检测
- **速率限制**：令牌桶算法
- **重试逻辑**：带抖动的指数退避
- **错误分类**：可重试vs永久错误

### 5. 模型管理

高级模型选择和负载均衡：

```rust
use ai_lib::{ModelArray, LoadBalancingStrategy, ModelSelectionStrategy};

let array = ModelArray::new("production")
    .with_strategy(LoadBalancingStrategy::HealthBased)
    .add_endpoint(ModelEndpoint {
        name: "groq-1".into(),
        url: "https://api.groq.com".into(),
        weight: 1.0,
        healthy: true,
    });
```

## 数据流

### 基本聊天请求

1. **请求创建**：带有消息和选项的`ChatCompletionRequest`
2. **提供商选择**：基于`Provider`枚举选择适配器
3. **请求转换**：转换为提供商特定格式
4. **传输执行**：使用重试逻辑发送HTTP请求
5. **响应解析**：将提供商响应解析为统一格式
6. **错误处理**：适当分类和处理错误

### 流式请求

1. **流初始化**：创建流式连接
2. **块处理**：解析到达的SSE块
3. **增量聚合**：将增量组合为完整响应
4. **错误恢复**：优雅处理流中断

### 函数调用

1. **工具定义**：使用JSON模式定义工具
2. **请求增强**：向聊天请求添加工具
3. **响应分析**：检测函数调用意图
4. **工具执行**：执行外部函数
5. **结果集成**：将结果反馈给模型

## 扩展点

### 自定义传输

实现`DynHttpTransport`进行自定义HTTP处理：

```rust
use ai_lib::transport::DynHttpTransport;

struct CustomTransport;

#[async_trait]
impl DynHttpTransport for CustomTransport {
    async fn post(&self, url: &str, body: &[u8]) -> Result<Vec<u8>, TransportError> {
        // 自定义HTTP实现
    }
}
```

### 自定义指标

实现`Metrics`特征进行可观测性：

```rust
use ai_lib::metrics::{Metrics, Timer};

struct PrometheusMetrics;

#[async_trait]
impl Metrics for PrometheusMetrics {
    async fn incr_counter(&self, name: &str, value: u64) {
        // Prometheus计数器实现
    }
    
    async fn start_timer(&self, name: &str) -> Option<Box<dyn Timer + Send>> {
        // Prometheus计时器实现
    }
}
```

### 自定义模型管理器

实现自定义模型选择策略：

```rust
use ai_lib::provider::models::{ModelSelectionStrategy, ModelInfo};

struct CustomStrategy;

impl ModelSelectionStrategy for CustomStrategy {
    fn select_model(&self, models: &[ModelInfo]) -> Option<&ModelInfo> {
        // 自定义选择逻辑
    }
}
```

## 设计原则

1. **统一接口**：所有提供商使用相同API
2. **渐进复杂性**：从简单开始，根据需要添加功能
3. **可扩展性**：可插拔的传输、指标和策略
4. **可靠性**：内置重试、熔断器和错误处理
5. **性能**：最小开销，高效资源使用
6. **类型安全**：整个API的强类型

## 未来增强

- **缓存层**：请求/响应缓存
- **WebSocket支持**：原生WebSocket流式处理
- **GraphQL接口**：GraphQL API表面
- **插件系统**：动态插件加载
- **配置热重载**：运行时配置更新

## 下一步

- 探索[提供商详情](/docs/providers)了解具体实现
- 学习[可靠性功能](/docs/reliability-overview)进行生产使用
- 查看[高级示例](/docs/advanced-examples)了解复杂模式
