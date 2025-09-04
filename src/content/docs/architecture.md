---
title: Architecture
group: Overview
order: 40
description: Layered design of the Rust SDK modules.
---

# Architecture

High-level module layering in the crate:

| Layer                         | Module(s)                                            | Responsibility                                       |
| ----------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| Public Facade                 | `AiClient`, `AiClientBuilder`, `Provider`            | Entry points & configuration                         |
| Domain Types                  | `types::request`, `types::response`, `types::common` | Messages, roles, content enums                       |
| API Traits                    | `api::chat`                                          | Chat abstractions + (optional) streaming chunk types |
| Provider Model Registry       | `provider::models`, `provider::configs`              | Capability metadata, selection strategies            |
| Reliability (planned/partial) | (integrated across client / provider strategy)       | Retry, fallback, race, routing hooks                 |
| Transport                     | `transport::{http,dyn_transport}`                    | HTTP execution, proxy, abstraction                   |
| Metrics                       | `metrics`                                            | Extensible instrumentation (noop + trait)            |
| Utilities                     | `utils::file`                                        | File helpers for multimodal / uploads                |

Flow (simplified):
`AiClient` -> build request (types) -> choose provider/model (provider::\*) -> send over `transport` -> parse provider response -> map into unified response structs -> surface via API trait.

Future docs may include sequence diagrams for: basic chat, streaming, and multi-provider fallback chain.
