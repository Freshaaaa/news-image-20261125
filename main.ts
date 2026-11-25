// main.ts — entry point for the news-image-20261125 poster.
// Copies the rendered entry.png into the output directory.
// Node 22, standard library only. No network, no extra dependencies.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.argv[2] ?? join(here, "output");
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
console.log("entry.png -> " + join(outDir, "entry.png"));
