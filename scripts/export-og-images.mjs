#!/usr/bin/env node
/**
 * Export OG image SVGs to PNG for social sharing (Facebook, Twitter, etc. don't support SVG).
 * Run from project root: node scripts/export-og-images.mjs
 */
import { Resvg } from '@resvg/resvg-js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const publicDir = path.join(__dirname, '..', 'public');

// Inline ailib_icon.png as base64 so Resvg can render without path resolution
const iconPath = path.join(publicDir, 'ailib_icon.png');
let iconDataUri = '';
if (fs.existsSync(iconPath)) {
  const iconBuf = fs.readFileSync(iconPath);
  iconDataUri = 'data:image/png;base64,' + iconBuf.toString('base64');
}

const svgFiles = [
  { svg: 'ogimage.svg', png: 'og-image-zh.png' },
  { svg: 'ogimage-en.svg', png: 'og-image-en.png' },
  { svg: 'ogimage-ja.svg', png: 'og-image-ja.png' },
  { svg: 'ogimage-es.svg', png: 'og-image-es.png' },
];

for (const { svg, png } of svgFiles) {
  const svgPath = path.join(publicDir, svg);
  const pngPath = path.join(publicDir, png);
  if (!fs.existsSync(svgPath)) {
    console.warn(`Skip ${svg}: not found`);
    continue;
  }
  let svgContent = fs.readFileSync(path.join(publicDir, svg), 'utf-8');
  // Strip control characters and normalize line endings for XML parsing
  svgContent = svgContent.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
  svgContent = svgContent.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F-\u009F]/g, '');
  if (iconDataUri) {
    svgContent = svgContent.replace(/href="ailib_icon\.png"/g, `href="${iconDataUri}"`);
  }
  const resvg = new Resvg(svgContent, {
    fitTo: { mode: 'width', value: 1200 },
  });
  const pngData = resvg.render();
  const pngBuffer = pngData.asPng();
  fs.writeFileSync(pngPath, pngBuffer);
  console.log(`Exported ${svg} -> ${png}`);
}
