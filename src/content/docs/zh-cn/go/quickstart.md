---
title: Go 快速开始
description: 几分钟上手 ai-lib-go。
---

# Go 快速开始

## 安装

```bash
go get github.com/ailib-official/ai-lib-go@v1.0.0
export OPENAI_API_KEY="your-key"
```

## 协议优先聊天

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

## 仅 BaseURL（OpenAI 兼容）

```go
client, err := ailib.NewClientBuilder().
	WithBaseURL("https://api.openai.com/v1").
	WithAPIKey(os.Getenv("OPENAI_API_KEY")).
	Build()
```

## 回退（策略层）

```go
import "github.com/ailib-official/ai-lib-go/pkg/contact"

fb := contact.NewFallbackClient([]ailib.Client{primary, secondary})
```

## 下一步

- **[Client API](/zh-cn/go/client/)**
- **[流式处理](/zh-cn/go/streaming/)**
