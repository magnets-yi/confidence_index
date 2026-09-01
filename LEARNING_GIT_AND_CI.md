# Learning Git & GitHub Actions (deep, slow path)

Personal curriculum for rebuilding ownership of this repo — especially parts built with AI a while ago.

Write session notes under **My notes** in this file, next to the session — your words, not the agent's. Other repo notes (uv, packaging, Python) live in [Other notes](#other-notes-repo-uv-python) at the bottom.

**Pace:** ~6–8 weeks · 30–45 min per session · 3 sessions per week · one concept per session.

**Habit every session:** predict → run command → compare to prediction → write one sentence under that session's **My notes**.

---

## How to learn when AI built most of it

Treat the repo as a **museum you're excavating**, not a tutorial you follow.

For every file someone (or AI) created, ask:

1. **What problem does this solve?**
2. **What would break if I deleted it?**
3. **Can I reproduce it from scratch in a smaller form?**

If you can't answer (3), you don't "know" it yet — you're only familiar with it. That's fine; the exercises fix that.

### Rules for this curriculum

- Never merge to `master` until you can explain the change in plain English.
- Always work on a branch named `learn/module-XX-short-name`.
- After each session, add 3–5 lines under that session's **My notes** — your words, not the agent's.
- When stuck >15 minutes, stop and write *what you expected* vs *what happened*. That's the learning.

---

## Week 0 — Reconnect (1 session)

**Goal:** Confirm your machine matches GitHub.

```powershell
cd c:\Users\yizha\python_repo\index_lab
git status
git remote -v
git log --oneline -5
uv sync --group dev
uv run pytest -q
```

### Checkpoint questions (answer under **My notes**)

- What is the difference between your **working folder**, **staging area**, and **last commit**?
- What does `origin` mean? [A] `origin` is the acronym for remote
- What does `uv sync` do: [A] `uv sync` reads pyproject.toml (the intention, human writes) and uv.lock (the exact package versions), creates or updates .venv/ in the project folder and install the packages there.
- What is `--group dev`:  [A] means also install dev group, not just base project deps. dev group is defined in pyproject.toml as:
    [dependency-groups]
    dev = [
      "index-platform",
      "pytest>=8.0",
      "ruff>=0.8",
    ]
- YAML: Created in 2001 by Clark Evans. stands for YAML Ain't Markup Language, designed to replace XML. In 2009, any valid JSON is automatically valid YAML. It is designed to be human-friendly data serialization standard across all programming languages. it relies on visual white space.
- TOML: Created in 2013 by Tom Preston-Werner, formal Github CEO. It is created due to complexity of YAML and strictness of JSON. It was started from INI file, with first-class support for data type. It's mainly for application configurations across all programming languages. it relies on headers and key pathing.
- If CI passes on GitHub but pytest fails locally, what are three things you'd check?

### Read (don't edit)

`README.md` — only the Layout section. Draw the folders on paper: `research/`, `spec/`, `code/`, `data/`.

---

## Module 1 — Git is a snapshot graph (Week 1, ~3 sessions)

### Session 1.1: What Git actually stores

**Mental model:** Git doesn't store "files." It stores **commits** — snapshots with a parent pointer. Branches are just **labels** pointing at a commit.

**Exercise:**

```powershell
git log --oneline --graph --decorate -10
git show HEAD --stat
git cat-file -p HEAD
```

Look at one commit hash. Follow it in the log. You don't need to understand every line of `git cat-file` — just notice: tree, parent, author, message.

### Checkpoint questions (answer under **My notes**)

**Prompt:** "A commit is ___ because ___."

**My notes:**

- A **commit** is a snapshot of the whole project at one moment, plus metadata:
  - a unique hash (the commit's ID)
  - a **parent** pointer (the previous commit; this is how history is chained)
  - a **tree** (the folder listing for that snapshot; it points at blobs and at other trees)
  - author + message
- The snapshot is a complete picture of every tracked file, but Git does not copy every file for every commit. Unchanged files reuse the same blobs.
- A **branch** is only a movable name (a label) pointing at one commit — not a stored copy of a path. **HEAD** is also a name: usually it points at a branch, and that branch points at a commit.
- When you trace a branch's history, Git starts at that label and follows each commit's parent pointer. The path is inferred; it is not stored on the branch.
- File contents are stored as **blobs** (raw bytes) in `.git/objects/`. The whole repo shares one object store. Two commits share a blob whenever the file contents are identical.

### Session 1.2: The four places files live

| Place | Command to see it |
|-------|-------------------|
| Working tree | `dir` / edited files |
| Staging (index) | `git status`, `git diff --cached` |
| Local repo | `git log` |
| Remote repo | GitHub website |

**Exercise:** Change one line in this file (a session **My notes** block only).

```powershell
git status
git diff
git add LEARNING_GIT_AND_CI.md
git diff --cached
git commit -m "learn: note module 1.2 staging"
```

Before each command, **write down what you expect**. Then run it.

**My notes:**

- Four places for files:
  - **Working tree / working directory:** the project folder on disk. You edit here. It is the last commit, plus any uncommitted changes. Edits here are not history yet.
  - **Staging (index):** Git's proposed next snapshot. Unchanged files keep their old blobs; `git add` records new blobs for the files you choose. It is called the index because that catalog lives in `.git/index`: each path maps to which blob (and file mode) should be in the next commit.
  - **Local repo:** `.git/objects/` — the commits you have locally. Each commit is a frozen snapshot: tree + parent + author + message. A commit photographs **staging**, not the working tree.
  - **Remote repo:** GitHub's copy of the same object store. It updates on `git push` / `git fetch`, not when you save a file or commit locally.
- Related commands:
  - `git add`: copy these working-tree bytes into the index (staging)
  - `git diff`: working tree vs staging (unstaged edits)
  - `git diff --cached`: staging vs last commit (`HEAD`) — what the next commit would contain
  - `git status`: a summary of unstaged, staged, and untracked files (not one three-way diff)
  - `git commit -m "..."`: freeze the index as a new commit, then slide the current branch label forward

### Session 1.3: Your first branch (the core habit)

```powershell
git checkout -b learn/module-01-snapshots
# make a tiny My notes line
git commit -am "learn: module 1 complete"
git push -u origin learn/module-01-snapshots
```

On GitHub: open a **Pull Request** into `master`. A PR is not a Git object — it is a GitHub request: “please merge these commits into `master`.” Creating it does not move `master`.

1. Open https://github.com/magnets-yi/index_lab (after the push, a banner **Compare & pull request** often appears).
2. Or: **Pull requests** → **New pull request**.
3. Base: `master` ← compare: `learn/module-01-snapshots`.
4. Title/body, then **Create pull request**.
5. Read every line of the diff. **Do not merge yet** — just look.

**Checkpoint:** Can you explain why `master` didn't move when you pushed the branch?

[A] You pushed the **`learn/module-01-snapshots` label**, not the **`master` label**. `HEAD` points at the learning branch, so new commits moved that name forward. `git push -u origin learn/module-01-snapshots` updates `origin/learn/module-01-snapshots` on GitHub. `master` is a different name; nothing rewrote it.

**My notes:**

- `git checkout -b learn/module-01-snapshots`: create a new branch label on the commit you are on right now, then point `HEAD` at that name. `-b` means **branch**: create it, then check it out. Same snapshot as `master` until you commit.
- `git commit -am "learn: module 1 complete"`: `-a` is `--all` (stage modified/deleted **tracked** files); `-m` is `--message`. This skips a separate `git add` for tracked files. It does **not** add untracked files. The commit moves the current branch label (`learn/module-01-snapshots`), not `master`.
- `git push -u origin learn/module-01-snapshots`: upload that branch's commits to GitHub and set upstream tracking (`-u`) so later `git push` / `git pull` know which remote branch to use.
- `Git Repo`: a repository is one Git database (.git/) and the working tree next to it.
- `GitHub Repo`: is the same kind of database sitting on GitHub's machines, with a website on top (PRs, Issues). Git pushes copies objects and updates labels there. A fork is another GitHub repo.

---

## Module 2 — Clone, remote, sync (Week 2)

### Session 2.1: Clone from scratch (second copy)

Pick an empty folder *outside* this repo:

```powershell
cd c:\Users\yizha\python_repo
git clone https://github.com/magnets-yi/index_lab.git index_lab_clone
cd index_lab_clone
uv sync --group dev
uv run pytest -q
```

**Goal:** Feel that clone = full history + `origin` already set.

Compare:

```powershell
# in original repo
git rev-parse HEAD
# in clone
git rev-parse HEAD
```

Same hash = same snapshot.

**My notes**
- git rev-parse: resolve name into an object ID / hash ID.
  - git rev-parse HEAD: HEAD is the name (I am on this branch). This command print out the hash HEAD point to
  - git rev-parse origin/master: 

### Session 2.2: Push, pull, fetch

Back in your **original** repo on your learning branch:

```powershell
git fetch origin
git status
git pull origin master   # only when on master; practice safely later
```

**Mental model:**

- `fetch` = download new commits, don't change your files
- `pull` = fetch + merge into current branch
- `push` = upload your commits to remote

**My notes:** Draw arrows: local branch → `origin/branch` → GitHub.
- **git fetch** origin: with `git fetch`, we can first look before merge
  - copy new objects from remote to .git/objects/ and 
  - move remote tracking label such as origin/master
  - with `git fetch origin`, we can check differences between remote and local:
    - `git log master..origin/master`
    - `git log origin/master..master`
- Difference between `fetch` and `pull`
  - `fetch` updates picture of remote
  - `pull` moves current label to include the picture

### Session 2.3: Merge your first PR

The PR was created in Session 1.3 (GitHub UI: base `master`, compare `learn/module-01-snapshots`). If that never happened, create it now with those same steps, then come back.

Merge it on GitHub (squash or merge commit — either is fine; note which you picked). Merging **is** what moves `master` on GitHub.

Locally:

```powershell
git checkout master
git pull
git log --oneline -3
```

**Checkpoint:** Where did your learning-branch commit go? Can you find it in the log?

**My notes**
- PR: Pull request, a GitHub ticket: merge branch X into branch Y
- Commits on a PR: snapshots on X that Y doesn't have yet
- This PR has two commits: you made two commits on X (the compare branch)
- Three options to merege a PR: suppose master is M and the PR has two commits A←B (A is B's parent)
  - **Squash and merge**: the most common choice. GitHub builds one new commits S, whose tree matches B (all PR changes in a single snapshot). S has one parent M. `M←S←master`. The history stays a straigh line. The PR is one commit on master. The idea is each PR is one story
  - **Create a merge commit**: GitHub adds a new commit C with two parents M and B. A and B stays in the history. This is the only option that records "This was a branch that merged."
  - **Rebase and merge**: the least common option. GitHub replays A and B on top of M as new commits A' and B', then moves master to B'. `M←A'←B'←master`


---

## Module 3 — Read your repo's CI without fear (Week 3)

Attack the AI-built part **one line at a time**.

Open `.github/workflows/code-ci.yml`. Read it with this map:

| YAML line | Question to answer |
|-----------|-------------------|
| `name:` | What shows up in GitHub Actions UI? |
| `on:` | When does this run? Push to which branches? |
| `paths:` | Why doesn't editing a notebook trigger this? |
| `jobs:` | What parallel work units exist? |
| `runs-on:` | What machine runs this? |
| `strategy.matrix` | Why test 3.12 *and* 3.13? |
| `steps:` | Ordered recipe inside the job |
| `uses: actions/checkout@v4` | "Check out" = clone this commit into the runner |
| `uses: astral-sh/setup-uv@v5` | Install uv + Python |
| `run: uv sync` | Same as your laptop |
| `run: pytest` | Same as your laptop |

**My notes:**

- YAML here is nested data (maps and lists), not a program. GitHub parses `.github/workflows/code-ci.yml`, then Actions follows that structure. Indentation = nesting. `key: value` is a map. `- item` or `[a, b]` is a list. `${{ ... }}` is not YAML; it is GitHub’s expression syntax, filled in later.
- Two vocabularies (do not memorize the file):
  - **Schema / events** (`name`, `on`, `push`, `pull_request`, `jobs`, `runs-on`, `steps`, `uses`, `run`, `with`, `matrix`): GitHub workflow docs. https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax

  - **`owner/repo@ref`**: another GitHub repo (an action) plus a git tag in *that* repo. README/Releases of that repo, not the YAML spec. `@v4` vs `@v5` are independent version numbers (like pytest vs ruff). Copy `uses:` from that action’s README. This file’s v4/v5 were current when CI was written; bumping is optional later.
  
- `name: code-ci` — label on the Actions tab.
- `on:` — when it runs:
  - `push` to `main` or `master`
  - `pull_request` (path-filtered; not limited to those branch names the way `push` is)
- `paths:` — only `code/**`, `pyproject.toml`, `uv.lock`, and this workflow file. A notebook under `research/` does not match, so `code-ci` does not run.
- `jobs.test` — one recipe. `strategy.matrix` python `3.12` and `3.13` clones that recipe twice (two parallel VMs). `runs-on: ubuntu-latest` is GitHub’s Linux VM, not the laptop.
- `steps` (order matters):
  - `uses: actions/checkout@v4` — `actions` org, `checkout` repo, tag `v4`. Clone *this* repo at the triggering commit onto the empty VM.
  - `uses: astral-sh/setup-uv@v5` — Astral’s `setup-uv` repo, tag `v5`. Install uv and the matrix Python (`with: python-version: ${{ matrix.python-version }}`).
  - `run: uv sync --group dev` — same as the laptop: lockfile → `.venv` on the runner, including pytest/ruff/`index-platform`.
  - `run: uv run ruff check code/platform code/calc` then `uv run pytest code/platform/tests code/calc/spxf3ev6/tests -q` — lint + tests on `code/` only. Non-zero exit → red check.
- Trigger → green: path-matching push/PR → two Ubuntu jobs → checkout → setup-uv → sync → ruff → pytest → both cells pass.

**Exercise (safe failure):**

```powershell
git checkout -b learn/module-03-break-ci
```

Add a silly failing test or break a string in an assertion. Push. Open PR. **Watch Actions tab.**

Fix it. Push again. Watch CI go green.

**Checkpoint:** In your own words, write what `code-ci` does from trigger → green checkmark.
[A] When a PR or push touches code/ or the lockile/CI file, GitHub starts two Linux VMs, clones the commits, installs uv/Python, `uv sync --group dev`, ruff, pytest, if both versions pass, the check is green.

Repeat **half** of this for `spec-ci.yml` — notice it's simpler and *doesn't* run pytest. Read `PLAN.md` CI section — now it should make sense *why* two workflows exist.

---

## Module 4 — Branching workflows you'll use forever (Week 4)

### Session 4.1: Feature branch lifecycle

Practice the loop until it's muscle memory:

1. `git checkout master && git pull`
2. `git checkout -b learn/module-04-feature`
3. change → commit → push
4. PR → review diff → merge
5. `git checkout master && git pull`
6. delete branch locally: `git branch -d learn/module-04-feature`

### Session 4.2: When branches diverge

On `master`, make commit A. On a branch, make commit B from an older point. Push both. Observe PR "can merge" vs conflict.

Optional: create a tiny conflict on purpose (same line in this file). Learn:

```powershell
git status          # during conflict
# edit file to resolve
git add ...
git commit
```

**Deep idea:** Merge = combine histories. Rebase = replay your commits on top of another branch. Don't rebase `master`; only experiment on `learn/*` branches.

### Session 4.3: What is `origin/master`?

```powershell
git branch -vv
git log master..origin/master
git log origin/master..master
```

**Checkpoint:** After `git fetch`, what updates — your files or remote-tracking branches?

---

## Module 5 — Build a tiny workflow yourself (Week 5)

Don't rewrite the real CI. Add a **learning workflow** on a branch.

Create `.github/workflows/learn-hello.yml`:

```yaml
name: learn-hello

on:
  workflow_dispatch:

jobs:
  say-hi:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello from Actions"
      - run: python --version
```

Push, go to Actions → **Run workflow** manually.

Then extend slowly (one addition per session):

- Add `actions/checkout@v4`
- Print `git log -1`
- Add a step that runs only if branch name starts with `learn/`

When each step works, you **own** Actions syntax — not AI.

Merge only when you can explain every line.

---

## Module 6 — Map repo architecture to Git/CI (Week 6+)

Revisit the AI-built structure with fresh eyes:

| Folder | CI | Your question |
|--------|-----|---------------|
| `research/` | none | Why no gate? |
| `spec/` | spec-ci | What would invalid YAML break? |
| `code/` | code-ci | What do tests actually guard? |
| `data/` | partial checks | What's committed vs generated? |

Pick **one** test file, e.g. `code/platform/tests/test_engine.py`. Read one test. Run it alone:

```powershell
uv run pytest code/platform/tests/test_engine.py -v
```

Trace: test → import → source file. That connects Git, CI, and Python packaging ([Other notes](#other-notes-repo-uv-python) has the import write-up — re-read it *after* Module 3).

---

## Pace and rhythm

| If you have… | Do… |
|--------------|-----|
| 30 min | One session, one concept, one **My notes** entry |
| 45 min | Session + checkpoint questions |
| 1 hr | Session + optional "break something on purpose" |

**Suggested schedule:** Mon / Wed / Fri, same time. Skip a day rather than cram.

**Don't skip:** predicting before running commands, and writing in your own words.

---

## What to ignore for now

- Advanced Actions (caching, secrets, deployments, matrix beyond Python version)
- Rebase wars, cherry-pick, hooks
- Rewriting `code-ci.yml` until Module 5 feels easy
- Understanding every line of `index_platform` — that's Python learning, not Git learning

---

## Why learn in this repo (not a blank tutorial)

This repo already has:

- A real remote: `https://github.com/magnets-yi/index_lab.git`
- Two path-filtered workflows: `code-ci` and `spec-ci`
- Tests that CI runs the same way as your laptop (`uv sync` + `pytest`)
- Documented layout in `README.md` and `PLAN.md`

Use a **fork** or local `learning_playground/` (gitignored) only for destructive experiments — breaking CI on purpose, messy rebases, etc.

---

## Session-by-session with an agent

In chat, say:

> "Starting Module 1, Session 1.1"

The agent should give you:

1. A short concept (~5 min read)
2. Exact commands for this repo
3. 2–3 checkpoint questions
4. What to write under that session's **My notes** when done

Run the commands yourself. Paste output if something surprises you. Only advance when the checkpoint makes sense.

---

## Progress tracker

Tick dates here as you go.

| Module | Session | Done | Date |
|--------|---------|------|------|
| 0 | Reconnect | | |
| 1 | 1.1 Snapshots | | |
| 1 | 1.2 Staging | | |
| 1 | 1.3 First branch | | |
| 2 | 2.1 Clone | | |
| 2 | 2.2 fetch/pull/push | | |
| 2 | 2.3 Merge first PR | | |
| 3 | Read code-ci | | |
| 3 | Break/fix CI | | |
| 3 | Read spec-ci | | |
| 4 | 4.1 Feature branch loop | | |
| 4 | 4.2 Divergence/conflicts | | |
| 4 | 4.3 origin/master | | |
| 5 | learn-hello workflow | | |
| 5 | Extend workflow | | |
| 6 | Map folders to CI | | |
| 6 | Trace one test | | |

---

## Next step

**Module 0 today:**

1. Run the reconnect commands above.
2. Answer the checkpoint questions under Week 0 **My notes**.
3. Note whether `pytest` passed locally and anything unexpected in `git status`.

Then start **Module 1, Session 1.1**.

---

## Other notes (repo, uv, Python)

Moved here from `LEARNING_JOURNAL.md` so everything lives in one file. Architecture still lives in [PLAN.md](./PLAN.md).

### Project steps

| Step | Title | Status | Date |
|------|-------|--------|------|
| 1 | Minimal scaffold (contracts + engine skeleton) | Done | 2026-06-01 |
| 2 | Methodology examples + data + scripts | Blocked on you | |

#### Step 1 — Minimal scaffold

**Status:** Done  
**Date:** 2026-06-01

What we built:

- Monorepo zones: `research/`, `spec/`, `code/platform/`, `code/calc/`, `data/` (legacy was three packages under `packages/`)
- Shared schemas, manifest, handoff dataclasses
- Generic `IndexEngine` + validation + audit + `run_daily()`
- Research onboard pipeline + parity helper
- Empty `data/` layout; no prefilled data or placeholder indices
- Split CI; 6 tests passing

```bash
uv sync --group dev
uv run pytest -q
```

**Next:** Provide methodology examples → we add data, handoff bundles, golden calcs, and scripts.

### Commands worth keeping

Search commit history for messages containing `step 2:`:

```bash
git log --oneline --grep="step 2:"
```

Quick peek at parquet without a notebook:

```bash
uv run python -c "import polars as pl; print(pl.read_parquet('data/spxf3ev6/onboarded/synthetic_v1/prices.parquet').head())"
```

### `uv.lock`, `pyproject.toml`, `.venv/`

| File/folder | Committed to git? | Role |
|-------------|-------------------|------|
| `pyproject.toml` | Yes | What you declare you need |
| `uv.lock` | Yes (recommended) | Exact resolved versions |
| `.venv/` | No (in `.gitignore`) | Actual installed files on disk |

Flow: `pyproject.toml` → uv resolves → `uv.lock` (saved) → `uv sync` → `.venv/` (local install)

When someone clones the repo, `uv sync --group dev` reads `uv.lock` and installs the same versions into a new `.venv`.

`uv.lock` updates when you change dependencies, for example:

- `uv add pandas`
- Edit `pyproject.toml` and run `uv lock` or `uv sync`
- `uv lock --upgrade` (intentionally bump versions)

Practical takeaways:

- Don't edit `uv.lock` by hand — uv maintains it
- When learning what packages this project uses, start with `pyproject.toml` (human intent)
- When debugging "why did CI install a different version than my laptop?", compare `uv.lock` or rerun `uv sync` from the latest lock
- The lock is why `uv run pytest` always sees the same polars/pytest versions across machines

### Push local repo to GitHub

1. Create the repo on GitHub: https://github.com/new
   - Repository name: `index_lab`
   - Description: `Research-to-production index calculation workflow simulation`
   - Do not add a README, `.gitignore`, or license on GitHub (those already exist locally)
2. Connect the local repo:

```powershell
cd c:\Users\yizha\python_repo\index_lab
git remote add origin https://github.com/magnets-yi/index_lab.git
git push -u origin master
```

`-u origin master` sets `master` to track `origin/master`, so later you can just run `git push`.

3. Verify:

```powershell
git remote -v
git status
```

You should see `origin` pointing at your GitHub URL and something like "Your branch is up to date with `origin/master`."

### Additional libraries to be learned

```python
from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path
```

`from __future__ import annotations` lets you write `list[date]` in type hints on older Python. Without it, `list` as a type cannot be subscripted with `[date]`.

```python
from __future__ import annotations

def business_days(start, end) -> list[date]:
    ...
```

### Python packaging and how imports resolve

```python
from index_platform.contracts.manifest import DatasetManifest, save_manifest
```

#### 1. Python package (what you `import`)

- Code lives at `code/platform/src/index_platform/`
- Folder `index_platform/` is the package because it has `__init__.py`
- Files like `manifest.py` are submodules → `from index_platform.contracts.manifest import ...`
- **Import name** uses underscores: `index_platform`

#### 2. Installable distribution (what uv installs)

In `code/platform/pyproject.toml`:

- `[project] name = "index-platform"` → **distribution name** (hyphens, for uv/pip)
- `[build-system]` + hatchling → builds/installs the package
- `packages = ["src/index_platform"]` → tells the builder where the importable code is

#### 3. Workspace + dependency resolution (root `pyproject.toml`)

- `[tool.uv.workspace] members = ["code/platform"]` → local packages in the monorepo
- `[tool.uv.sources] index-platform = { workspace = true }` → use the local folder, not PyPI
- `[dependency-groups] dev = ["index-platform", ...]` → optional deps installed with `uv sync --group dev`

#### 4. What `uv sync --group dev` does

1. Reads root + each member's `pyproject.toml`
2. Resolves versions → `uv.lock`
3. Installs into `.venv` (editable links to `code/platform/`)
4. Python can then `import index_platform` from anywhere

**One line:** `index-platform` in TOML = what uv installs; `index_platform` in Python = what you import; `uv sync --group dev` wires them together in `.venv`.
