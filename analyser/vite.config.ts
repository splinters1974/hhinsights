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
 * The page has no favicon.svg beside it: inline the bar mark instead, and
 * give the tab the product name.
 */
function inlineIcon(): Plugin {
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 34 34'><rect x='3' y='15' width='5' height='10' rx='1' fill='%230065A4'/><rect x='10' y='9' width='5' height='16' rx='1' fill='%230065A4'/><rect x='17' y='3' width='5' height='22' rx='1' fill='%23F8C05D'/><rect x='24' y='12' width='5' height='13' rx='1' fill='%230065A4'/><rect x='1' y='26' width='32' height='3' rx='1.5' fill='%23063C55'/></svg>`
  return {
    name: 'inline-icon',
    transformIndexHtml: (html) => html
      .replace(/<link rel="icon"[^>]*>/, `<link rel="icon" href="data:image/svg+xml,${svg}" />`)
      .replace(/<title>[^<]*<\/title>/, '<title>Analyser | Half Hourly Insights</title>'),
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
