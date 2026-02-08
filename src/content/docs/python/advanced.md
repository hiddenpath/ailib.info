---
title: Advanced Features (Python)
description: Telemetry, model routing, embeddings, caching, plugins, and structured output in ai-lib-python.
---

# Advanced Features

## Production Telemetry

### Metrics (Prometheus)

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

### Distributed Tracing (OpenTelemetry)

```python
from ai_lib_python.telemetry import Tracer

tracer = Tracer(service_name="my-app")

# Traces propagate through the entire request lifecycle
client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .tracer(tracer) \
    .build()
```

### Health Monitoring

```python
from ai_lib_python.telemetry import HealthChecker

health = HealthChecker()
status = await health.check()
print(f"Healthy: {status.is_healthy}")
```

## Model Routing

Intelligent model selection across multiple providers:

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

### Pre-configured Catalogs

```python
from ai_lib_python.routing import create_openai_models, create_anthropic_models

openai_models = create_openai_models()
anthropic_models = create_anthropic_models()
```

### Selection Strategies

| Strategy | Description |
|----------|-------------|
| `round_robin` | Rotates through models |
| `weighted` | Probability-based selection |
| `cost_based` | Prefers cheaper models |
| `quality_based` | Prefers higher-quality models |
| `latency_based` | Prefers faster models |

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

## Response Caching

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

## Token Counting

```python
from ai_lib_python.tokens import TokenCounter

counter = TokenCounter.for_model("gpt-4o")
count = counter.count("Hello, how are you?")

# Cost estimation
from ai_lib_python.tokens import CostEstimator
estimator = CostEstimator.for_model("openai/gpt-4o")
cost = estimator.estimate(prompt_tokens=100, completion_tokens=50)
```

## Batch Processing

```python
from ai_lib_python.batch import BatchCollector, BatchExecutor

collector = BatchCollector()
collector.add(client.chat().user("Question 1"))
collector.add(client.chat().user("Question 2"))
collector.add(client.chat().user("Question 3"))

executor = BatchExecutor(concurrency=5, timeout=30)
results = await executor.execute(collector)
```

## Plugin System

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

## Structured Output

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
