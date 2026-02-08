import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  site: 'https://ailib.info',
  integrations: [
    starlight({
      title: 'AI-Protocol Ecosystem',
      logo: {
        src: './src/assets/logo.svg',
      },
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/hiddenpath/ai-protocol' },
      ],
      editLink: {
        baseUrl: 'https://github.com/hiddenpath/ailib.info/edit/main/',
      },
      sidebar: [
        {
          label: 'Start Here',
          translations: { 'zh-CN': '快速开始' },
          items: [
            { label: 'Introduction', slug: 'intro' },
            { label: 'Getting Started', slug: 'getting-started' },
            { label: 'Ecosystem Architecture', slug: 'ecosystem-architecture' },
          ],
        },
        {
          label: 'Core Concepts',
          translations: { 'zh-CN': '核心概念' },
          items: [
            { label: 'Concepts', slug: 'concepts' },
            { label: 'Architecture', slug: 'architecture' },
            { label: 'Providers', slug: 'providers' },
          ],
        },
        {
          label: 'Developer Guides',
          translations: { 'zh-CN': '开发者指南' },
          items: [
            { label: 'Chat Completions', slug: 'chat' },
            { label: 'Function Calling', slug: 'functions' },
            { label: 'Reasoning Models', slug: 'reasoning-models' },
            { label: 'Observability', slug: 'observability' },
          ],
        },
        {
          label: 'Reliability',
          translations: { 'zh-CN': '可靠性' },
          items: [
            { label: 'Overview', slug: 'reliability-overview' },
            { label: 'Retry Strategies', slug: 'reliability-retry' },
            { label: 'Fallback', slug: 'reliability-fallback' },
            { label: 'Routing', slug: 'reliability-routing' },
            { label: 'Circuit Breaker', slug: 'reliability-circuit' },
          ],
        },
        {
          label: 'Advanced',
          translations: { 'zh-CN': '高级主题' },
          items: [
            { label: 'Recipes', slug: 'recipes' },
            { label: 'Import Patterns', slug: 'import-patterns' },
            { label: 'Extension', slug: 'extension' },
            { label: 'Runtime Selection', slug: 'runtime-selection' },
          ],
        },
        {
          label: 'Release Notes',
          translations: { 'zh-CN': '版本发布' },
          items: [
            { label: 'v0.4.0', slug: 'news-040' },
            { label: 'v0.3.4', slug: 'news-034' },
            { label: 'v0.3.3', slug: 'news-033' },
            { label: 'v0.3.0', slug: 'news-030' },
            { label: 'Upgrade to v0.4.0', slug: 'upgrade-040' },
          ],
        },
      ],
      customCss: [
        './src/styles/custom.css',
      ],
      defaultLocale: 'root',
      locales: {
        root: {
          label: 'English',
          lang: 'en',
        },
        zh: {
          label: '简体中文',
          lang: 'zh-CN',
        },
      },
    }),
    tailwind({
      applyBaseStyles: false,
    }),
  ],
});
