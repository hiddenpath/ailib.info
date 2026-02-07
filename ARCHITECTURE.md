# ailib.info 新架构设计文档

## 🏗️ 整体架构图

```
ailib.info/
├── src/
│   ├── pages/
│   │   ├── index.astro              # 生态首页 (重构)
│   │   ├── 404.astro
│   │   │
│   │   ├── protocol/                # Protocol 专区 (新增)
│   │   │   ├── index.astro          # 协议概览
│   │   │   └── providers/           # Provider 目录 (迁移)
│   │   │       └── index.astro
│   │   │
│   │   ├── rust/                    # Rust SDK 专区 (新增)
│   │   │   ├── index.astro          # SDK 概览
│   │   │   ├── features.astro       # 功能特性
│   │   │   └── quick-start.astro   # 快速开始
│   │   │
│   │   ├── python/                  # Python SDK 专区 (新增)
│   │   │   ├── index.astro          # SDK 概览
│   │   │   ├── features.astro       # 功能特性
│   │   │   └── quick-start.astro   # 快速开始
│   │   │
│   │   ├── docs/                    # 通用文档 (保留)
│   │   │   ├── index.astro          # 文档索引
│   │   │   └── [slug].astro
│   │   │
│   │   ├── zh/                      # 中文版 (重构)
│   │   │   ├── index.astro
│   │   │   ├── protocol/
│   │   │   │   └── index.astro
│   │   │   ├── rust/
│   │   │   │   ├── index.astro
│   │   │   │   └── quick-start.astro
│   │   │   └── python/
│   │   │       ├── index.astro
│   │   │       └── quick-start.astro
│   │   │
│   │   └── blog/                    # 博客 (新增)
│   │       └── [slug].astro
│   │
│   ├── components/
│   │   ├── SiteHeader.astro (重构)  # 新导航栏
│   │   ├── Footer.astro
│   │   │
│   │   ├── Hero.astro (重构)        # 生态 Hero
│   │   ├── ValueProps.astro (重构)  # 价值主张
│   │   │
│   │   ├── ProjectCard.astro (新)   # 三项目卡片
│   │   ├── ComparisonTable.astro (新) # 运行时对比
│   │   ├── RuntimeSelector.astro (新) # 运行时选择器
│   │   │
│   │   ├── Providers.astro (重构)   # Provider Grid
│   │   ├── Architecture.astro (重构) # 架构图
│   │   │
│   │   ├── FAQ.astro
│   │   ├── Support.astro (删除)     # 移除企业支持
│   │   │
│   │   └── shared/
│   │       ├── InstallSnippet.astro (新) # 安装代码块
│   │       ├── VersionBadge.astro   (新) # 版本徽章
│   │       └── CodeExample.astro    (新) # 代码示例
│   │
│   ├── content/
│   │   ├── config.ts (更新)         # 新增 content type
│   │   │
│   │   ├── docs/                    # 文档内容
│   │   │   ├── introduction.md      # 架构介绍
│   │   │   ├── protocol-guide.md    # 协议指南
│   │   │   ├── provider-list.md     # Provider 完整列表
│   │   │   └── concepts.md
│   │   │
│   │   └── blog/                    # 博客文章 (新增)
│   │       ├── v04-release.md
│   │       └── ...
│   │
│   └── styles/
│       ├── global.css
│       ├── theme.css                # 新增主题变量
│       └── components/
│           ├── hero.css
│           ├── card.css
│           └── comparison.css       # 新增
│
├── public/
│   ├── icons/                       # Provider 图标
│   └── images/                      # 图片资源
│       └── architecture/
│           ├── ecosystem.svg        # 生态架构图
│           ├── layers.svg           # 分层架构图
│           └── flow.svg             # 数据流图
│
└── astro.config.mjs (更新)           # Astro 配置
```

## 🔗 新路由映射

### 英文路由
| 路由 | 用途 | 文件 |
|------|------|------|
| `/` | 生态首页 | `pages/index.astro` |
| `/protocol/` | Protocol 概览 | `pages/protocol/index.astro` |
| `/protocol/providers/` | Provider 目录 | `pages/protocol/providers/index.astro` |
| `/rust/` | Rust SDK 概览 | `pages/rust/index.astro` |
| `/rust/quick-start/` | Rust 快速开始 | `pages/rust/quick-start.astro` |
| `/rust/features/` | Rust 功能特性 | `pages/rust/features.astro` |
| `/python/` | Python SDK 概览 | `pages/python/index.astro` |
| `/python/quick-start/` | Python 快速开始 | `pages/python/quick-start.astro` |
| `/python/features/` | Python 功能特性 | `pages/python/features.astro` |
| `/docs/[slug]` | 通用文档 | `pages/docs/[slug].astro` |
| `/blog/[slug]` | 博客文章 | `pages/blog/[slug].astro` |

### 中文路由
| 路由 | 用途 | 文件 |
|------|------|------|
| `/zh/` | 生态首页 (中文) | `pages/zh/index.astro` |
| `/zh/protocol/` | Protocol 概览 | `pages/zh/protocol/index.astro` |
| `/zh/rust/` | Rust SDK 概览 | `pages/zh/rust/index.astro` |
| `/zh/python/` | Python SDK 概览 | `pages/zh/python/index.astro` |

## 🎨 导航栏设计

### 桌面版导航
```html
<nav class="site-header">
  <div class="nav-left">
    <a href="/" class="logo">λAilib</a>
  </div>

  <ul class="nav-menu">
    <li><a href="/">生态首页</a></li>
    <li><a href="/protocol/">Protocol 规范</a></li>
    <li><a href="/rust/">Rust 运行时</a></li>
    <li><a href="/python/">Python 运行时</a></li>
    <li><a href="/blog/">博客</a></li>
  </ul>

  <div class="nav-right">
    <a href="/zh/" class="lang-switch">中文</a>
    <a href="https://github.com/hiddenpath" class="github-link" target="_blank">
      <svg>GitHub</svg>
    </a>
  </div>
</nav>
```

### 移动版导航
- Hamburger menu
- 折叠菜单

### 语言切换器
- 英文版导航中显示 "中文" 链接到 `/zh/`
- 中文版导航中显示 "English" 链接到 `/`

## 🎨 组件设计

### 1. ProjectCard 组件 (新)

```typescript
// src/components/ProjectCard.astro
---
interface Props {
  project: 'protocol' | 'rust' | 'python';
  version: string;
  title: string;
  description: string;
  features: string[];
  link: string;
  icon: string;
}

const { project, version, title, description, features, link, icon } = Astro.props;
---

<div class="project-card" data-project={project}>
  <div class="card-header">
    <img src={icon} alt={title} class="project-icon" />
    <div>
      <h3>{title}</h3>
      <span class="version-badge">v{version}</span>
    </div>
  </div>

  <p class="description">{description}</p>

  <ul class="feature-list">
    {features.map(feature => (
      <li>✓ {feature}</li>
    ))}
  </ul>

  <a href={link} class="card-cta">
    了解更多 →
  </a>
</div>
```

**使用示例**:
```astro
<ProjectCard
  project="protocol"
  version="0.4.0"
  title="AI-Protocol"
  description="统一 AI 模型交互规范"
  features={[
    "30+ 提供商支持",
    "声明式配置",
    "算子式架构"
  ]}
  link="/protocol/"
  icon="/icons/protocol.svg"
/>
```

### 2. ComparisonTable 组件 (新)

```typescript
// src/components/ComparisonTable.astro
---
const isZh = false;
// 配置对比数据
const comparisons = [
  {
    feature: "类型安全",
    protocol: "YAML/JSON Schema",
    rust: "编译时检查",
    python: "运行时类型检查"
  },
  {
    feature: "性能",
    protocol: "N/A (规范)",
    rust: "<1ms 开销",
    python: "约 10-50ms"
  },
  // ... 更多对比项
};
---

<table class="comparison-table">
  <thead>
    <tr>
      <th>特性</th>
      <th>Protocol</th>
      <th>Rust SDK</th>
      <th>Python SDK</th>
    </tr>
  </thead>
  <tbody>
    {comparisons.map(item => (
      <tr>
        <td class="feature">{item.feature}</td>
        <td>{item.protocol}</td>
        <td>{item.rust}</td>
        <td>{item.python}</td>
      </tr>
    ))}
  </tbody>
</table>
```

### 3. RuntimeSelector 组件 (新)

简化版引导用户选择合适运行时的交互组件:

```astro
<div class="runtime-selector">
  <h2>选择适合您的运行时</h2>

  <div class="selector-grid">
    <button class="option" data-target="rust">
      我是 Rust 开发者 / 系统编程
    </button>
    <button class="option" data-target="python">
      我使用 Python / 数据科学 / ML
    </button>
    <button class="option" data-target="protocol">
      我想实现自己的 runtime
    </button>
  </div>

  <div class="recommendations">
    <div class="recommendation rust">
      <h3>推荐使用 ai-lib-rust</h3>
      <p>高性能、类型安全、生产级可靠性</p>
    </div>
    <!-- ... -->
  </div>
</div>
```

### 4. Hero 组件 (重构)

```html
<section class="hero">
  <div class="badge">Ecosystem v0.4.0</div>

  <h1>
    AI-Protocol 生态系统
  </h1>
  <p class="subtitle">
    一个规范，多个运行时：<br/>
    统一的 AI 模型交互方式，支持 Rust 和 Python
  </p>

  <div class="cta-group">
    <a href="https://github.com/hiddenpath/ai-protocol" target="_blank" class="btn primary">
      Protocol 文档 <svgIcon github />
    </a>
    <a href="/rust/quick-start/" class="btn secondary">
      Rust 快速开始
    </a>
    <a href="/python/quick-start/" class="btn secondary">
      Python 快速开始
    </a>
  </div>

  <div class="hero-illustration">
    <!-- 生态架构图 SVG -->
  </div>
</section>
```

## 🎨 样式系统

### 颜色变量
```css
:root {
  /* 主色调 */
  --color-primary: #0a2540;
  --color-primary-light: #1a3a5c;
  --color-accent: #3b82f6;
  --color-accent-hover: #2563eb;

  /* 背景色 */
  --color-bg: #f8fafc;
  --color-bg-dark: #0f172a;

  /* 文本色 */
  --color-text: #0f172a;
  --color-text-dim: #64748b;
  --color-text-light: #94a3b8;

  /* 功能色 */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;

  /* 项目色 */
  --color-protocol: #8b5cf6;
  --color-rust: #dea584;
  --color-python: #3776ab;
}
```

### 组件样式
- `card.css` - 卡片组件（ProjectCard, FeatureCard）
- `comparison.css` - 对比表格
- `hero.css` - Hero section
- `nav.css` - 导航栏
- `provider-grid.css` - Provider 网格

## 📝 Content Collections 更新

### 新增 collections

```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

// Protocol 文档
const protocolDocs = defineCollection({
  schema: z.object({
    title: z.string(),
    topics: z.array(z.string()).optional(),
    order: z.number().optional(),
    status: z.enum(['stable', 'draft', 'deprecated']).optional(),
  }),
});

// 博客文章
const blogPosts = defineCollection({
  schema: z.object({
    title: z.string(),
    publishDate: z.date(),
    author: z.string(),
    tags: z.array(z.string()).optional(),
    draft: z.boolean().optional(),
  }),
});

// Provider 目录
const providers = defineCollection({
  schema: z.object({
    name: z.string(),
    category: z.enum(['global', 'china', 'local', 'custom']),
    homepage: z.string().url(),
    models: z.array(z.string()).optional(),
    status: z.enum(['stable', 'partial', 'beta']).optional(),
  }),
});

export const collections = {
  protocolDocs,
  blogPosts,
  providers,
  // 保留原有的 docs collection
};
```

## 🔗 外部链接结构

### 官方仓库链接
```typescript
const REPOS = {
  protocol: 'https://github.com/hiddenpath/ai-protocol',
  rust: 'https://github.com/hiddenpath/ai-lib-rust',
  python: 'https://github.com/hiddenpath/ai-lib-python',
};

const DOCS = {
  protocol: 'https://github.com/hiddenpath/ai-protocol/tree/main/docs',
  rust: 'https://github.com/hiddenpath/ai-lib-rust/tree/main/docs',
  python: 'https://github.com/hiddenpath/ai-lib-python/blob/main/README.md',
};

const PACKAGES = {
  python: 'https://pypi.org/project/ai-lib-python/',
  rust: 'https://crates.io/crates/ai-lib', // 如果有的话
};
```

## 🚀 性能优化

### 优化策略
1. **静态生成**: 所有页面都是静态 HTML
2. **图片优化**: 使用 Astro Image 组件
3. **代码分割**: 按需加载 JavaScript
4. **CSS 优化**: 使用 Tailwind 或内联关键 CSS
5. **预加载**: 关键资源预加载

### 关键指标
- LCP < 1.5s
- FID < 100ms
- CLS < 0.1

---

**架构版本**: v1.0
**创建日期**: 2025-02-07
**状态**: 🟡 设计阶段
