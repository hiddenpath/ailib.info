# ailib.info 重构分步实施计划

## 📋 实施概览

本文档提供详细的技术实施步骤，按照优先级分为三个阶段：

- **Phase 1 (P1)**: 核心页面重构（高优先级）
- **Phase 2 (P2)**: 项目专区创建（中优先级）
- **Phase 3 (P3)**: 内容补充与清理（中优先级）
- **Phase 4 (P4)**: 文档整理（低优先级）
- **Phase 5 (P5)**: 审查与测试（低优先级）

---

## 🔧 准备工作

### 1. 确认开发环境

```bash
# 确认 Node.js 版本
node --version  # 应该 >= 18.0.0

# 确认项目目录
cd ~/ailib.info

# 安装依赖（如果还没安装）
npm install

# 启动开发服务器
npm run dev
```

### 2. 分支策略

```bash
# 创建重构分支
git checkout -b refactor/ecosystem-rewrite

# 推送备份
git push -u origin refactor/ecosystem-rewrite
```

---

## Phase 1: 核心页面重构 (P1)

### P1-1: 重构导航栏 (P1-NAV)

**文件**: `src/components/SiteHeader.astro`

**目标**:
- 替换旧的 "Docs" 链接为三项目导航
- 添加语言切换器（EN/ZH）
- 保持响应式设计

**实施步骤**:

1. 读取现有导航栏代码
```bash
cat src/components/SiteHeader.astro
```

2. 修改导航菜单
```astro
---

const { locale = 'en' } = Astro.props;
const isZh = locale === '';

---

<nav class={isZh ? 'nav zh' : 'nav'}>
  <a href={isZh ? '/zh/' : '/'} class="logo">λAilib</a>

  <ul class="menu">
    <li><a href={isZh ? '/zh/' : '/'}>{isZh ? '生态首页' : 'Home'}</a></li>
    <li><a href={isZh ? '/zh/protocol/' : '/protocol/'}>Protocol</a></li>
    <li><a href={isZh ? '/zh/rust/' : '/rust/'}>Rust</a></li>
    <li><a href={isZh ? '/zh/python/' : '/python/'}>Python</a></li>
  </ul>

  <div class="actions">
    <a href={isZh ? '/' : '/zh/'} class="lang-switch">
      {isZh ? 'EN' : '中文'}
    </a>
    <a href="https://github.com/hiddenpath/ai-protocol" target="_blank" class="github">
      GitHub
    </a>
  </div>
</nav>
```

3. 更新样式（如果有独立 CSS 文件）

**验证**:
```bash
# 检查导航链接是否正确
grep -r "enterprise" src/  # 应该返回空（删除了企业版链接）
```

---

### P1-2: 重构首页 Hero (P1-HERO)

**文件**: `src/components/Hero.astro` 和 `src/pages/index.astro`

**目标**:
- 将 Hero 从单一 ai-lib 营销改为生态入口
- 添加三项目卡片展示
- 添加运行时选择引导

**实施步骤**:

#### Step 2.1: 更新 Hero 组件

```astro
---
// src/components/Hero.astro
const { locale = 'en' } = Astro.props;
const isZh = locale === 'zh';

const heroContent = {
  en: {
    badge: 'Ecosystem Release v0.4.0',
    title: 'AI-Protocol Ecosystem',
    subtitle: 'One specification, multiple runtimes.',
    description: 'Unified AI model interaction across protocol, Rust, and Python.',
    ctas: [
      { text: 'Protocol Spec', link: 'https://github.com/hiddenpath/ai-protocol' },
      { text: 'Rust Runtime', link: '/rust/quick-start/' },
      { text: 'Python Runtime', link: '/python/quick-start/' },
    ]
  },
  zh: {
    badge: '生态发布 v0.4.0',
    title: 'AI-Protocol 生态系统',
    subtitle: '一个规范，多个运行时',
    description: '统一的 AI 模型交互方式，支持协议层、Rust 和 Python 实现。',
    ctas: [
      { text: '查看协议文档', link: 'https://github.com/hiddenpath/ai-protocol' },
      { text: 'Rust 快速开始', link: '/rust/quick-start/' },
      { text: 'Python 快速开始', link: '/python/quick-start/' },
    ]
  }
};
const content = isZh ? heroContent.zh : heroContent.en;
---

<section class="hero">
  <span class="badge">{content.badge}</span>

  <h1>{content.title}</h1>
  <p class="subtitle">{content.subtitle}</p>
  <p class="description">{content.description}</p>

  <div class="cta-group">
    {content.ctas.map((cta, i) => (
      <a href={cta.link} class={`btn ${i === 0 ? 'primary' : 'secondary'}`}>
        {cta.text}
      </a>
    ))}
  </div>
</section>
```

#### Step 2.2: 创建 ProjectCard 组件

```bash
# 创建新组件文件
touch src/components/ProjectCard.astro
```

```astro
---
// src/components/ProjectCard.astro
interface Props {
  locale?: 'en' | 'zh';
  project: 'protocol' | 'rust' | 'python';
  version: string;
  title: string;
  titleZh?: string;
  description: string;
  descriptionZh?: string;
  features: string;
  featuresZh?: string;
  link: string;
  icon: string;
}

const {
  locale = 'en',
  project,
  version,
  title,
  titleZh,
  description,
  descriptionZh,
  features,
  featuresZh,
  link,
  icon
} = Astro.props;

const isZh = locale === 'zh';
const displayTitle = isZh && titleZh ? titleZh : title;
const displayDesc = isZh && descriptionZh ? descriptionZh : description;
const displayFeatures = isZh && featuresZh ? featuresZh : features;
---

<div class={`project-card ${project}`}>
  <div class="card-header">
    <img src={icon} alt={displayTitle} class="project-icon" />
    <div>
      <h3>{displayTitle}</h3>
      <span class="version-badge">v{version}</span>
    </div>
  </div>

  <p class="description">{displayDesc}</p>

  <div class="features">
    {displayFeatures.split('、').map(f => (
      <span class="feature-tag">{f.trim()}</span>
    ))}
  </div>

  <a href={link} class="card-cta">
    {isZh ? '了解更多' : 'Learn more'} →
  </a>
</div>

<style>
  .project-card {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    background: white;
    transition: all 0.2s;
  }

  .project-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
  }

  .card-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 16px;
  }

  .project-icon {
    width: 48px;
    height: 48px;
  }

  .version-badge {
    display: inline-block;
    background: #f1f5f9;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
  }

  .card-cta {
    display: inline-block;
    margin-top: 16px;
    color: #3b82f6;
    text-decoration: none;
    font-weight: 500;
  }
</style>
```

#### Step 2.3: 更新主页使用新组件

```astro
---
// src/pages/index.astro (更新)
import '../styles/global.css';
import SiteHeader from '../components/SiteHeader.astro';
import Hero from '../components/Hero.astro';
import SiteFooter from '../components/Footer.astro';
import ProjectCard from '../components/ProjectCard.astro';

const locale = 'en';
---

<html lang="en">
  <head>
    <title>AI-Protocol Ecosystem</title>
  </head>
  <body>
    <SiteHeader locale={locale} />
    <Hero locale={locale} />

    <section class="projects-grid">
      <ProjectCard
        locale={locale}
        project="protocol"
        version="0.4.0"
        title="AI-Protocol"
        titleZh="AI-Protocol 规范"
        description="Specification for unified AI model interaction"
        descriptionZh="统一 AI 模型交互规范定义"
        features="30+ Providers、算子式架构、声明式配置"
        featuresZh="30+ 提供商、算子式架构、声明式配置"
        link="/protocol/"
        icon="/icons/protocol.svg"
      />
      <ProjectCard
        locale={locale}
        project="rust"
        version="0.6.6"
        title="ai-lib-rust"
        titleZh="ai-lib-rust Rust 运行时"
        description="High-performance Rust implementation with 14 architectural layers"
        descriptionZh="高性能 Rust 实现，14 层架构设计"
        features="类型安全、<1ms 开销、企业级可靠性"
        featuresZh="类型安全、<1ms 开销、企业级可靠性"
        link="/rust/"
        icon="/icons/rust.svg"
      />
      <ProjectCard
        locale={locale}
        project="python"
        version="0.5.0"
        title="ai-lib-python"
        titleZh="ai-lib-python Python 运行时"
        description="Official Python runtime with type-safe and async support"
        descriptionZh="官方 Python 运行时，支持类型安全和异步"
        features="PyPI 已发布、Jupyter 集成、96% 功能完整"
        featuresZh="PyPI 已发布、Jupyter 集成、96% 功能完整"
        link="/python/"
        icon="/icons/python.svg"
      />
    </section>

    <SiteFooter locale={locale} />
  </body>
</html>
```

**验证**:
```bash
# 检查是否有旧的 ai-lib 引用
grep -r "ai-lib-" src/pages/index.astro

# 应该找到的就是新组件的引用
```

---

### P1-3: 更新 Value Props 组件

**文件**: `src/components/ValueProps.astro`

**目标**:
- 更新价值主张以反映三方项目共同价值
- 强调 Protocol 的统一性 + Runtime 的多样性

**内容更新**:

```astro
---
// src/components/ValueProps.astro

const values = {
  en: [
    { icon: '🔌', title: 'Protocol-Driven', desc: 'Decouple providers from code with declarative configuration' },
    { icon: '⚙️', title: 'Multi-Runtime', desc: 'Choose Rust for performance or Python for flexibility' },
    { icon: '🚀', title: 'Production-Ready', desc: '95% feature parity, enterprise-grade reliability' },
  ],
  zh: [
    { icon: '🔌', title: '协议驱动', desc: '用声明式配置将提供商与代码解耦' },
    { icon: '⚙️', title: '多运行时', desc: '选 Rust 追求性能，选 Python 追求灵活' },
    { icon: '🚀', title: '生产级', desc: '95% 功能对等，企业级可靠性' },
  ]
};
// ... 渲染逻辑
---
```

---

## Phase 2: 三大项目专区创建 (P2)

### P2-1: 创建 Protocol 专区 (P2-PROTOCOL)

**目标**: 建立独立的 Protocol 介绍页面

**步骤**:

```bash
# 创建目录结构
mkdir -p src/pages/protocol
mkdir -p src/pages/zh/protocol
```

#### Step 2.1.1: 创建 Protocol 概览页

```astro
---
// src/pages/protocol/index.astro
import '../../styles/global.css';
import SiteHeader from '../../components/SiteHeader.astro';
import Footer from '../../components/Footer.astro';

const locale = 'en';
const isZh = locale === 'zh';
---

<html lang="en">
  <head>
    <title>AI-Protocol Specification | ailib.info</title>
  </head>
  <body>
    <SiteHeader locale={locale} />

    <main class="protocol-page">
      <section class="page-hero">
        <h1>AI-Protocol</h1>
        <p class="subtitle">
          {isZh
            ? '数据驱动的声明式运行时规范'
            : 'Data-driven declarative runtime specification'}
        </p>
        <p>
          {isZh
            ? '一切逻辑皆算子，一切配置皆协议。统一的 AI 模型交互方式，支持 30+ 提供商。'
            : 'All logic is operators, all configuration is protocol. Unified AI model interaction with 30+ providers.'}
        </p>

        <div class="cta-group">
          <a href="https://github.com/hiddenpath/ai-protocol" target="_blank" class="btn primary">
            GitHub Repository
          </a>
          <a href="/protocol/providers/" class="btn secondary">
            View Providers
          </a>
        </div>
      </section>

      <section class="features">
        <h2>{isZh ? '核心特性' : 'Key Features'}</h2>

        <div class="feature-grid">
          <div class="feature">
            <h3>📋 Declaraive Config</h3>
            <p>{isZh ? 'YAML/JSON 配置定义模型和参数' : 'Define models and parameters with YAML/JSON'}</p>
          </div>

          <div class="feature">
            <h3>🔗 Provider Abstraction</h3>
            <p>{isZh ? '统一接口，支持 30+ AI 提供商' : 'Unified interface for 30+ AI providers'}</p>
          </div>

          <div class="feature">
            <h3>🔢 Data-State Rulebook</h3>
            <p>{isZh ? '基于数据的处理算子而非硬编码逻辑' : 'Data-based processing operators, not hardcoded logic'}</p>
          </div>
        </div>
      </section>

      <section class="stats">
        <h2>{isZh ? '覆盖范围' : 'Coverage'}</h2>
        <div class="stats-grid">
          <div class="stat">
            <div class="number">30+</div>
            <div class="label">{isZh ? '支持的提供商' : 'Supported Providers'}</div>
          </div>
          <div class="stat">
            <div class="number">2</div>
            <div class="label">{isZh ? '官方运行时实现' : 'Official Runtimes'}</div>
          </div>
          <div class="stat">
            <div class="number">48k+</div>
            <div class="label">{isZh ? '文档字数' : 'Documentation Words'}</div>
          </div>
        </div>
      </section>

      <section class="resources">
        <h2>{isZh ? '快速链接' : 'Quick Links'}</h2>
        <ul class="link-list">
          <li><a href="https://github.com/hiddenpath/ai-protocol/tree/main/docs">📚 Protocol Documentation</a></li>
          <li><a href="https://github.com/hiddenpath/ai-protocol/tree/main/examples">💡 Example Configurations</a></li>
          <li><a href="https://github.com/hiddenpath/ai-protocol/blob/main/README.md">📖 Full README</a></li>
        </ul>
      </section>
    </main>

    <Footer locale={locale} />
  </body>
</html>
```

#### Step 2.1.2: 中文版

```bash
# 创建链接到英文版的简化中文首页
cat > src/pages/zh/protocol/index.astro << 'EOF'
---
// 中文版可以暂时重定向到英文版，或提供简单的介绍
import '../../../styles/global.css';
import SiteHeader from '../../../components/SiteHeader.astro';
import Footer from '../../../components/Footer.astro';

const locale = 'zh';
---

<html lang="zh-CN">
  <head>
    <title>AI-Protocol 规范 | ailib.info</title>
  </head>
  <body>
    <SiteHeader locale={locale} />
    <!-- ... 类似英文版但用中文 ... -->
    <Footer locale={locale} />
  </body>
</html>
EOF
```

---

### P2-2: 创建 Rust SDK 专区 (P2-RUST)

**步骤**:

```bash
# 创建目录结构
mkdir -p src/pages/rust
mkdir -p src/pages/zh/rust
```

```astro
---
// src/pages/rust/index.astro
import '../../styles/global.css';
import SiteHeader from '../../components/SiteHeader.astro';
import Footer from '../../components/Footer.astro';

const locale = 'en';
const isZh = false;
---

<html lang="en">
  <head>
    <title>ai-lib-rust | Rust AI SDK</title>
  </head>
  <body>
    <SiteHeader locale={locale} />

    <main class="rust-page">
      <section class="page-hero">
        <span class="version-badge">v0.6.6</span>
        <h1>ai-lib-rust</h1>
        <p class="subtitle">High-performance AI SDK for Rust</p>
        <p>
          Reference implementation of AI-Protocol with 14 architectural layers.
          Built for systems programming, embedded devices, and infrastructure teams.
        </p>

        <div class="cta-group">
          <a href="https://github.com/hiddenpath/ai-lib-rust" target="_blank" class="btn primary">
            GitHub Repository
          </a>
          <a href="/rust/quick-start/" class="btn secondary">
            Quick Start
          </a>
        </div>
      </section>

      <section class="architecture">
        <h2>14-Layer Architecture</h2>
        <div class="layers-grid">
          <div class="layer">Protocol layer</div>
          <div class="layer">Transport layer</div>
          <div class="layer">Pipeline layer</div>
          <div class="layer">Client layer</div>
          <div class="layer">Resilience layer</div>
          <div class="layer">Telemetry layer</div>
          <!-- ... 更多层 ... -->
        </div>
      </section>

      <section class="features">
        <h2>Why Rust?</h2>
        <ul>
          <li>✅ <strong>Performance</strong>: &lt;1ms overhead, minimal memory footprint</li>
          <li>✅ <strong>Type Safety</strong>: Compile-time guarantees prevent runtime errors</li>
          <li>✅ <strong>Reliability</strong>: Built-in retry, rate limiting, circuit breaker</li>
          <li>✅ <strong>Enterprise Features</strong>: Hot-reload config, plugin system</li>
        </ul>
      </section>

      <section class="quickstart">
        <h2>Quick Install</h2>

        <pre class="code-block"><code>// Cargo.toml
[dependencies]
ai-lib = "0.6.6"
tokio = { version = "1", features = ["full"] }</code></pre>
      </section>

      <section class="resources">
        <h2>Documentation</h2>
        <ul class="link-list">
          <li><a href="https://github.com/hiddenpath/ai-lib-rust">Full README</a></li>
          <li><a href="https://crates.io/crates/ai-lib">Crates.io</a></li>
          <li><a href="/rust/features/">Feature Guide</a></li>
        </ul>
      </section>
    </main>

    <Footer locale={locale} />
  </body>
</html>
```

---

### P2-3: 创建 Python SDK 专区 (P2-PYTHON)

**步骤**:

```bash
# 创建目录结构
mkdir -p src/pages/python
mkdir -p src/pages/zh/python
```

```astro
---
// src/pages/python/index.astro
import '../../styles/global.css';
import SiteHeader from '../../components/SiteHeader.astro';
import Footer from '../../components/Footer.astro';

const locale = 'en';
const isZh = false;
---

<html lang="en">
  <head>
    <title>ai-lib-python | Python AI SDK</title>
  </head>
  <body>
    <SiteHeader locale={locale} />

    <main class="python-page">
      <section class="page-hero">
        <span class="version-badge">v0.5.0 Published</span>
        <span class="pypi-badge">PyPI</span>
        <h1>ai-lib-python</h1>
        <p class="subtitle">Official Python Runtime for AI-Protocol</p>
        <p>
          Production-ready Python implementation with 95% feature parity.
          Ideal for ML/data science teams, startups, and enterprise Python environments.
        </p>

        <div class="cta-group">
          <a href="https://pypi.org/project/ai-lib-python/" target="_blank" class="btn primary">
            PyPI Package
          </a>
          <a href="https://github.com/hiddenpath/ai-lib-python" target="_blank" class="btn secondary">
            GitHub Repository
          </a>
          <a href="/python/quick-start/" class="btn outline">
            Quick Start
          </a>
        </div>
      </section>

      <section class="features">
        <h2>Why Python?</h2>
        <ul>
          <li>✅ <strong>Type-Safe</strong>: Pydantic v2 for runtime type checking</li>
          <li>✅ <strong>Async First</strong>: Full async/await support with httpx</li>
          <li>✅ <strong>Easy Integration</strong>: Works with FastAPI, Jupyter, ML pipelines</li>
          <li>✅ <strong>Model Routing</strong>: 6 routing strategies built-in</li>
          <li>✅ <strong>Caching & Telemetry</strong>: OpenTelemetry ready, plugin support</li>
        </ul>
      </section>

      <section class="quickstart">
        <h2>Quick Install</h2>

        <pre class="code-block"><code># Basic installation
pip install ai-lib-python

# With all features
pip install ai-lib-python[full]</code></pre>
      </section>

      <section class="stats">
        <h2>Feature Parity</h2>
        <div class="comparison">
          <div class="bar-label">Rust SDK</div>
          <div class="bar-container">
            <div class="bar rust" style="width: 100%"></div>
          </div>

          <div class="bar-label">Python SDK</div>
          <div class="bar-container">
            <div class="bar python" style="width: 95%"></div>
          </div>
        </div>
      </section>

      <section class="resources">
        <h2>Documentation</h2>
        <ul class="link-list">
          <li><a href="https://github.com/hiddenpath/ai-lib-python">Full README on GitHub</a></li>
          <li><a href="https://pypi.org/project/ai-lib-python/">PyPI Package Page</a></li>
          <li><a href="/python/features/">Feature Guide</a></li>
        </ul>
      </section>
    </main>

    <Footer locale={locale} />
  </body>
</html>
```

---

## Phase 3: 内容补充与清理 (P3)

### P3-1: 清除过时内容 (P3-CLEAN)

**目标**: 删除所有 ai-lib-pro 引用和过时的企业版内容

**步骤**:

```bash
# 1. 查找并删除 enterprise 页面
find src/pages -name "*enterprise*" -type f

# 如果找到，删除这些文件
rm -f src/pages/enterprise.astro
rm -f src/pages/zh/enterprise.astro

# 2. 查找 EnterpriseFeatures 组件
find src/components -name "*enterprise*" -type f

# 删除或重构相关组件

# 3. 搜索并移除 ai-lib-pro 引用
grep -r "ai-lib-pro" src/
# 删除或替换这些引用

# 4. 删除过时的企业版 README 内容
rm -f src/content/docs/enterprise-pro.md
rm -f src/content/docs/enterprise-pro.zh.md
rm -f src/content/docs/enterprise-*.md
```

---

### P3-2: 更新 Provider Grid (P3-PROVIDERS)

**目标**: 扩展 Provider 列表到 30+，并添加分类

**步骤**:

#### 3.2.1: 更新 Providers 组件

```astro
---
// src/components/Providers.astro 或创建新页面

const providersByCategory = {
  global: [
    { name: 'OpenAI', icon: '/icons/openai.svg', link: 'https://openai.com' },
    { name: 'Anthropic', icon: '/icons/anthropic.svg', link: 'https://anthropic.com' },
    { name: 'Groq', icon: '/icons/groq.svg', link: 'https://groq.com' },
    { name: 'Gemini', icon: '/icons/gemini.svg', link: 'https://gemini.com' },
    { name: 'Mistral', icon: '/icons/mistral.svg', link: 'https://mistral.ai' },
    { name: 'Cohere', icon: '/icons/cohere.svg', link: 'https://cohere.com' },
    // ... 15+ 全球提供商
  ],

  china: [
    { name: '通义千问', icon: '/icons/qwen.svg', link: 'https://tongyi.aliyun.com' },
    { name: '智谱', icon: '/icons/zhipu.svg', link: 'https://zhipuai.cn' },
    { name: '百川', icon: '/icons/baichuan.svg', link: 'https://baichuan-ai.com' },
    { name: '月之暗面', icon: '/icons/kimi.svg', link: 'https://moonshot.cn' },
    { name: '腾讯混元', icon: '/icons/hunyuan.svg', link: 'https://hunyuan.tencent.com' },
    { name: '百度文心', icon: '/icons/baidu.svg', link: 'https://wenxin.baidu.com' },
    // ... 10+ 中国区提供商
  ],

  local: [
    { name: 'Ollama', icon: '/icons/ollama.svg', link: 'https://ollama.com' },
    { name: 'vLLM', icon: '/icons/vllm.svg', link: 'https://vllm.ai' },
    { name: 'LM Studio', icon: '/icons/lmstudio.svg', link: 'https://lmstudio.ai' },
    // ... 本地托管选项
  ]
};
---

<section class="providers-section">
  <h2>Supported Providers</h2>
  <p class="subtitle">30+ AI providers, worldwide coverage</p>

  {Object.entries(providersByCategory).map(([category, providers]) => (
    <div class={`provider-category ${category}`}>
      <h3 class="category-title">
        {category === 'global' ? 'Global Providers 🌍' :
         category === 'china' ? 'China Region 🇨🇳' :
         'Local & Custom 🏠'}
      </h3>

      <div class="provider-grid">
        {providers.map(provider => (
          <a href={provider.link} target="_blank" class="provider-card">
            <img src={provider.icon} alt={provider.name} />
            <span>{provider.name}</span>
          </a>
        ))}
      </div>
    </div>
  ))}
</section>
```

---

## Phase 4: 文档整理 (P4)

### P4-1: 创建通用文档结构

```bash
# 确保文档目录存在
mkdir -p src/content/docs/introduction
mkdir -p src/content/docs/guides

# 创建新的通用文档文件
touch src/content/docs/introduction/architecture.md
touch src/content/docs/guides/runtime-selection.md
```

**architectural.md 示例**:
```markdown
---
title: Ecosystem Architecture
group: introduction
order: 1
---

# AI-Protocol Ecosystem Architecture

## Layered Design

```
┌────────────────────────────────────┐
│         Application Layer          │
├────────────────────────────────────┤
│   Runtime Implementations         │
│   ├─ ai-lib-rust                  │
│   └─ ai-lib-python                │
├────────────────────────────────────┤
│         AI-Protocol                │
│   (Specification)                 │
├────────────────────────────────────┤
│   AI Providers (30+)              │
└────────────────────────────────────┘
```

## Core Principles

1. **Protocol-Driven**: All interactions defined by the protocol spec
2. **Multi-Runtime**: Multiple language implementations
3. **Provider Agnostic**: No hard-coded provider logic
4. **Declarative Configuration**: YAML/JSON manifests

...
```

---

## Phase 5: 审查与测试 (P5)

### P5-1: 本地完整测试

```bash
# 1. 启动开发服务器
npm run dev

# 2. 测试所有页面
# - http://localhost:4321/
# - http://localhost:4321/protocol/
# - http://localhost:4321/rust/
# - http://localhost:4321/python/
# - http://localhost:4321/zh/
# - http://localhost:4321/zh/protocol/

# 3. 测试导航链接
# 点击所有导航项，确保链接正确

# 4. 测试响应式布局
# 在浏览器开发者工具中测试不同屏幕尺寸

# 5. 检查控制台错误
# 打开浏览器开发者工具，检查 JavaScript 错误
```

### P5-2: 性能检查

```bash
# 构建生产版本
npm run build

# 检查构建产物
# dist/ 目录下应该生成所有页面

# 查看构建输出
# 确保没有警告或错误
```

### P5-3: 跨浏览器测试

- Chrome ✅
- Firefox ✅
- Safari ✅
- Edge ✅

### P5-4: 代码审查清单

```bash
# 1. 检查是否移除了所有 ai-lib-pro 引用
grep -r "ai-lib-pro" src/
# 应该返回空

# 2. 检查是否移除了所有 enterprise 相关页面
find src/pages -name "*enterprise*"
# 应该返回空

# 3. 检查所有外部链接是否正确
grep -r "github.com" src/pages/
# 确保指向正确的仓库

# 4. 检查版本号是否正确
grep -r "v0\.4\.0" src/
grep -r "v0\.5\.0" src/
grep -r "v0\.6\.6" src/

# 5. 运行代码格式化检查
npm run format:check
```

---

## 📝 最终审查要点

完成后，确认以下所有项都已完成：

### 功能完整性
- [x] 导航栏包含三项目链接
- [x] 首页显示三项目卡片
- [x] Protocol、Rust、Python 专区页已创建
- [x] 所有链接指向正确的仓库和文档
- [x] Provider 列表扩展到 30+

### 内容准确性
- [x] 版本号正确
- [x] 无 ai-lib-pro 引用
- [x] 无过时企业版内容
- [x] 描述准确反映项目现状
- [x] 双语内容一致

### 技术质量
- [x] 无控制台错误
- [x] 响应式布局正确
- [x] 性能指标达标（LCP < 1.5s）
- [x] 代码格式正确
- [x] 无死链

### 用户体验
- [x] 导航逻辑清晰
- [x] 信息层级合理
- [x] 语言切换正确
- [x] 移动端友好

---

## 🔖 提交与推送

完成后，推送到远程：

```bash
# 提交所有更改
git add .
git commit -m "refactor: rewrite ailib.info for new ecosystem

- Restructure as ecosystem portal for AI-Protocol, ai-lib-rust, ai-lib-python
- Add new pages: /protocol/, /rust/, /python/
- Update Hero to ecosystem landing
- Remove deprecated ai-lib-pro content
- Update provider grid to 30+ providers
- Add runtime comparison and selection guide"

# 推送到远程
git push origin refactor/ecosystem-rewrite
```

---

**文档版本**: v1.0
**创建日期**: 2025-02-07
**状态**: 🟡 实施阶段
