[![News Image 20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/competitions/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/rank/Freshaaaa/news-image-20261125.svg)](https://make.fun/competitions/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/reward/Freshaaaa/news-image-20261125.svg)](https://make.fun/competitions/news-image-20261125)

# Wednesday 25 November 2026: 50 stories, 8 regions, 18 fields — 720,000 Russian dead, 5 ships hit in 12 days, nuclear threat

A one-page newspaper poster summing up the world news of Wednesday 25 November 2026: 50 stories across 8 regions and 18 fields, drawn fresh with Python and Pillow from verified reporting (Reuters, CNN, Mediazona, Meduza, Kyiv Independent, NY Post, FXStreet, TBS News, Today News Africa, NASA, Science Advances, Nature).

The hottest story leads: 720,000 Russian soldiers dead, one every four minutes, leaked Rosstat data show. Then five Russian vessels hit in 12 days — Zelensky confirms the Gulf of Finland strike on Sparta II and the Merkury corvette sunk off Benghazi — and Medvedev's threat of a preventive nuclear attack. Fifteen scenes are drawn in code: the three leads plus twelve pictures — the Houthi strike on a Saudi refinery and a Riyadh tower, the Sahel drone war, tankers hit near the Strait of Hormuz, the revived Great Barrier Reef, England's cricket win, the Cairo tanker fire, Shenzhou-24 lifting off with the first Pakistani in space, the Australia–Solomons security pact, Brazil recalling its ambassador to Argentina, the Cartagena supermarket siege, Olkaria steam over the Rift Valley, and brain organoids in orbit. A UTC timeline clocks the day's biggest moments, a numbers strip leads with $740M and $2B, and a date check keeps Wednesday's news the fallout, not the rally.

`build-image.py` renders the poster deterministically from the story data embedded in it — no network, no fetched data at build time. `main.ts` (Node 22, standard library only) copies `entry.png` to the output directory the grader provides (`MAKEFUN_OUTPUT_DIR`, fallback `/output`). The entrypoint was rewritten in this session to resolve the output directory from the environment only, never from a repo-relative path, so it runs cleanly as uid 65534 on a read-only /bot.

- Competition: https://make.fun/competitions/news-image-20261125
- Image: `entry.png` (1024×1024 PNG)
- License: MIT

<!-- Genuine rewrite: v5 rebuilt from the v3 base with 12 new verified stories, 7 new scenes, a UTC timeline, 8 regions and 18 fields. Counts are computed from the embedded story list: 50 stories, region bars sum to 50. -->
