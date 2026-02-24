# AI-Lib Ecosystem Documentation (ailib.info)

[English](./README.md) | [简体中文](./README_zh-CN.md)

Welcome to the official documentation repository for the **AI-Lib** ecosystem. This website ([ailib.info](https://ailib.info)) serves as the central hub for developers to understand, integrate, and master AI-protocol-driven development.

## 🌟 Our Mission

The AI-Lib ecosystem aims to **standardize AI interaction**. We believe that "All logic is operators, all configuration is protocol." By decoupler provider-specific logic from application code, we enable developers to build resilient, provider-agnostic AI applications with zero code changes when switching models.

## 📖 What's Inside?

This site provides comprehensive guides and technical specifications for the entire ecosystem:

### 1. AI-Protocol
The foundation of the ecosystem. A language-agnostic specification using YAML/JSON manifests to describe AI providers, model capabilities, and interaction rules (MCP, Computer Use, Multimodal).

### 2. Runtime SDKs
- **[ai-lib-rust](https://github.com/hiddenpath/ai-lib-rust)**: A high-performance, resilient Rust implementation of the AI-Protocol.
- **[ai-lib-python](https://github.com/hiddenpath/ai-lib-python)**: A developer-friendly, Pydantic-powered Python implementation.
- **[ai-lib-ts](https://github.com/hiddenpath/ai-lib-ts)**: The TypeScript/JavaScript implementation for web and Node.js environments.

### 3. Guides & Tutorials
- **Quick Start**: Get your first AI request running in minutes.
- **Core Concepts**: Understand how the streaming pipeline, capability registry, and resilience patterns work.
- **Advanced Features**: Deep dives into MCP tool integration, Computer Use (GUI automation), and Multimodal capabilities.

## 🌍 Background & Origin

AI-Lib was born out of the frustration of managing fragmented AI SDKs. As the number of AI providers exploded, developers found themselves trapped in a cycle of rewriting integration code. 

We started with **AI-Protocol**, a vision to move API logic into data manifests. This led to the creation of **ai-lib-rust** and **ai-lib-python**, the first runtimes to prove that a single unified API could handle dozens of disparate providers without a single `if provider == "openai"` check in the core logic.

Today, AI-Lib supports over 38 providers and continues to evolve with the latest AI capabilities like MCP and Computer Use.

---

## 🛠️ For Maintainers

This site is built with **Astro Starlight**.

### Local Development

```bash
npm install
npm run dev
```

### Build & Deploy

- **Build**: `npm run build` (Static export to `dist/`)
- **Deploy**: Automatically deployed to **Vercel** on every push to `main`.
- **Domain**: Managed at `ailib.info` (aliased to `ailib.rs`).

## 📜 License

Content and code are licensed under **MIT / Apache-2.0**, matching the main AI-Lib projects.

---
