---
title: Go Quick Start
description: Get up and running with ai-lib-go.
---

# Go Quick Start

## Installation

```bash
go get github.com/ailib-official/ai-lib-go@v1.0.0
export OPENAI_API_KEY="your-key"
```

## Protocol-first chat

```go
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/ailib-official/ai-lib-go/pkg/ailib"
)

func main() {
	manifestYAML := `id: openai
protocol_version: "2.0"
endpoint:
  base_url: "https://api.openai.com/v1"
`
	client, err := ailib.NewClientBuilder().
		WithProtocolData([]byte(manifestYAML)).
		WithAPIKey(os.Getenv("OPENAI_API_KEY")).
		Build()
	if err != nil {
		panic(err)
	}
	defer client.Close()

	resp, err := client.Chat(context.Background(), []ailib.Message{
		{Role: ailib.RoleUser, Content: "Hello!"},
	}, &ailib.ChatOptions{Model: "gpt-4o"})
	if err != nil {
		panic(err)
	}
	fmt.Println(resp.Choices[0].Message.Content)
}
```

## BaseURL-only (OpenAI-compatible)

```go
client, err := ailib.NewClientBuilder().
	WithBaseURL("https://api.openai.com/v1").
	WithAPIKey(os.Getenv("OPENAI_API_KEY")).
	Build()
```

## Fallback (policy layer)

```go
import "github.com/ailib-official/ai-lib-go/pkg/contact"

fb := contact.NewFallbackClient([]ailib.Client{primary, secondary})
```

## Next Steps

- **[Client API](/go/client/)**
- **[Streaming](/go/streaming/)**
