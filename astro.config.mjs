import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://ailib.info',
  output: 'static',
  markdown: {
    // 语法高亮方案：'shiki' 或 'prism'，二选一。这里用 shiki（更好看）。
    syntaxHighlight: 'shiki',
    shikiConfig: {
      theme: 'github-dark',
    },
    // 如需自定义 remark 插件：
    // remarkPlugins: [],
    // rehypePlugins: [],
  }
});