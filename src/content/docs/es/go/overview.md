---
title: Descripción general del SDK de Go
description: Descripción general de la implementación del runtime ai-lib-go.
---

# ai-lib-go

La implementación en Go de la especificación AI-Protocol. Proporciona un runtime de Go idiomático y de alta concurrencia para interactuar con más de 37 proveedores de IA utilizando una interfaz unificada.

## Capacidades principales

- **Impulsado por manifiesto**: Lee `v2/providers/*.yaml` directamente. Sin lógica codificada.
- **Go nativo**: Utiliza mecanismos de concurrencia estándar de Go 1.21+ para streaming de alto rendimiento.
- **Resiliente**: Timeouts conscientes del contexto, reintentos automáticos usando `net/http`.
- **Tipado seguro**: Mapea esquemas JSON estrictamente a structs de Go.

## Soporte de Protocol V2

El SDK de Go se encuentra actualmente en una fase temprana de desarrollo (v0.5.0), pero implementa las características principales de Ring 1/Ring 2 de la especificación V2:

- Manejo de transporte HTTP (Cabeceras, Autenticación, Construcción de endpoints)
- Decodificación SSE y NDJSON
- Mapeo de clasificación de errores
- Estrategias de acumulación de streaming
- Cancelación consciente del contexto
