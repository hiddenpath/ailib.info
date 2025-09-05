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
    group: '快速开始',
    items: [
      { title: '介绍', path: '/zh/docs/intro' },
      { title: '快速开始', path: '/zh/docs/getting-started' },
      { title: '核心概念', path: '/zh/docs/concepts' },
      { title: '支持的提供商', path: '/zh/docs/providers' },
    ],
  },
  {
    group: '核心功能',
    items: [
      { title: '聊天与流式处理', path: '/zh/docs/chat', status: 'stable' },
      { title: '函数与工具', path: '/zh/docs/functions', status: 'stable' },
      { title: '可观测性', path: '/zh/docs/observability', status: 'stable' },
    ],
  },
  {
    group: '可靠性与性能',
    items: [
      { title: '可靠性概述', path: '/zh/docs/reliability-overview', status: 'stable' },
      { title: '重试策略', path: '/zh/docs/reliability-retry', status: 'stable' },
      { title: '回退链', path: '/zh/docs/reliability-fallback', status: 'stable' },
      { title: '速率限制', path: '/zh/docs/reliability-rate', status: 'partial' },
      { title: '熔断器', path: '/zh/docs/reliability-circuit', status: 'partial' },
      { title: '竞争/对冲', path: '/zh/docs/reliability-race', status: 'stable' },
      { title: '智能路由', path: '/zh/docs/reliability-routing', status: 'stable' },
    ],
  },
  {
    group: '高级主题',
    items: [
      { title: '架构', path: '/zh/docs/architecture' },
      { title: '高级示例', path: '/zh/docs/advanced-examples' },
      { title: '实用示例', path: '/zh/docs/recipes', status: 'stable' },
      { title: '扩展SDK', path: '/zh/docs/extension', status: 'stable' },
    ],
  },
  {
    group: '企业版',
    items: [
      { title: '为什么选择Ailib', path: '/zh/docs/enterprise-overview' },
      { title: '部署与安全', path: '/zh/docs/enterprise-deployment', status: 'partial' },
      { title: '支持与联系', path: '/zh/docs/enterprise-support' },
    ],
  },
  {
    group: '参考',
    items: [
      { title: 'API文档', external: 'https://docs.rs/ai-lib/latest/ai_lib/' },
      { title: '常见问题', path: '/zh/docs/faq' },
      { title: '更新日志', external: 'https://github.com/hiddenpath/ai-lib/releases' },
      { title: '路线图', external: 'https://github.com/hiddenpath/ai-lib#roadmap' },
    ],
  },
];

export default sidebar;
