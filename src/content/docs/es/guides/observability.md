---
title: Observabilidad
description: Monitoreo, métricas, registro y trazado con los tiempos de ejecución de AI-Lib.
---

# Observabilidad

Ambos tiempos de ejecución proporcionan características de observabilidad para despliegues en producción.

## Rust: Registro estructurado

ai-lib-rust utiliza el ecosistema `tracing`:

```rust
use tracing_subscriber;

// Enable logging
tracing_subscriber::init();

// All AI-Lib operations emit structured log events
let client = AiClient::new("openai/gpt-4o").await?;
```

Niveles de registro:
- `INFO` — Resúmenes de solicitud/respuesta
- `DEBUG` — Carga de protocolo, etapas de la canalización
- `TRACE` — Frames individuales, coincidencias JSONPath

## Rust: Estadísticas de llamadas

Cada solicitud devuelve estadísticas de uso:

```rust
let (response, stats) = client.chat()
    .user("Hello")
    .execute_with_stats()
    .await?;

println!("Model: {}", stats.model);
println!("Provider: {}", stats.provider);
println!("Prompt tokens: {}", stats.prompt_tokens);
println!("Completion tokens: {}", stats.completion_tokens);
println!("Total tokens: {}", stats.total_tokens);
println!("Latency: {}ms", stats.latency_ms);
```

## Python: Estadísticas de llamadas

```python
response, stats = await client.chat() \
    .user("Hello") \
    .execute_with_stats()

print(f"Tokens: {stats.total_tokens}")
print(f"Latency: {stats.latency_ms}ms")
```

## TypeScript: Estadísticas de llamadas

```typescript
const { response, stats } = await client
  .chat()
  .user('Hello')
  .executeWithStats();

console.log(`Model: ${stats.model}`);
console.log(`Provider: ${stats.provider}`);
console.log(`Prompt tokens: ${stats.promptTokens}`);
console.log(`Completion tokens: ${stats.completionTokens}`);
console.log(`Total tokens: ${stats.totalTokens}`);
console.log(`Latency: ${stats.latencyMs}ms`);
```

## Python: Métricas (Prometheus)

```python
from ai_lib_python.telemetry import MetricsCollector

metrics = MetricsCollector()

client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .metrics(metrics) \
    .build()

# After some requests...
prometheus_text = metrics.export_prometheus()
```

## TypeScript: Métricas (Prometheus)

```typescript
import { MetricsCollector } from '@hiddenpath/ai-lib-ts/telemetry';

const metrics = new MetricsCollector();

const client = await AiClient.builder()
  .model('openai/gpt-4o')
  .metrics(metrics)
  .build();

// After some requests...
const prometheusText = metrics.exportPrometheus();
```

Métricas rastreadas:
- `ai_lib_requests_total` — Conteo de solicitudes por modelo/proveedor
- `ai_lib_request_duration_seconds` — Histograma de latencia
- `ai_lib_tokens_total` — Uso de tokens por tipo
- `ai_lib_errors_total` — Conteo de errores por tipo

## Python: Trazado distribuido (OpenTelemetry)

```python
from ai_lib_python.telemetry import Tracer

tracer = Tracer(
    service_name="my-app",
    endpoint="http://jaeger:4317",
)

client = await AiClient.builder() \
    .model("openai/gpt-4o") \
    .tracer(tracer) \
    .build()
```

## TypeScript: Trazado distribuido (OpenTelemetry)

```typescript
import { Tracer } from '@hiddenpath/ai-lib-ts/telemetry';

const tracer = new Tracer({
  serviceName: 'my-app',
  endpoint: 'http://jaeger:4317',
});

const client = await AiClient.builder()
  .model('openai/gpt-4o')
  .tracer(tracer)
  .build();
```

Los trazados incluyen spans para:
- Carga de protocolo
- Compilación de solicitudes
- Transporte HTTP
- Procesamiento de la canalización
- Mapeo de eventos

## Python: Monitoreo de salud

```python
from ai_lib_python.telemetry import HealthChecker

health = HealthChecker()
status = await health.check()

print(f"Healthy: {status.is_healthy}")
print(f"Details: {status.details}")
```

## TypeScript: Monitoreo de salud

```typescript
import { HealthChecker } from '@hiddenpath/ai-lib-ts/telemetry';

const health = new HealthChecker();
const status = await health.check();

console.log(`Healthy: ${status.isHealthy}`);
console.log(`Details: ${status.details}`);
```

## Python: Retroalimentación del usuario

Recolecte retroalimentación sobre las respuestas de IA:

```python
from ai_lib_python.telemetry import FeedbackCollector

feedback = FeedbackCollector()

# After getting a response
feedback.record(
    request_id=stats.request_id,
    rating=5,
    comment="Helpful response",
)
```

## TypeScript: Retroalimentación del usuario

```typescript
import { FeedbackCollector } from '@hiddenpath/ai-lib-ts/telemetry';

const feedback = new FeedbackCollector();

// After getting a response
feedback.record({
  requestId: stats.requestId,
  rating: 5,
  comment: 'Helpful response',
});
```

## Observabilidad de resiliencia

Monitoree el estado del circuit breaker y el limitador de velocidad:

```rust
// Rust
let state = client.circuit_state(); // Closed, Open, HalfOpen
let inflight = client.current_inflight();
```

## Python: Observabilidad de resiliencia

```python
# Python
signals = client.signals_snapshot()
print(f"Circuit: {signals.circuit_state}")
print(f"Inflight: {signals.current_inflight}")
```

```typescript
// TypeScript
const signals = client.signalsSnapshot();
console.log(`Circuit: ${signals.circuitState}`);
console.log(`Inflight: ${signals.currentInflight}`);
```
