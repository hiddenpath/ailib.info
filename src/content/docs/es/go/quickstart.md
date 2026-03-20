---
title: Inicio rápido
description: Comienza con ai-lib-go en minutos.
---

# Inicio rápido

Pónte en marcha con `ai-lib-go`.

## Instalación

Añade la librería a tu proyecto de Go:

```bash
go get github.com/ailib-official/ai-lib-go
```

## Uso básico

El SDK de Go gestiona las configuraciones de los proveedores de forma dinámica. Así es como se transmite una complet散 (completion) usando OpenAI:

```go
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/ailib-official/ai-lib-go/client"
)

func main() {
	// Requiere que AI_PROTOCOL_PATH apunte a tu directorio de manifiestos
	// export OPENAI_API_KEY="sk-..."

	ctx := context.Background()

	// Crear un nuevo cliente, configurado para OpenAI
	aiClient, err := client.NewAiClient(ctx, "openai", nil)
	if err != nil {
		panic(err)
	}

	// Construir la solicitud
	req := aiClient.Chat().
		Model("gpt-4o").
		User("Hola, ¿cómo estás?").
		MaxTokens(100)

	// Transmitir la respuesta usando el patrón de streaming estándar de Go
	stream, err := req.ExecuteStream(ctx)
	if err != nil {
		panic(err)
	}
	defer stream.Close()

	for stream.Next() {
		event := stream.Event()
		if event.Type == "content" {
			fmt.Print(event.Text)
		}
	}

	if err := stream.Err(); err != nil {
		fmt.Printf("\nError: %v\n", err)
	}
}
```
