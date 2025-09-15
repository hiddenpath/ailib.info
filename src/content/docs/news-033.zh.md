---
title: 版本 v0.3.3 发布
group: 新闻
order: 1
status: stable
---

# ai-lib v0.3.3

亮点：

- 开发者体验优化：根级导出（`Tool`、`FunctionCallPolicy`、`FunctionCall`），统一导入（`use ai_lib::Content`）。
- Feature 别名更清晰：`resilience`（interceptors）、`streaming`（unified_sse）、`transport`（unified_transport）、`hot_reload`（config_hot_reload）、`all`（多数 OSS 功能）。
- 文档与网站：新增“特性指南”（中英）、示例统一到 `0.3.3`、企业页面强化价值主张与服务层级。
- 兼容性：增量更新，无破坏性改动。

升级建议：

```toml
[dependencies]
ai-lib = "0.3.3"
# 生产环境建议按需启用：
# ai-lib = { version = "0.3.3", features = ["resilience","transport","streaming"] }
```

快速链接：

- 特性指南：[/zh/docs/features](/zh/docs/features)
- 快速开始：[/zh/docs/getting-started](/zh/docs/getting-started)
- 企业功能与服务：[/zh/docs/enterprise-pro](/zh/docs/enterprise-pro)
- GitHub Releases: [https://github.com/hiddenpath/ai-lib/releases](https://github.com/hiddenpath/ai-lib/releases)


