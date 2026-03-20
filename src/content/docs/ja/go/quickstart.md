---
title: クイックスタート
description: 数分で ai-lib-go を使い始める。
---

# クイックスタート

`ai-lib-go` を使い始める準備をしましょう。

## インストール

Go プロジェクトにライブラリを追加します：

```bash
go get github.com/ailib-official/ai-lib-go
```

## 基本的な使い方

Go SDK はプロバイダー設定を動的に管理します。OpenAI を使用してレスポンスをストリーミングする方法は以下の通りです：

```go
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/ailib-official/ai-lib-go/client"
)

func main() {
	// マニフェストディレクトリを指す AI_PROTOCOL_PATH が必要です
	// export OPENAI_API_KEY="sk-..."

	ctx := context.Background()

	// OpenAI 用に構成された新しいクライアントを作成
	aiClient, err := client.NewAiClient(ctx, "openai", nil)
	if err != nil {
		panic(err)
	}

	// リクエストの構築
	req := aiClient.Chat().
		Model("gpt-4o").
		User("こんにちは、元気ですか？").
		MaxTokens(100)

	// 標準的な Go のストリーミングパターンを使用してレスポンスをストリーミング
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
		fmt.Printf("\nエラー: %v\n", err)
	}
}
```
