---
title: 高级功能（Python）
description: ai-lib-python v0.6.0 中的 telemetry、模型路由、embeddings、缓存、插件与结构化输出。
---

# 高级功能

## Capability Extras

通过 pip extras 安装可选功能（v0.6.0+）：

| Extra | Purpose |
|-------|---------|
| `vision` | 图像处理（Pillow） |
| `audio` | 音频处理（soundfile） |
| `embeddings` | 生成 embedding |
| `structured` | 结构化输出 / JSON 模式 |
| `batch` | 批处理 |
| `agentic` | Agent 工作流支持 |
| `telemetry` | OpenTelemetry 集成 |
| `tokenizer` | Token 计数（tiktoken） |
| `full` | 所有功能 + watchdog + keyring |

```bash
pip install ai-lib-python[full]   # All features
pip install ai-lib-python[vision,embeddings]   # Selected extras
```

## V2 错误码

`errors/standard_codes.py` 中的 `StandardErrorCode` 类型提供协议一致的错误分类：

- **13 个 frozen dataclass 码** — E1001–E9999 范围
- **`from_http_status(status_code)`** — 将 HTTP 状态码映射到标准码
- **`from_name(name)`** — 按字符串名称查找码
- **分类流水线** — 使用 `retryable` 与 `fallbackable` 属性进行弹性决策（重试、回退链）

```python
from ai_lib_python.errors.standard_codes import StandardErrorCode

code = StandardErrorCode.from_http_status(429)
print(code.retryable)   # True
print(code.fallbackable)  # True
```

## 生产级 Telemetry

### 指标（Prometheus）

```python
from ai_lib_python.telemetry import MetricsCollector

metrics = MetricsCollector()

# Automatically tracks request counts, latency, token usage, errors
client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .metrics(metrics) \
    .build()

# Export to Prometheus
metrics.export_prometheus()  # Returns Prometheus text format
```

### 分布式追踪（OpenTelemetry）

```python
from ai_lib_python.telemetry import Tracer

tracer = Tracer(service_name="my-app")

# Traces propagate through the entire request lifecycle
client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .tracer(tracer) \
    .build()
```

### 健康监控

```python
from ai_lib_python.telemetry import HealthChecker

health = HealthChecker()
status = await health.check()
print(f"Healthy: {status.is_healthy}")
```

## 模型路由

跨多个提供商的智能模型选择：

```python
from ai_lib_python.routing import ModelManager, ModelInfo

manager = ModelManager()

# Register models
manager.register(ModelInfo(
    model_id="openai/gpt-4o",
    weight=0.7,
    capabilities=["chat", "tools", "vision"],
))
manager.register(ModelInfo(
    model_id="anthropic/claude-3-5-sonnet",
    weight=0.3,
    capabilities=["chat", "tools", "reasoning"],
))

# Select based on strategy
model = manager.select(strategy="weighted")
```

### 预配置目录

```python
from ai_lib_python.routing import create_openai_models, create_anthropic_models

openai_models = create_openai_models()
anthropic_models = create_anthropic_models()
```

### 选择策略

| Strategy | Description |
|----------|-------------|
| `round_robin` | 轮询模型 |
| `weighted` | 基于概率选择 |
| `cost_based` | 优先更便宜模型 |
| `quality_based` | 优先更高质量模型 |
| `latency_based` | 优先更快模型 |

## Embeddings

```python
from ai_lib_python.embeddings import EmbeddingClient

client = EmbeddingClient(model="openai/text-embedding-3-small")

embeddings = await client.embed([
    "Python programming",
    "Machine learning",
    "Cooking recipes",
])

from ai_lib_python.embeddings.vectors import cosine_similarity
sim = cosine_similarity(embeddings[0], embeddings[1])
print(f"Similarity: {sim:.3f}")
```

## 响应缓存

```python
from ai_lib_python.cache import CacheManager, MemoryCache, DiskCache

# In-memory cache
cache = CacheManager(backend=MemoryCache(), ttl=3600)

# Disk cache
cache = CacheManager(backend=DiskCache("./cache"), ttl=86400)

client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .cache(cache) \
    .build()
```

## Token 计数

```python
from ai_lib_python.tokens import TokenCounter

counter = TokenCounter.for_model("gpt-4o")
count = counter.count("Hello, how are you?")

# Cost estimation
from ai_lib_python.tokens import CostEstimator
estimator = CostEstimator.for_model("openai/gpt-4o")
cost = estimator.estimate(prompt_tokens=100, completion_tokens=50)
```

## 批处理

```python
from ai_lib_python.batch import BatchCollector, BatchExecutor

collector = BatchCollector()
collector.add(client.chat().user("Question 1"))
collector.add(client.chat().user("Question 2"))
collector.add(client.chat().user("Question 3"))

executor = BatchExecutor(concurrency=5, timeout=30)
results = await executor.execute(collector)
```

## 插件系统

```python
from ai_lib_python.plugins import Plugin, PluginRegistry

class LoggingPlugin(Plugin):
    def name(self) -> str:
        return "logging"

    async def on_request(self, request):
        print(f"→ {request.model}")

    async def on_response(self, response):
        print(f"← {response.usage.total_tokens} tokens")

registry = PluginRegistry()
registry.register(LoggingPlugin())
```

## 结构化输出

```python
from ai_lib_python.structured import JsonMode, SchemaGenerator

# JSON mode
response = await client.chat() \
    .user("List 3 countries as JSON") \
    .response_format(JsonMode()) \
    .execute()

# With Pydantic schema
from pydantic import BaseModel

class Country(BaseModel):
    name: str
    capital: str

schema = SchemaGenerator.from_model(Country)
```

## Guardrails

```python
from ai_lib_python.guardrails import ContentFilter, PiiDetector

filter = ContentFilter(blocked_keywords=["unsafe"])
pii = PiiDetector()
```
