---
title: 熔断器
group: 可靠性
order: 60
status: partial
---

# 熔断器（部分实现）

在达到故障阈值后打开；半开状态允许有限的试验调用，然后完全关闭。当前范围可能较粗（提供商/模型级别）。

```rust
// let cb = CircuitBreaker::new().failures(5).window(Duration::from_secs(30)).cooldown(Duration::from_secs(10));
// let client = AiClientBuilder::new(Provider::OpenAI).circuit_breaker(cb).build()?;
```

计划中：错误加权和每个端点的更细粒度。

## 熔断器模式

熔断器是一种重要的可靠性模式，用于防止级联故障。当服务出现问题时，熔断器会"打开"并阻止进一步的请求，给服务时间恢复。

### 状态转换

熔断器有三种状态：

1. **关闭（Closed）**：正常状态，请求正常通过
2. **打开（Open）**：故障状态，请求被阻止
3. **半开（Half-Open）**：测试状态，允许有限数量的请求通过

### 基本配置

```rust
use ai_lib::circuit_breaker::{CircuitBreaker, CircuitBreakerConfig};

let config = CircuitBreakerConfig {
    failure_threshold: 5,           // 5次失败后打开
    success_threshold: 3,           // 3次成功后半开转关闭
    timeout: Duration::from_secs(30), // 30秒超时
    cooldown: Duration::from_secs(10), // 10秒冷却期
};

let circuit_breaker = CircuitBreaker::new(config);
```

### 使用示例

```rust
use ai_lib::{AiClient, Provider, ChatCompletionRequest, Message, Content};

async fn resilient_request(
    client: &AiClient,
    request: ChatCompletionRequest,
) -> Result<String, Box<dyn std::error::Error>> {
    // 检查熔断器状态
    if !circuit_breaker.can_execute() {
        return Err("Circuit breaker is open".into());
    }
    
    match client.chat_completion(request).await {
        Ok(response) => {
            circuit_breaker.record_success();
            Ok(response.first_text()?)
        }
        Err(error) => {
            circuit_breaker.record_failure();
            Err(error.into())
        }
    }
}
```

### 高级配置

```rust
use ai_lib::circuit_breaker::{CircuitBreaker, CircuitBreakerConfig, ErrorWeighting};

let config = CircuitBreakerConfig {
    failure_threshold: 10,
    success_threshold: 5,
    timeout: Duration::from_secs(60),
    cooldown: Duration::from_secs(30),
    error_weighting: Some(ErrorWeighting::new()
        .add_weight("rate_limit", 0.5)    // 速率限制错误权重较低
        .add_weight("timeout", 1.0)       // 超时错误权重正常
        .add_weight("server_error", 2.0)  // 服务器错误权重较高
    ),
};

let circuit_breaker = CircuitBreaker::new(config);
```

### 监控和指标

```rust
use ai_lib::circuit_breaker::CircuitBreaker;

impl CircuitBreaker {
    pub fn get_state(&self) -> CircuitState {
        // 返回当前状态
    }
    
    pub fn get_failure_count(&self) -> u32 {
        // 返回当前失败计数
    }
    
    pub fn get_success_count(&self) -> u32 {
        // 返回当前成功计数
    }
    
    pub fn get_last_failure_time(&self) -> Option<Instant> {
        // 返回最后失败时间
    }
}

// 使用指标记录熔断器状态
metrics.record_gauge("circuit_breaker_state", state as f64).await;
metrics.record_gauge("circuit_breaker_failures", failure_count as f64).await;
```

### 多级熔断器

```rust
use ai_lib::circuit_breaker::{CircuitBreaker, CircuitBreakerLevel};

// 提供商级别熔断器
let provider_cb = CircuitBreaker::new(CircuitBreakerConfig {
    level: CircuitBreakerLevel::Provider,
    failure_threshold: 10,
    // ...
});

// 模型级别熔断器
let model_cb = CircuitBreaker::new(CircuitBreakerConfig {
    level: CircuitBreakerLevel::Model,
    failure_threshold: 5,
    // ...
});

// 端点级别熔断器
let endpoint_cb = CircuitBreaker::new(CircuitBreakerConfig {
    level: CircuitBreakerLevel::Endpoint,
    failure_threshold: 3,
    // ...
});
```

### 自定义熔断器实现

```rust
use ai_lib::circuit_breaker::{CircuitBreaker, CircuitBreakerConfig};
use std::sync::Arc;
use tokio::sync::RwLock;

pub struct CustomCircuitBreaker {
    config: CircuitBreakerConfig,
    state: Arc<RwLock<CircuitState>>,
    failure_count: Arc<RwLock<u32>>,
    success_count: Arc<RwLock<u32>>,
    last_failure: Arc<RwLock<Option<Instant>>>,
}

impl CustomCircuitBreaker {
    pub fn new(config: CircuitBreakerConfig) -> Self {
        Self {
            config,
            state: Arc::new(RwLock::new(CircuitState::Closed)),
            failure_count: Arc::new(RwLock::new(0)),
            success_count: Arc::new(RwLock::new(0)),
            last_failure: Arc::new(RwLock::new(None)),
        }
    }
    
    pub async fn can_execute(&self) -> bool {
        let state = *self.state.read().await;
        match state {
            CircuitState::Closed => true,
            CircuitState::Open => {
                // 检查是否应该进入半开状态
                if let Some(last_failure) = *self.last_failure.read().await {
                    if last_failure.elapsed() >= self.config.cooldown {
                        *self.state.write().await = CircuitState::HalfOpen;
                        *self.success_count.write().await = 0;
                        true
                    } else {
                        false
                    }
                } else {
                    false
                }
            }
            CircuitState::HalfOpen => true,
        }
    }
    
    pub async fn record_success(&self) {
        let mut success_count = self.success_count.write().await;
        *success_count += 1;
        
        if *success_count >= self.config.success_threshold {
            *self.state.write().await = CircuitState::Closed;
            *self.failure_count.write().await = 0;
        }
    }
    
    pub async fn record_failure(&self) {
        let mut failure_count = self.failure_count.write().await;
        *failure_count += 1;
        
        if *failure_count >= self.config.failure_threshold {
            *self.state.write().await = CircuitState::Open;
            *self.last_failure.write().await = Some(Instant::now());
        }
    }
}
```

### 最佳实践

1. **合理设置阈值**：根据服务特性设置合适的失败阈值
2. **监控状态变化**：记录熔断器状态变化和指标
3. **错误分类**：对不同类型错误设置不同权重
4. **快速失败**：在熔断器打开时快速返回错误
5. **优雅降级**：提供备用方案或缓存响应

### 配置建议

```rust
// 生产环境配置
let production_config = CircuitBreakerConfig {
    failure_threshold: 10,           // 10次失败
    success_threshold: 5,            // 5次成功
    timeout: Duration::from_secs(30), // 30秒超时
    cooldown: Duration::from_secs(60), // 60秒冷却
    error_weighting: Some(ErrorWeighting::new()
        .add_weight("rate_limit", 0.3)
        .add_weight("timeout", 0.8)
        .add_weight("server_error", 1.5)
    ),
};

// 开发环境配置
let development_config = CircuitBreakerConfig {
    failure_threshold: 3,            // 3次失败
    success_threshold: 2,            // 2次成功
    timeout: Duration::from_secs(10), // 10秒超时
    cooldown: Duration::from_secs(5),  // 5秒冷却
    error_weighting: None,
};
```

## 下一步

- 学习[可靠性概述](/docs/reliability-overview)了解其他可靠性功能
- 查看[重试机制](/docs/reliability-retry)了解重试策略
- 探索[回退策略](/docs/reliability-fallback)了解故障转移
