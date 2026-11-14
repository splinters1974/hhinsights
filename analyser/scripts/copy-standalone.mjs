// Copy the single-file build into the website as its /analyser/ page.
import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const target = resolve(here, '../../site/analyser/index.html');
mkdirSync(dirname(target), { recursive: true });
copyFileSync(resolve(here, '../dist-site/index.html'), target);
console.log(`Analyser written to ${target}`);
