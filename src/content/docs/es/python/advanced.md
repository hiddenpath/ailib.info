---
title: Características avanzadas (Python)
description: Telemetría, enrutamiento de modelos, embeddings, caché, plugins y salida estructurada en ai-lib-python v0.6.0.
---

# Características avanzadas

## Extras de capacidades

Instale características opcionales mediante extras pip (v0.6.0+):

| Extra | Propósito |
|-------|-----------|
| `vision` | Procesamiento de imágenes (Pillow) |
| `audio` | Procesamiento de audio (soundfile) |
| `embeddings` | Generación de embeddings |
| `structured` | Salida estructurada / modo JSON |
| `batch` | Procesamiento por lotes |
| `agentic` | Soporte para flujos de trabajo de agentes |
| `telemetry` | Integración OpenTelemetry |
| `tokenizer` | Conteo de tokens (tiktoken) |
| `full` | Todas las características + watchdog + keyring |

```bash
pip install ai-lib-python[full]   # All features
pip install ai-lib-python[vision,embeddings]   # Selected extras
```

## Códigos de error V2

El tipo `StandardErrorCode` en `errors/standard_codes.py` proporciona clasificación de errores alineada con el protocolo:

- **13 códigos dataclass congelados** — Rango E1001–E9999
- **`from_http_status(status_code)`** — Mapear códigos de estado HTTP a códigos estándar
- **`from_name(name)`** — Buscar código por nombre de cadena
- **Canalización de clasificación** — Use las propiedades `retryable` y `fallbackable` para decisiones de resiliencia (reintentos, cadenas de fallback)

```python
from ai_lib_python.errors.standard_codes import StandardErrorCode

code = StandardErrorCode.from_http_status(429)
print(code.retryable)   # True
print(code.fallbackable)  # True
```

## Telemetría para producción

### Métricas (Prometheus)

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

### Trazado distribuido (OpenTelemetry)

```python
from ai_lib_python.telemetry import Tracer

tracer = Tracer(service_name="my-app")

# Traces propagate through the entire request lifecycle
client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .tracer(tracer) \
    .build()
```

### Monitoreo de salud

```python
from ai_lib_python.telemetry import HealthChecker

health = HealthChecker()
status = await health.check()
print(f"Healthy: {status.is_healthy}")
```

## Enrutamiento de modelos

Selección inteligente de modelos entre múltiples proveedores:

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

### Catálogos preconfigurados

```python
from ai_lib_python.routing import create_openai_models, create_anthropic_models

openai_models = create_openai_models()
anthropic_models = create_anthropic_models()
```

### Estrategias de selección

| Strategy | Description |
|----------|-------------|
| `round_robin` | Rota entre modelos |
| `weighted` | Selección basada en probabilidad |
| `cost_based` | Prefiere modelos más económicos |
| `quality_based` | Prefiere modelos de mayor calidad |
| `latency_based` | Prefiere modelos más rápidos |

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

## Caché de respuestas

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

## Conteo de tokens

```python
from ai_lib_python.tokens import TokenCounter

counter = TokenCounter.for_model("gpt-4o")
count = counter.count("Hello, how are you?")

# Cost estimation
from ai_lib_python.tokens import CostEstimator
estimator = CostEstimator.for_model("openai/gpt-4o")
cost = estimator.estimate(prompt_tokens=100, completion_tokens=50)
```

## Procesamiento por lotes

```python
from ai_lib_python.batch import BatchCollector, BatchExecutor

collector = BatchCollector()
collector.add(client.chat().user("Question 1"))
collector.add(client.chat().user("Question 2"))
collector.add(client.chat().user("Question 3"))

executor = BatchExecutor(concurrency=5, timeout=30)
results = await executor.execute(collector)
```

## Sistema de plugins

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

## Salida estructurada

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
