[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Plowester1/news-image-20261117-poler-v2/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Plowester1/news-image-20261117-poler-v2/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

# The World in One Day — 17 November 2026

An entry in make.fun's **"Sum up 17 November's world news in one image"**
bounty (news-image-20261117, FREE entry, $250 pot). The program copies a
single 1024×1024 infographic to `/output/entry.png`: a light sky-blue
front page summing up Tuesday 17 November 2026's world news in eight
stories, each verified against multiple news sources for that day.

## The eight stories

1. **Asia (hero)** — Japan scrambles jets over Russian airspace: Tokyo
   protests after two suspected Russian aircraft cross its skies.
2. **Economy** — Japan's economy unexpectedly contracts: Q3 shrinks an
   annualized 0.1%, surprising markets.
3. **Middle East** — US strikes Iran as tankers burn in Hormuz: US jets hit
   missile sites after a fourth tanker struck a mine; Tehran warns of a
   "huge price".
4. **Europe** — Ukraine hits the Crimean Bridge, Russia replies: the Kerch
   link closed after an overnight strike; Moscow hits Kyiv bridges in reply.
5. **Tech** — US tightens AI chip export ban on China: the Commerce Dept
   closes a loophole on AI chips bought abroad; Nvidia rules out rehiring
   Huang.
6. **Diplomacy** — Trump meets Quad leaders in Manila: the US, Japan, India
   and Australia announce an AI initiative and minerals pacts.
7. **Finance** — Chase glitch delays bank transfers: a JPMorgan software bug
   slows transfers and Zelle; restored Monday evening.
8. **Yemen** — Houthi advance forces Yemen government retreat: government
   troops pull back from the Red Sea coast to defend Aden.

## How it is built

`entry.png` is composed programmatically with Python PIL (`build_image.py`):
crisp vector text, a clean light sky-blue layout — aviation hero, 2×2 grid,
bottom row of three cards — no AI-generated imagery, so every headline is
legible and correct. `main.py` is a pure file copy with sha256 verification
of the output — no network, no randomness — so both runs write identical
bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png — 1024x1024 PNG, identical on every run
```
