---
title: Resiliencia (Python)
description: Patrones de fiabilidad en producción en ai-lib-python v0.7.0 — ResilientExecutor, cortacircuitos, limitador de tasa, fallback.
---

# Patrones de resiliencia

ai-lib-python (v0.7.0+) incluye un sistema integral de resiliencia centrado en `ResilientExecutor`. Las decisiones de reintento y fallback utilizan ahora códigos de error estándar V2 mediante las propiedades `retryable` y `fallbackable` en `StandardErrorCode`, garantizando un comportamiento alineado con el protocolo.

## ResilientExecutor

Combina todos los patrones de fiabilidad en un único ejecutor:

```python
from ai_lib_python.resilience import (
    ResilientConfig, RetryConfig, RateLimiterConfig,
    CircuitBreakerConfig, BackpressureConfig
)

config = ResilientConfig(
    retry=RetryConfig(
        max_retries=3,
        initial_delay=1.0,
        max_delay=30.0,
        backoff_multiplier=2.0,
    ),
    rate_limiter=RateLimiterConfig(
        requests_per_second=10,
    ),
    circuit_breaker=CircuitBreakerConfig(
        failure_threshold=5,
        cooldown_seconds=30,
    ),
    backpressure=BackpressureConfig(
        max_inflight=50,
    ),
)

client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .resilience(config) \
    .build()
```

## Patrones individuales

### Cortacircuitos (Circuit Breaker)

```python
from ai_lib_python.resilience import CircuitBreaker

breaker = CircuitBreaker(
    failure_threshold=5,
    cooldown_seconds=30,
)

# Check state
print(breaker.state)  # "closed", "open", "half_open"
```

### Limitador de tasa

Algoritmo de cubo de tokens:

```python
from ai_lib_python.resilience import RateLimiter

limiter = RateLimiter(
    requests_per_second=10,
    burst_size=20,
)
```

### Contrapresión (Backpressure)

Limitación de concurrencia:

```python
from ai_lib_python.resilience import Backpressure

bp = Backpressure(max_inflight=50)
```

### Cadena de fallback

Conmutación por error multirrecurso:

```python
from ai_lib_python.resilience import FallbackChain

chain = FallbackChain([
    "openai/gpt-4o",
    "anthropic/claude-3-5-sonnet",
    "deepseek/deepseek-chat",
])
```

## PreflightChecker

Control de acceso unificado antes de la ejecución de la solicitud:

```python
from ai_lib_python.resilience import PreflightChecker

checker = PreflightChecker()
# Checks circuit state, rate limits, inflight count
# before allowing a request through
```

## SignalsSnapshot

Estado agregado del tiempo de ejecución:

```python
signals = client.signals_snapshot()
print(f"Circuit: {signals.circuit_state}")
print(f"Inflight: {signals.current_inflight}")
print(f"Rate remaining: {signals.rate_remaining}")
```

## Variables de entorno

| Variable | Propósito |
|----------|---------|
| `AI_LIB_RPS` | Límite de tasa (solicitudes por segundo) |
| `AI_LIB_BREAKER_FAILURE_THRESHOLD` | Umbral del cortacircuitos |
| `AI_LIB_BREAKER_COOLDOWN_SECS` | Período de espera |
| `AI_LIB_MAX_INFLIGHT` | Máximo de solicitudes concurrentes |

## Próximos pasos

- **[Funciones avanzadas](/python/advanced/)** — Telemetría, enrutamiento, plugins
- **[API AiClient](/python/client/)** — Uso del cliente
