import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://ailib.info',
  integrations: [
    starlight({
      title: 'AI-Lib',
      logo: {
        src: './src/assets/logo.svg',
      },
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/hiddenpath' },
      ],
      editLink: {
        baseUrl: 'https://github.com/hiddenpath/ailib.info/edit/main/',
      },
      sidebar: [
        {
          label: 'Getting Started',
          translations: { 'zh-CN': '快速入门' },
          items: [
            { label: 'Introduction', slug: 'intro' },
            { label: 'Quick Start', slug: 'quickstart' },
            { label: 'Ecosystem Architecture', slug: 'ecosystem' },
          ],
        },
        {
          label: 'AI-Protocol',
          translations: { 'zh-CN': 'AI-Protocol 协议' },
          items: [
            { label: 'Overview', slug: 'protocol/overview' },
            { label: 'Specification', slug: 'protocol/spec' },
            { label: 'Provider Manifests', slug: 'protocol/providers' },
            { label: 'Model Registry', slug: 'protocol/models' },
            { label: 'Contributing Providers', slug: 'protocol/contributing' },
          ],
        },
        {
          label: 'Rust SDK',
          translations: { 'zh-CN': 'Rust SDK' },
          items: [
            { label: 'Overview', slug: 'rust/overview' },
            { label: 'Quick Start', slug: 'rust/quickstart' },
            { label: 'AiClient API', slug: 'rust/client' },
            { label: 'Streaming Pipeline', slug: 'rust/streaming' },
            { label: 'Resilience', slug: 'rust/resilience' },
            { label: 'Advanced Features', slug: 'rust/advanced' },
          ],
        },
        {
          label: 'Python SDK',
          translations: { 'zh-CN': 'Python SDK' },
          items: [
            { label: 'Overview', slug: 'python/overview' },
            { label: 'Quick Start', slug: 'python/quickstart' },
            { label: 'AiClient API', slug: 'python/client' },
            { label: 'Streaming Pipeline', slug: 'python/streaming' },
            { label: 'Resilience', slug: 'python/resilience' },
            { label: 'Advanced Features', slug: 'python/advanced' },
          ],
        },
        {
          label: 'Developer Guides',
          translations: { 'zh-CN': '开发者指南' },
          items: [
            { label: 'Chat Completions', slug: 'guides/chat' },
            { label: 'Function Calling', slug: 'guides/tools' },
            { label: 'Reasoning Models', slug: 'guides/reasoning' },
            { label: 'Multimodal', slug: 'guides/multimodal' },
            { label: 'Observability', slug: 'guides/observability' },
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
      },
    }),
    tailwind({
      applyBaseStyles: false,
    }),
  ],
});
