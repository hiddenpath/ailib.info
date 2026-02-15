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
      sidebar: [
        {
          label: 'Getting Started',
          translations: { 'zh-CN': '快速入门', 'ja': 'はじめに', 'es': 'Inicio' },
          items: [
            { label: 'Introduction', translations: { 'zh-CN': '简介', 'ja': 'はじめに', 'es': 'Introducción' }, slug: 'intro' },
            { label: 'Quick Start', translations: { 'zh-CN': '快速开始', 'ja': 'クイックスタート', 'es': 'Inicio rápido' }, slug: 'quickstart' },
            { label: 'Ecosystem Architecture', translations: { 'zh-CN': '生态系统架构', 'ja': 'エコシステムアーキテクチャ', 'es': 'Arquitectura del ecosistema' }, slug: 'ecosystem' },
          ],
        },
        {
          label: 'AI-Protocol',
          translations: { 'zh-CN': 'AI-Protocol 协议', 'ja': 'AI-Protocol 仕様', 'es': 'AI-Protocol' },
          items: [
            { label: 'Overview', translations: { 'zh-CN': '概览', 'ja': '概要', 'es': 'Visión general' }, slug: 'protocol/overview' },
            { label: 'Specification', translations: { 'zh-CN': '规范', 'ja': '仕様', 'es': 'Especificación' }, slug: 'protocol/spec' },
            { label: 'Provider Manifests', translations: { 'zh-CN': '供应商清单', 'ja': 'プロバイダーマニフェスト', 'es': 'Manifiestos de proveedores' }, slug: 'protocol/providers' },
            { label: 'Model Registry', translations: { 'zh-CN': '模型注册', 'ja': 'モデルレジストリ', 'es': 'Registro de modelos' }, slug: 'protocol/models' },
            { label: 'Contributing Providers', translations: { 'zh-CN': '贡献供应商', 'ja': 'プロバイダーの貢献', 'es': 'Contribuir proveedores' }, slug: 'protocol/contributing' },
          ],
        },
        {
          label: 'Rust SDK',
          translations: { 'zh-CN': 'Rust SDK', 'ja': 'Rust SDK', 'es': 'Rust SDK' },
          items: [
            { label: 'Overview', translations: { 'zh-CN': '概览', 'ja': '概要', 'es': 'Visión general' }, slug: 'rust/overview' },
            { label: 'Quick Start', translations: { 'zh-CN': '快速开始', 'ja': 'クイックスタート', 'es': 'Inicio rápido' }, slug: 'rust/quickstart' },
            { label: 'AiClient API', translations: { 'zh-CN': 'AiClient API', 'ja': 'AiClient API', 'es': 'AiClient API' }, slug: 'rust/client' },
            { label: 'Streaming Pipeline', translations: { 'zh-CN': '流式管道', 'ja': 'ストリーミングパイプライン', 'es': 'Pipeline de streaming' }, slug: 'rust/streaming' },
            { label: 'Resilience', translations: { 'zh-CN': '弹性机制', 'ja': 'レジリエンス', 'es': 'Resiliencia' }, slug: 'rust/resilience' },
            { label: 'Advanced Features', translations: { 'zh-CN': '高级功能', 'ja': '高度な機能', 'es': 'Funciones avanzadas' }, slug: 'rust/advanced' },
          ],
        },
        {
          label: 'Python SDK',
          translations: { 'zh-CN': 'Python SDK', 'ja': 'Python SDK', 'es': 'Python SDK' },
          items: [
            { label: 'Overview', translations: { 'zh-CN': '概览', 'ja': '概要', 'es': 'Visión general' }, slug: 'python/overview' },
            { label: 'Quick Start', translations: { 'zh-CN': '快速开始', 'ja': 'クイックスタート', 'es': 'Inicio rápido' }, slug: 'python/quickstart' },
            { label: 'AiClient API', translations: { 'zh-CN': 'AiClient API', 'ja': 'AiClient API', 'es': 'AiClient API' }, slug: 'python/client' },
            { label: 'Streaming Pipeline', translations: { 'zh-CN': '流式管道', 'ja': 'ストリーミングパイプライン', 'es': 'Pipeline de streaming' }, slug: 'python/streaming' },
            { label: 'Resilience', translations: { 'zh-CN': '弹性机制', 'ja': 'レジリエンス', 'es': 'Resiliencia' }, slug: 'python/resilience' },
            { label: 'Advanced Features', translations: { 'zh-CN': '高级功能', 'ja': '高度な機能', 'es': 'Funciones avanzadas' }, slug: 'python/advanced' },
          ],
        },
        {
          label: 'Developer Guides',
          translations: { 'zh-CN': '开发者指南', 'ja': '開発者ガイド', 'es': 'Guías para desarrolladores' },
          items: [
            { label: 'Chat Completions', translations: { 'zh-CN': '对话补全', 'ja': 'チャット補完', 'es': 'Chat Completions' }, slug: 'guides/chat' },
            { label: 'Function Calling', translations: { 'zh-CN': '函数调用', 'ja': '関数呼び出し', 'es': 'Llamada de funciones' }, slug: 'guides/tools' },
            { label: 'Reasoning Models', translations: { 'zh-CN': '推理模型', 'ja': '推論モデル', 'es': 'Modelos de razonamiento' }, slug: 'guides/reasoning' },
            { label: 'Multimodal', translations: { 'zh-CN': '多模态', 'ja': 'マルチモーダル', 'es': 'Multimodal' }, slug: 'guides/multimodal' },
            { label: 'Observability', translations: { 'zh-CN': '可观测性', 'ja': 'オブザーバビリティ', 'es': 'Observabilidad' }, slug: 'guides/observability' },
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
        'zh-cn': {
          label: '简体中文',
          lang: 'zh-CN',
        },
        ja: {
          label: '日本語',
          lang: 'ja',
        },
        es: {
          label: 'Español',
          lang: 'es',
        },
      },
    }),
    tailwind({
      applyBaseStyles: false,
    }),
  ],
});
