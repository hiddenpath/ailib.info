/** @type {import('tailwindcss').Config} */
export default {
    content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
    theme: {
        extend: {
            colors: {
                // AI-Protocol Ecosystem color palette
                'deep-space': '#0a0c10',
                'midnight': '#0d1117',
                'slate': {
                    850: '#1e293b',
                    950: '#0f172a',
                },
                'accent': {
                    DEFAULT: '#3b82f6',
                    light: '#60a5fa',
                    dark: '#2563eb',
                },
                'rust': '#f97316',
                'python': '#22c55e',
                'protocol': '#8b5cf6',
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
                mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
            },
        },
    },
    plugins: [],
}
