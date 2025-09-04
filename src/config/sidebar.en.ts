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
    group: 'Overview',
    items: [
      { title: 'Introduction', path: '/docs/intro' },
      { title: 'Getting Started', path: '/docs/getting-started' },
      { title: 'Supported Providers', path: '/docs/providers' },
      { title: 'Architecture', path: '/docs/architecture' },
      { title: 'FAQ', path: '/docs/faq' },
    ],
  },
  {
    group: 'Developer Guide',
    items: [
      { title: 'Core Concepts', path: '/docs/concepts' },
      { title: 'Chat & Streaming', path: '/docs/chat', status: 'stable' },
      { title: 'Functions & Tools', path: '/docs/functions', status: 'stable' },
      { title: 'Reliability Overview', path: '/docs/reliability', status: 'stable' },
      { title: 'Retry', path: '/docs/reliability-retry', status: 'stable' },
      { title: 'Fallback Chains', path: '/docs/reliability-fallback', status: 'stable' },
      { title: 'Race / Hedging', path: '/docs/reliability-race', status: 'stable' },
      { title: 'Routing', path: '/docs/reliability-routing', status: 'stable' },
      { title: 'Rate Limiting', path: '/docs/reliability-rate', status: 'partial' },
      { title: 'Circuit Breaker', path: '/docs/reliability-circuit', status: 'partial' },
      { title: 'Observability', path: '/docs/observability', status: 'planned' },
      { title: 'Extending the SDK', path: '/docs/extension', status: 'stable' },
    ],
  },
  {
    group: 'Recipes',
    items: [{ title: 'Recipes Overview', path: '/docs/recipes', status: 'planned' }],
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
      { title: 'API (docs.rs)', external: 'https://docs.rs/ai-lib/latest/ai_lib/' },
      { title: 'Changelog', external: 'https://github.com/hiddenpath/ai-lib/releases' },
      { title: 'Roadmap', external: 'https://github.com/hiddenpath/ai-lib#roadmap' },
    ],
  },
];

export default sidebar;
