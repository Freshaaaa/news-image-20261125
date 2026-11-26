// main.ts — news-image-20261125 poster entrypoint.
// Copies the rendered entry.png into the grader's output directory.
// Node 22, standard library only. No network, no dependencies.
//
// The grader runs `node /bot/main.ts` with /bot READ-ONLY and a writable
// /output (MAKEFUN_OUTPUT_DIR=/output). The output directory MUST come from
// MAKEFUN_OUTPUT_DIR (fallback "/output") — writing to a path under /bot
// fails because /bot is read-only (that was the round-3 run_completes
// rejection: the old main.ts wrote to /bot/output and exited 1).
// Run locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = new URL("./entry.png", import.meta.url);
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);
console.log("entry.png -> " + dst);
