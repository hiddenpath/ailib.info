---
title: 快速入门
description: 几分钟内上手 ai-lib-go。
---

# 快速入门

开始使用 `ai-lib-go`。

## 安装

将库添加到你的 Go 项目中：

```bash
go get github.com/ailib-official/ai-lib-go
```

## 基本用法

Go SDK 动态管理供应商配置。以下是使用 OpenAI 处理流式响应的示例：

```go
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/ailib-official/ai-lib-go/client"
)

func main() {
	// 需要 AI_PROTOCOL_PATH 指向你的清单目录
	// export OPENAI_API_KEY="sk-..."

	ctx := context.Background()

	// 创建一个配置为使用 OpenAI 的新客户端
	aiClient, err := client.NewAiClient(ctx, "openai", nil)
	if err != nil {
		panic(err)
	}

	// 构建请求
	req := aiClient.Chat().
		Model("gpt-4o").
		User("你好，最近怎么样？").
		MaxTokens(100)

	// 使用标准 Go 流式处理模式
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
		fmt.Printf("\n错误: %v\n", err)
	}
}
```
