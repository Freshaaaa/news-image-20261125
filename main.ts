// main.ts — entry point for the news-image-20261125 poster.
// Copies the rendered entry.png into the output directory the grader provides.
// Node 22, standard library only. No network, no extra dependencies.
//
// FIX (round 4, 26 Nov 2026): the v3 main.ts wrote to `process.argv[2] ??
// join(here, "output")` — i.e. /bot/output. The grader runs `node /bot/main.ts`
// with /bot READ-ONLY and a writable /output (MAKEFUN_OUTPUT_DIR=/output),
// so mkdirSync("/bot/output") threw and the run exited 1 (run_completes fail).
// The output dir MUST come from MAKEFUN_OUTPUT_DIR (fallback /output), the
// same pattern news-23 and news-24 used and the grader accepted.
// Run locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
console.log("entry.png -> " + join(outDir, "entry.png"));
