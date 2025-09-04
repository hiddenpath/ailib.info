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
<form method="POST" action="https://formspree.io/f/your-form-id"></form>
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

## Continuous Integration (GitHub Actions)

This repository includes a GitHub Actions workflow that:

1. Runs on pushes to `main` and on all pull requests.
2. Caches `~/.npm` for faster builds.
3. Installs dependencies with `npm ci`.
4. Checks formatting (`npm run format:check`).
5. Builds the static site (`npm run build`).
6. (Optional) Uploads the `dist/` folder as an artifact for PR preview.

If you deploy with **Vercel** connected to GitHub, Vercel will build & deploy separately; this CI build is a quality gate (fast failure feedback). You can safely disable the build step in Vercel if you later introduce a multi-step pipeline, but default settings are fine.

### Local parity

The CI uses:

```bash
npm ci
npm run format:check
npm run build
```

Ensure your local Node.js version is >= the version declared in your `.nvmrc` (add one if needed) or engines field if added later.

## Automated Deployment (Vercel)

When the repo is linked to Vercel:

- Every push to `main` triggers a Production deployment.
- Every PR gets a Preview URL (great for design/content review).
- Build command: `astro build`
- Output dir: `dist`

### Environment Variables

Currently none required. If later you add analytics tokens or form IDs, set them in Vercel Project Settings → Environment Variables, then reference via `import.meta.env`. Re-run deployments after adding them.

### Recommended Hardening

- Add a `NODE_VERSION` or `engines` constraint to ensure consistent runtime.
- Add a `sitemap.xml` generation step (Astro integration) for SEO.
- Add a `robots.txt` rule update if you introduce staging environments.

## Artifacts

The CI workflow uploads `site-dist` artifact for inspection. Download from the workflow run page if you need to diff generated HTML without pulling locally.

---
