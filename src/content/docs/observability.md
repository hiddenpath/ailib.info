---
title: Observability
group: Guide
order: 80
status: planned
---

# Observability (Planned)

Target metrics: request_count, latency (histogram p50/p95/p99), token_usage, error_count{class}, provider_success_rate.

`metrics` module exposes traits (`Metrics`, `Timer`). A noop implementation ships by default; plug in your collector by implementing these traits.

Tracing (planned): OpenTelemetry spans around: request build -> transport -> parse -> reliability decisions.

Logging: structured JSON (add correlation / request id). Integrate with `tracing` crate when instrumentation lands.
