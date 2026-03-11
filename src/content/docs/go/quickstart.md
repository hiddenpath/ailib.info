---
title: Quick Start
description: Get started with ai-lib-go in minutes.
---

# Quick Start

Get up and running with `ai-lib-go`.

## Installation

Add the library to your Go project:

```bash
go get github.com/hiddenpath/ai-lib-go
```

## Basic Usage

The Go SDK manages provider configurations dynamically. Here's how to stream a completion using OpenAI:

```go
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/hiddenpath/ai-lib-go/client"
)

func main() {
	// Require AI_PROTOCOL_PATH to point to your manifests directory
	// export OPENAI_API_KEY="sk-..."

	ctx := context.Background()

	// Create a new client, configured for OpenAI
	aiClient, err := client.NewAiClient(ctx, "openai", nil)
	if err != nil {
		panic(err)
	}

	// Build the request
	req := aiClient.Chat().
		Model("gpt-4o").
		User("Hello, how are you?").
		MaxTokens(100)

	// Stream the response using Go iterators (iter.Seq2)
	for event, err := range req.Stream(ctx) {
		if err != nil {
			fmt.Printf("Error: %v\n", err)
			break
		}

		if event.Type == "content" {
			fmt.Print(event.Text)
		}
	}
}
```
