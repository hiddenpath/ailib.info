---
title: Release v0.3.3
group: News
order: 0
status: stable
---

# ai-lib v0.3.3

Highlights:

- Developer ergonomics: root-level exports (`Tool`, `FunctionCallPolicy`, `FunctionCall`) and unified imports (`use ai_lib::Content`).
- Feature alias presets for clarity: `resilience` (interceptors), `streaming` (unified_sse), `transport` (unified_transport), `hot_reload` (config_hot_reload), `all` (most OSS features).
- Docs & Website: new Features guide (EN/ZN), examples updated to `0.3.3`, refined Enterprise pages with value proposition and service tiers.
- Compatibility: additive, no breaking changes.

Upgrade tips:

```toml
[dependencies]
ai-lib = "0.3.3"
# Or selectively enable features (recommended for production):
# ai-lib = { version = "0.3.3", features = ["resilience","transport","streaming"] }
```

Quick links:

- Features Guide: [/docs/features](/docs/features)
- Getting Started: [/docs/getting-started](/docs/getting-started)
- Enterprise Features & Services: [/docs/enterprise-pro](/docs/enterprise-pro)
- GitHub Releases: [https://github.com/hiddenpath/ai-lib/releases](https://github.com/hiddenpath/ai-lib/releases)


