import { fileURLToPath } from 'node:url'
import { readFileSync } from 'node:fs'
import path from 'node:path'
import { defineConfig, type Plugin } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { viteSingleFile } from 'vite-plugin-singlefile'

/**
 * Standalone build: route every import of api/client to the in-browser
 * engine, so the same screens run with no server behind them.
 */
function localApi(): Plugin {
  const local = path.resolve(__dirname, 'src/local/localClient.ts')
  return {
    name: 'local-api',
    enforce: 'pre',
    resolveId(source, importer) {
      if (!importer || importer.includes(`${path.sep}local${path.sep}`)) return null
      if (/(^|\/)api\/client(\.ts)?$/.test(source)) return local
      return null
    },
  }
}

/**
 * Embed the 32 px icon so the page, and customer dashboards saved from it as
 * a single file, carry their own tab icon. Larger icons (192 px, apple touch)
 * point at the website's files beside /analyser/. Also names the tab.
 */
function inlineIcon(): Plugin {
  const png = readFileSync(fileURLToPath(new URL('../site/images/brand/favicon-32.png', import.meta.url))).toString('base64')
  return {
    name: 'inline-icon',
    transformIndexHtml: (html) => html
      .replace(/<link rel="icon" type="image\/png" sizes="32x32"[^>]*>/, `<link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,${png}" />`)
      .replace(/<title>[^<]*<\/title>/, '<title>Half-hourly electricity analyser | Half Hourly Insights</title>'),
  }
}

export default defineConfig(({ mode }) => {
  // `npm run build` makes the analyser as one self-contained HTML page for
  // the website's /analyser/, no server and no install.
  if (mode === 'standalone') {
    return {
      base: './',
      plugins: [localApi(), inlineIcon(), react(), tailwindcss(), viteSingleFile()],
      build: { outDir: 'dist-site', chunkSizeWarningLimit: 5000 },
    }
  }

  return {
    // GitHub Pages serves from /Solardataprofile/ in production
    base: process.env.NODE_ENV === 'production' ? '/Solardataprofile/' : '/',
    plugins: [react(), tailwindcss()],
    server: {
      proxy: {
        '/api': 'http://localhost:8000',
        '/healthz': 'http://localhost:8000',
      },
    },
  }
})
