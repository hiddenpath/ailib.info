---
title: 常见问题
group: 概述
order: 90
---

# 常见问题

## 这个库是否可用于生产环境？

核心抽象（客户端、请求/响应类型）已经可用。可靠性原语（重试/回退/竞争/路由）是重点；速率限制和熔断器部分完成。

## 为什么不直接调用提供商？

统一的Rust API减少了每个提供商的代码路径，并支持跨提供商的可靠性策略。

## 支持哪些语言绑定？

目前支持Rust（crate）。其他语言包装器可能会在以后出现；请关注仓库路线图。

## 如何选择最适合的提供商？

选择提供商取决于你的具体需求：

- **速度和成本**：Groq提供超低延迟
- **推理质量**：Anthropic Claude 3适合复杂任务
- **多模态**：OpenAI GPT-4或Google Gemini
- **本地部署**：Ollama支持私有部署
- **中文支持**：百度文心、腾讯混元等

## 如何处理API速率限制？

ai-lib内置了速率限制和重试机制：

```rust
// 自动重试和速率限制
let resp = client.chat_completion(req).await?;

// 检查错误是否可重试
match client.chat_completion(req).await {
    Ok(response) => println!("成功"),
    Err(e) if e.is_retryable() => {
        // 实现自定义重试逻辑
    }
    Err(e) => println!("永久错误: {}", e),
}
```

## 支持哪些模型类型？

ai-lib支持各种模型类型：

- **文本生成**：GPT-4、Claude 3、Llama 3等
- **多模态**：支持图像、音频输入
- **函数调用**：结构化工具调用
- **流式处理**：实时响应生成

## 如何配置代理？

支持多种代理配置方式：

```bash
# 环境变量
export AI_PROXY_URL=http://proxy.example.com:8080
```

```rust
// 编程方式
let client = AiClient::with_options(
    Provider::OpenAI,
    ConnectionOptions {
        proxy: Some("http://proxy:8080".into()),
        ..Default::default()
    }
)?;
```

## 性能如何？

ai-lib经过优化，具有：

- **低延迟**：SDK开销<1ms
- **高吞吐**：支持并发批处理
- **内存效率**：最小内存占用
- **连接复用**：内置连接池

## 如何贡献？

欢迎贡献！请：

1. Fork仓库
2. 创建功能分支
3. 运行测试：`cargo test`
4. 提交PR

## 许可证是什么？

ai-lib采用双重许可证：
- MIT许可证
- Apache许可证2.0

你可以选择最适合你项目的许可证。

## 如何获取支持？

- **文档**：查看完整文档
- **Issues**：在GitHub上报告问题
- **讨论**：参与社区讨论
- **示例**：查看examples目录
