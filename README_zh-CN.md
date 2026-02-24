# AI-Lib 生态系统文档 (ailib.info)

[English](./README.md) | [简体中文](./README_zh-CN.md)

欢迎来到 **AI-Lib** 生态系统的官方文档仓库。本网站 ([ailib.info](https://ailib.info)) 是开发者了解、集成和掌握 AI 协议驱动开发的核心枢纽。

## 🌟 我们的使命

AI-Lib 生态系统旨在 **标准化 AI 交互**。我们坚信“逻辑即算子，配置即协议”。通过将特定供应商的逻辑从应用程序代码中解耦，我们使开发者能够构建具有韧性的、与供应商无关的 AI 应用程序，在切换模型时无需更改任何代码。

## 📖 网站内容

本网站为整个生态系统提供了全面的指南和技术规范：

### 1. AI-Protocol
生态系统的基石。一个与语言无关的规范，使用 YAML/JSON 配置清单来描述 AI 供应商、模型能力和交互规则（MCP、Computer Use、多模态）。

### 2. 运行时 SDKs
- **[ai-lib-rust](https://github.com/hiddenpath/ai-lib-rust)**: AI-Protocol 的高性能、高韧性 Rust 实现。
- **[ai-lib-python](https://github.com/hiddenpath/ai-lib-python)**: 开发者友好、由 Pydantic 驱动的 Python 实现。
- **[ai-lib-ts](https://github.com/hiddenpath/ai-lib-ts)**: 适用于 Web 和 Node.js 环境的 TypeScript/JavaScript 实现。

### 3. 指南与教程
- **快速开始**: 在几分钟内运行你的第一个 AI 请求。
- **核心概念**: 了解流式渲染管线、能力注册表和韧性模式的工作原理。
- **高级特性**: 深入探讨 MCP 工具集成、Computer Use（GUI 自动化）和多模态能力。

## 🌍 背景与起源

AI-Lib 诞生于对碎片化 AI SDK 的管理困境。随着 AI 供应商数量的爆炸式增长，开发者发现自己陷入了不断重写集成代码的死循环。

我们从 **AI-Protocol** 开始，愿景是将 API 逻辑移至数据配置清单中。这促使了 **ai-lib-rust** 和 **ai-lib-python** 的诞生，它们作为首批运行时，证明了单个统一 API 可以处理数十个迥异的供应商，而无需在核心逻辑中编写任何 `if provider == "openai"` 之类的判断。

今天，AI-Lib 支持超过 38 个供应商，并持续进化以支持最新的 AI 能力，如 MCP 和 Computer Use。

---

## 🛠️ 维护者指南

本网站使用 **Astro Starlight** 构建。

### 本地开发

```bash
npm install
npm run dev
```

### 构建与部署

- **构建**: `npm run build` (静态导出至 `dist/` 目录)
- **部署**: 每次推送到 `main` 分支时会自动部署到 **Vercel**。
- **域名**: 由 `ailib.info` 管理（别名为 `ailib.rs`）。

## 📜 许可证

内容和代码均采用 **MIT / Apache-2.0** 许可证，与 AI-Lib 主项目保持一致。
