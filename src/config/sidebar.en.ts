export interface SidebarItem {
  title: string;
  path?: string;
  external?: string;
  status?: 'stable' | 'partial' | 'planned';
}
export interface SidebarGroup {
  group: string;
  items: SidebarItem[];
}

const sidebar: SidebarGroup[] = [
  {
    group: 'Getting Started',
    items: [
      { title: 'Introduction', path: '/docs/intro' },
      { title: 'Quick Start', path: '/docs/getting-started' },
      { title: 'Core Concepts', path: '/docs/concepts' },
      { title: 'Supported Providers', path: '/docs/providers' },
    ],
  },
  {
    group: 'Core Features',
    items: [
      { title: 'Chat & Streaming', path: '/docs/chat', status: 'stable' },
      { title: 'Functions & Tools', path: '/docs/functions', status: 'stable' },
      { title: 'Observability', path: '/docs/observability', status: 'stable' },
    ],
  },
  {
    group: 'Reliability & Performance',
    items: [
      { title: 'Reliability Overview', path: '/docs/reliability-overview', status: 'stable' },
      { title: 'Retry Strategies', path: '/docs/reliability-retry', status: 'stable' },
      { title: 'Fallback Chains', path: '/docs/reliability-fallback', status: 'stable' },
      { title: 'Rate Limiting', path: '/docs/reliability-rate', status: 'partial' },
      { title: 'Circuit Breaker', path: '/docs/reliability-circuit', status: 'partial' },
      { title: 'Race / Hedging', path: '/docs/reliability-race', status: 'stable' },
      { title: 'Intelligent Routing', path: '/docs/reliability-routing', status: 'stable' },
    ],
  },
  {
    group: 'Advanced Topics',
    items: [
      { title: 'Architecture', path: '/docs/architecture' },
      { title: 'Advanced Examples', path: '/docs/advanced-examples' },
      { title: 'Code Recipes', path: '/docs/recipes', status: 'stable' },
      { title: 'Extending the SDK', path: '/docs/extension', status: 'stable' },
    ],
  },
  {
    group: 'Enterprise',
    items: [
      { title: 'Why Ailib', path: '/docs/enterprise-overview' },
      { title: 'Deployment & Security', path: '/docs/enterprise-deployment', status: 'partial' },
      { title: 'Support & Contact', path: '/docs/enterprise-support' },
    ],
  },
  {
    group: 'Reference',
    items: [
      { title: 'API Documentation', external: 'https://docs.rs/ai-lib/latest/ai_lib/' },
      { title: 'FAQ', path: '/docs/faq' },
      { title: 'Changelog', external: 'https://github.com/hiddenpath/ai-lib/releases' },
      { title: 'Roadmap', external: 'https://github.com/hiddenpath/ai-lib#roadmap' },
    ],
  },
];

export default sidebar;
