---
title: プロバイダーマニフェスト
description: AI-Protocol プロバイダーマニフェストの仕組み — エンドポイント設定、認証、パラメータマッピング、ストリーミング、エラーハンドリング。
---

# プロバイダーマニフェスト

エコシステム内の各 AI プロバイダーには、その API とのやり取り方法を完全に記述する YAML マニフェストファイル（`v1/providers/<provider>.yaml`）があります。

## サポート対象プロバイダー

プロバイダーマニフェストは 2 つの形式で利用可能です：**v1**（レガシー）と **v2-alpha**。v2-alpha 形式は Ring 1/2/3 同心円構造（コアスケルトン → 機能マッピング → 高度な拡張）を使用します。**OpenAI、Anthropic、Gemini** は v1 と v2-alpha 両方の形式で利用可能です。

### グローバルプロバイダー

OpenAI、Anthropic、Google Gemini、Groq、Mistral、Cohere、Perplexity、Together AI、DeepInfra、OpenRouter、Azure OpenAI、NVIDIA、Fireworks AI、Replicate、AI21 Labs、Cerebras、Lepton AI、Grok

### 中国リージョンプロバイダー

DeepSeek、Qwen（Alibaba）、Zhipu GLM、Doubao（ByteDance）、Baidu ERNIE、iFlytek Spark、Tencent Hunyuan、SenseNova、Tiangong、Moonshot（Kimi）、MiniMax、Baichuan、Yi（01.AI）、SiliconFlow

## マニフェスト構造

### エンドポイント設定

```yaml
endpoint:
  base_url: "https://api.openai.com/v1"
  chat_path: "/chat/completions"
  protocol: "https"
  timeout_ms: 60000
```

### 認証

複数の認証タイプをサポートします：

```yaml
# Bearer トークン（最も一般的）
auth:
  type: bearer
  token_env: "OPENAI_API_KEY"

# ヘッダー内の API キー
auth:
  type: api_key
  header: "x-api-key"
  token_env: "ANTHROPIC_API_KEY"

# カスタムヘッダー
auth:
  type: bearer
  token_env: "ANTHROPIC_API_KEY"
  headers:
    anthropic-version: "2023-06-01"
```

### パラメータマッピング

標準パラメータ名をプロバイダー固有のフィールドにマッピングします：

```yaml
parameter_mappings:
  temperature: "temperature"
  max_tokens: "max_completion_tokens"  # OpenAI は異なる名前を使用
  stream: "stream"
  tools: "tools"
  tool_choice: "tool_choice"
  response_format: "response_format"
```

### ストリーミング設定

ストリーミングレスポンスのデコードと解釈方法を宣言します：

```yaml
streaming:
  decoder:
    format: "sse"              # "sse"、"ndjson"、または "anthropic_sse"
    done_signal: "[DONE]"      # ストリーム終了マーカー
  event_map:
    - match: "$.choices[0].delta.content"
      emit: "PartialContentDelta"
      extract:
        content: "$.choices[0].delta.content"
    - match: "$.choices[0].delta.tool_calls"
      emit: "PartialToolCall"
      extract:
        tool_calls: "$.choices[0].delta.tool_calls"
    - match: "$.choices[0].finish_reason"
      emit: "StreamEnd"
      extract:
        finish_reason: "$.choices[0].finish_reason"
```

### エラー分類

HTTP レスポンスを標準エラー型にマッピングします：

```yaml
error_classification:
  by_http_status:
    "400": "invalid_request"
    "401": "authentication"
    "403": "permission"
    "404": "not_found"
    "429": "rate_limited"
    "500": "server_error"
    "503": "overloaded"
  by_error_code:
    "context_length_exceeded": "context_length"
    "content_filter": "content_filter"
```

### 機能

ランタイムがリクエスト前にチェックするフィーチャーフラグ：

```yaml
capabilities:
  streaming: true
  tools: true
  vision: true
  audio: false
  reasoning: true
  agentic: true
  json_mode: true
```

## ランタイムがマニフェストを使用する方法

1. **読み込み** — YAML マニフェストを読み込む（ローカル、環境変数、または GitHub）
2. **検証** — JSON Schema で検証
3. **コンパイル** — パラメータマッピングを使用してユーザーリクエストを変換
4. **実行** — 正しい認証/ヘッダーで HTTP リクエストを送信
5. **デコード** — ストリーミング設定を使用してレスポンスを処理
6. **分類** — 分類ルールを使用してエラーを処理

## 次のステップ

- **[モデルレジストリ](/protocol/models/)** — モデルの設定方法
- **[プロバイダーへの貢献](/protocol/contributing/)** — 新規プロバイダーの追加
