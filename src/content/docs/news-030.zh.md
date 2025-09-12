---
title: 版本 v0.3.2 发布
group: 新闻
order: 1
status: stable
---

# ai-lib v0.3.2

亮点：

- **增强的可靠性功能**：改进的流式处理性能和错误处理
- **JSONL 流式协议**：完整的增量/最终类型结构化流式处理实现
- **统一传输 API**：跨所有提供商的标准化 HTTP 客户端工厂和配置
- **函数调用兼容性**：跨提供商支持 OpenAI 风格的 `tool_calls` 和自动解析字符串化 JSON 参数
- **拦截器管道**：可插拔的 `InterceptorPipeline`，包含重试、超时和熔断器模式的默认/最小预设
- **企业级架构**：ai-lib-pro 企业功能的基础

新功能：

- **增量 JSON 解析器**：高性能流式内容提取和适当的错误处理
- **增强的示例**：所有主要提供商和用例的综合示例
- **黄金测试用例**：广泛的 SSE 流式测试覆盖和 MD5 一致性验证
- **可配置的流式演示**：通过环境变量支持模型覆盖
- **构建器 UX 改进**：具有增强配置选项的 `AiClientBuilder`

快速链接：

- 路由指南: /zh/docs/reliability-routing
- 可观测性: /zh/docs/observability
- 企业功能: /zh/docs/enterprise-pro
- GitHub Releases: https://github.com/hiddenpath/ai-lib/releases

