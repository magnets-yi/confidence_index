# Learning plan (copy this file into the new repo)

Cadence: **3 hours × 5 days = 15 hours/week**.  
Calendar: **9 weeks** (135 hours), 1 Sep 2026 → **31 Oct 2026**.  
One week of buffer is included. Miss a day; do not skip a week.

`index_lab` is a **museum**. Do not import `index_platform`. Copy this file, `LEARNING_GIT_AND_CI.md` if you want Git notes, and the methodology markdown when Stage 2 starts.

---

## Approach

- **New repo.** Empty Git history. One package, one CI workflow.
- **You type the files.** Agent guides and debugs; it does not paste finished calc, `pyproject.toml`, or workflow YAML. Definitions stay direct.
- **Skip:** research notebooks, data QA, live market data, official vendor parity.
- **Stage 1** is a **toy** index so you learn Git, uv, folders, README, YAML, Polars, pytest, Actions.
- **Stage 2** is **SPXF3EV6 only**, using the vendor methodology markdown. Implied vol is a **fixture column**, not a full SPXW options engine. Appendix A is optional after the finish date.

Each 3-hour day: 10 min predict → 2 h work → 20 min tests/notes → 10 min commit on a branch. Do not merge until you can explain the change.

---

## Stage 1 — toy index + tooling (3 weeks, 45h)

Toy methodology (you write one page): daily prices → returns → scale to target vol → constant decrement. Tiny committed CSV. One `config.yaml`.

| Week | Dates | Hours | Milestone | Done when |
|------|-------|-------|-----------|-----------|
| 1 | 1–5 Sep | 15 | Repo, Git, uv | GitHub repo exists. README, `.gitignore`. Branch → PR → merge → pull `master`. `pyproject.toml` + `uv.lock`. `uv sync --group dev`. `uv run pytest` passes on a trivial test. You can explain toml vs lock vs `.venv`. |
| 2 | 8–12 Sep | 15 | CI + spec | One workflow: checkout, setup-uv, `uv sync`, pytest. PR is green. `methodology.md` + `config.yaml`. Python loads YAML and prints it. You can explain every CI key. |
| 3 | 15–19 Sep | 15 | Polars + tests | Fixture CSV → levels table. Hand calc on ~5 rows matches. Pytest fails if you break the formula. README says how to run. You can say what each file is for. |

**Gate to Stage 2:** clone → `uv sync --group dev` → `uv run pytest` green locally and on GitHub. Config is YAML, not magic numbers. You typed CI yourself.

---

## Stage 2 — SPXF3EV6 (5 weeks, 75h)

Copy `research/spxf3ev6/intake/MinerU_markdown_methodology-sp-edge-vol-indices.md` into the new repo. Implement **S&P 500 Futures 35% Edge Volatility 6% Decrement (USD) ER** only.

**In:** five weekday subindices, leverage `min(cap, TV/IV)`, 25% floor, 6% decrement (360-day), equal-weight composite, YAML params + rebalance rules, synthetic underlying (close / TWAP / fixing) + IV series, tests, CI green.

**Out until later:** other family members, live data, minute-level options, Black IV from a full chain, research/onboard/parity.

| Week | Dates | Hours | Milestone | Done when |
|------|-------|-------|-----------|-----------|
| 4 | 22–26 Sep | 15 | Read + spec + fixtures | Markdown copied. YAML: TV=35%, cap=5, DF=6%, base 100, weekday rebalance map. Synthetic series for ≥2 weeks (close/TWAP/fixing + IV). |
| 5 | 29 Sep–3 Oct | 15 | Calendar + one subindex | Code knows whose rebalance day it is and how `Days(rb-1, t)` is counted. One subindex matches a 3-day hand calc (leverage, `n`, floor, decrement). Pytest locks those rows. |
| 6 | 6–10 Oct | 15 | Five subindices + composite | All five subindices and index aggregation (close / fixing / TWAP as in the doc). One fixture run writes a levels table. |
| 7 | 13–17 Oct | 15 | Floor, decrement, tests | 25% floor and 6% DF covered (including a day that would breach the floor). Hand-calc tests for one rebalance day and one non-rebalance day. CI runs the real tests. |
| 8 | 20–24 Oct | 15 | Ship | README: how to run SPXF3EV6. You can walk trigger → green. **Main finish.** |

---

## Buffer (1 week, 15h)

| Week | Dates | Hours | Use |
|------|-------|-------|-----|
| 9 | 27–31 Oct | 15 | Slip only. If Stage 2 is already shipped, optional stretch: Appendix A (IV from a **tiny** options fixture). Do not start stretch if recursion is unfinished. |

**Main finish date:** 24 Oct 2026. **Hard stop including buffer:** 31 Oct 2026.

---

## Layout to aim for (Stage 1)

```
<new-repo>/
  README.md
  pyproject.toml
  .gitignore
  spec/methodology.md
  spec/config.yaml
  fixtures/prices.csv
  src/… or calc/
  tests/
  .github/workflows/ci.yml
```

Stage 2 adds the vendor markdown, more YAML, more fixtures, more tests — same skeleton.
