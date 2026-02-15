---
title: モデルレジストリ
description: AI-Protocol のモデルレジストリがモデル識別子をプロバイダー設定にマッピングする方法 — 機能と価格を含む。
---

# モデルレジストリ

モデルレジストリ（`v1/models/*.yaml`）は、モデル識別子をプロバイダー設定にマッピングし、各モデルの機能、コンテキストウィンドウ、価格を記録します。

## モデルファイル構造

モデルはファミリ（GPT、Claude、Gemini など）ごとに整理されています：

```
v1/models/
├── gpt.yaml          # OpenAI GPT モデル
├── claude.yaml        # Anthropic Claude モデル
├── gemini.yaml        # Google Gemini モデル
├── deepseek.yaml      # DeepSeek モデル
├── qwen.yaml          # Alibaba Qwen モデル
├── mistral.yaml       # Mistral モデル
├── llama.yaml         # Meta Llama モデル
└── ...                # 28 以上のモデルファイル
```

## モデル定義

各モデルエントリには以下が含まれます：

```yaml
models:
  gpt-4o:
    provider: openai
    model_id: "gpt-4o"
    context_window: 128000
    max_output_tokens: 16384
    capabilities:
      - chat
      - streaming
      - tools
      - vision
      - json_mode
    pricing:
      input_per_token: 0.0000025
      output_per_token: 0.00001
    release_date: "2024-05-13"
```

## モデル識別子

ランタイムはモデルを識別するために `provider/model` 形式を使用します：

```
anthropic/claude-3-5-sonnet
openai/gpt-4o
deepseek/deepseek-chat
gemini/gemini-2.0-flash
qwen/qwen-plus
```

ランタイムはこれを次のように分割します：
1. **プロバイダー ID**（`anthropic`）→ プロバイダーマニフェストを読み込む
2. **モデル名**（`claude-3-5-sonnet`）→ モデルレジストリで検索

## 機能

標準機能フラグ：

| 機能 | 説明 |
|------|------|
| `chat` | 基本チャット補完 |
| `streaming` | ストリーミングレスポンス |
| `tools` | 関数/ツール呼び出し |
| `vision` | 画像理解 |
| `audio` | オーディオ入出力 |
| `reasoning` | 拡張思考（CoT） |
| `agentic` | マルチステップエージェントワークフロー |
| `json_mode` | 構造化 JSON 出力 |

## 価格

トークンごとの価格により、ランタイムでのコスト見積もりが可能になります：

```yaml
pricing:
  input_per_token: 0.000003      # 100万入力トークンあたり $3
  output_per_token: 0.000015     # 100万出力トークンあたり $15
  cached_input_per_token: 0.0000003  # キャッシュプロンプト割引
```

Rust と Python の両ランタイムが `CostEstimate` 計算にこのデータを使用します。

## 検証

本番デプロイメント用の検証ステータスをモデルに含めることができます：

```yaml
verification:
  status: "verified"
  last_checked: "2025-01-15"
  verified_capabilities:
    - chat
    - streaming
    - tools
```

## 次のステップ

- **[プロバイダーへの貢献](/protocol/contributing/)** — 新規プロバイダーとモデルの追加
- **[クイックスタート](/quickstart/)** — ランタイムでモデルを使用開始
