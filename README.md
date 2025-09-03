# ai-lib Website

This is the minimal marketing & info site for **ai-lib** (Unified Multi-Provider AI SDK for Rust).

## Features (MVP)
- English + Simplified Chinese landing pages
- Core value props
- Quick Start installation snippet
- Supported providers grid
- Performance snapshot (from main README)
- Simplified architecture diagram (text block)
- Roadmap snapshot
- Early access / support inquiry form (Formspree placeholder)
- FAQ
- Cloudflare Web Analytics placeholder

## Local Development

```bash
npm install
npm run dev
```

Open http://localhost:4321

## Build

```bash
npm run build
```

Output will be in `dist/` (static export).

## Deploy (Vercel)

1. Push repository to GitHub.
2. In Vercel: New Project → Import.
3. Framework auto-detected (Astro).
4. Build Command: `astro build` (default), Output: `dist`.
5. After deploy: add domain `ailib.rs` in Project Settings → Domains.

## Domain (ailib.rs)

For apex domain (root):
- Add an A record:
  - Host: `@`
  - Value: `76.76.21.21`
  - TTL: auto/3600

Optional `www`:
- CNAME: `www` → `cname.vercel-dns.com`.

Then verify in Vercel.

## Form Integration

Replace placeholder:

```html
<form method="POST" action="https://formspree.io/f/your-form-id">
```

with the Formspree form ID you create.

## Next Steps (Suggested)

- Add blog: create `src/pages/blog/` and markdown posts.
- Add provider logos as actual SVG icons.
- Automate performance benchmark JSON generation.
- Add `/docs` or link to existing repository docs.
- Add basic sitemap.xml (Astro integration or manual).
- Consider Tailwind if design complexity grows.

## Analytics

Uncomment Cloudflare snippet in `<head>` sections and add token if you enable Cloudflare Web Analytics.

## i18n Strategy

Currently manual duplication:
- `/src/pages/index.astro` (en)
- `/src/pages/zh/index.astro` (zh)

If content grows, migrate to an Astro i18n or content collections approach.

## License

Follow main project (MIT / Apache-2.0). Content here can mirror same licensing.

---