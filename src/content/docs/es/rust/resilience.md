---
title: Resiliencia (Rust)
description: Patrones de confiabilidad para producción en ai-lib-rust v0.8.0 — circuit breaker, limitador de velocidad, backpressure, reintentos.
---

# Patrones de resiliencia

ai-lib-rust (v0.8.0) incluye patrones de confiabilidad de nivel producción de serie. Las decisiones de reintento y fallback utilizan códigos de error estándar V2: las propiedades `retryable` y `fallbackable` en `StandardErrorCode` determinan si un error desencadena reintentos o fallback de modelo.

## Circuit Breaker

Previene fallos en cascada al detener las solicitudes a proveedores con fallos:

**Estados:**
- **Closed** — Operación normal, las solicitudes fluyen
- **Open** — Demasiados fallos, las solicitudes se rechazan inmediatamente
- **Half-Open** — Después del enfriamiento, permite una solicitud de prueba

**Configuración:**

```bash
export AI_LIB_BREAKER_FAILURE_THRESHOLD=5
export AI_LIB_BREAKER_COOLDOWN_SECS=30
```

El circuito se abre después de `FAILURE_THRESHOLD` fallos consecutivos y permanece abierto durante `COOLDOWN_SECS` antes de la prueba.

## Limitador de velocidad

El algoritmo de token bucket previene exceder los límites de velocidad del proveedor:

```bash
export AI_LIB_RPS=10    # Máximo de solicitudes por segundo
export AI_LIB_RPM=600   # Máximo de solicitudes por minuto
```

Las solicitudes que excedan el límite se encolan en lugar de rechazarse, proporcionando un rendimiento fluido.

## Backpressure

Limita las solicitudes concurrentes en curso con un semáforo:

```bash
export AI_LIB_MAX_INFLIGHT=50
```

Cuando se alcanza el límite, las nuevas solicitudes esperan hasta que se libere un espacio.

## Reintentos

Reintento con backoff exponencial impulsado por la política de reintento del manifiesto del protocolo:

```yaml
# In the provider manifest
retry_policy:
  strategy: "exponential_backoff"
  max_retries: 3
  initial_delay_ms: 1000
  max_delay_ms: 30000
  retryable_errors:
    - "rate_limited"
    - "overloaded"
    - "server_error"
```

Solo los errores clasificados como reintentables desencadenan reintentos. Los errores de autenticación, por ejemplo, fallan inmediatamente.

## Combinación de patrones

Todos los patrones de resiliencia funcionan juntos. Un flujo de solicitud típico:

1. **Backpressure** — Esperar un espacio si está al máximo de solicitudes en curso
2. **Circuit Breaker** — Rechazar inmediatamente si el circuito está abierto
3. **Limitador de velocidad** — Esperar un token si hay límite de velocidad
4. **Ejecutar** — Enviar la solicitud
5. **Reintentar** — Si es error reintentable, esperar y reintentar
6. **Actualizar** — Registrar éxito/fallo para el circuit breaker

## Observabilidad

Monitoree el estado de resiliencia en tiempo de ejecución:

```rust
// Check circuit breaker state
let state = client.circuit_state();
println!("Circuit: {:?}", state); // Closed, Open, HalfOpen

// Check current inflight count
let inflight = client.current_inflight();
```

## Próximos pasos

- **[Características avanzadas](/rust/advanced/)** — Embeddings, caché, plugins
- **[API AiClient](/rust/client/)** — Uso del cliente
