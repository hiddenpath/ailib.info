---
title: Deployment & Security
group: Enterprise
order: 20
status: partial
---

# Deployment & Security

Stateless core: embed crate inside your async service and scale horizontally. Use environment isolation for provider keys.

## Security Practices

- Keys loaded at process start; never logged.
- Planned: secret rotation hooks.
- Planned: per-request audit metadata.

## Self-Hosting

Runtime embed or service wrapper. Minimal dependencies keep footprint small.
