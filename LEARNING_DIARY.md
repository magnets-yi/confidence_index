# WEEK1, DAY1
## Actions:
### Set up basic local folders, files and initiate Git
- Create an empty folder called confidence_index
- `git init -b master`: create .git/ under confidence_index. this is called initialize git repository. `-b` is short for `--initial branch`
- Create a new file under confidence_index called .gitignore: this file has a list of files and folders that will be ignored in git activities
- Create a new file under confidence_index called README.md: this is the markdown file to explain the repository. For the beginning, we just put in the project name and a short description.

### Create first commit to master branch
- `git add .gitignore README.md LEARNING_GIT_AND_CI.md LEARNING_PLAN.md`
- `git status`
- `git diff --cached`: shows difference between staged changes and last commits, i.e., exactly what will go into the next commit
- `git commit -m ""`
- `git log --oneline`

### Create remote repo on GitHub and connect with local
- Open http://github.com/new, name the project confidence_index: create same name repository on GitHub remotely. Make sure don't edit README.md file on GitHub. As if README.md is created remotely, GitHub will produce a commit, which completely separate from local commit. Later PR won't be able to merge from local commit that doesn't share the same history with GitHub commit. If we were to push and PR local commit, it will fail
- `git remote add origin http://github.com/magnets-yi/confidence_index.git`: register a remote repo location with local Git setup
- `git push -u origin master`: GitHub default = master

### Create feature branch, PR loop
- `git checkout -b learn/week01-setup`: create a new local branch
- More local edit and commit
- `git push -u origin learn/week01-setup`: upload local commit to remote repo; learn/week01-setup is the local branch name. `-u` stands for --set upstream
- Create a PR on GitHub and squash merge


## Notes:
- **.git/**: is the git database
- **commit** each commit is a snapshot of the whole project a one moment, plus meta data (hash, parent, tree/index, author, message). Git photograpns the index - every tracked path - not a patch. Unchanged file reuse the same blobs. A branch is only a name pointing at that snapshot. The unit of history (commits) is a full tree not only the line edited



# WEEK1, DAY2
## Actions:

### Branch off master
- `git checkout master`
- `git checkout -b learn/week01-uv`

### Type pyproject.toml
- `uv --version`
- Create new file pyproject.toml under project folder, type
  - [project]
  - [dependency-groups]

### uv lock, sync, smoke test
- `uv lock`: uv generate uv.lock file
- `uv sync --group dev`
  - Read uv.lock (exact version) and pyproject.toml. if toml changes, uv will refresh lock file first
  - Create .venv/ if it is missing
  - Install into .venv/: pytest (defined in dev group) and its transitive dependencies (from PyPI). The project itself is not installed as `uv.lock` says `source = { virtual = "." }`
- Create ./tests folder and a new file named test_smoke.py with assert (1+1==2)
- `uv run pytest`

### Commit and push
- `git status`
- `git add .`
- `git status`
- `git diff --cached`: check what will go into the commit
- `git commit -m "..."`
- `git status`
- `git push -u origin learn/week01-uv`
- PR and squash merged this branch on GitHub


## Notes
- **pyproject.toml**: what human declare, edit and commit
- **uv.lock**: exact resolved versions; committed; uv maintains, never hand-edit
- **.venv/**: actual installed files on this machine; gitignored; disposable, rebuld with `uv sync`
- I had a typo in pyproject.toml. After the typo is corrected, I run `uv sync --group dev` to update uv.lock and .venv/
- `git log --oneline --graph --decorate --all`: shows all the branches as a graph

### HEAD
- Locally: 
  - HEAD is stored in .git/HEAD, which is a one-line text file, such as "ref: refs/heads/learn/week01-uv"
  - HEAD is a pointer to a branch name and the branch name points to a commit
  - Working tree is a checkout of whatever commit HEAD resolves to, so HEAD determines which files are on disk
  - When commit, Git moves the branch that HEAD points to
- Remotely:
  - remote's HEAD means which branch is the default
  - It is the branch you land on when you clone without asking for one and the branch GitHub shows first in the web UI and pre-selects as the base for new PRs
  - It changes only when someone changes the repo setting

### stash
- `git stash`: Git takes uncommitted changes to tracked files, wraps them into commit objects, and points a new ref called `ref/stash` at them. Then it resets to the working tree to match whatever HEAD resolves to
- `git checkout master`: the file .git/HEAD gets rewritten to `ref/heads/master`. checkout nevers moves a label; it only changes which label HEAD names. Working tree is rebuilt to master branch
- `git pull`: two steps
  - `git fetch origin`: fetch downloads any new objects and update remote-tracking labels
  - `git merge origin/master`: Git checks if master is an ancestor of origin/master. It is in this case, hence it just slides master forward
- `git checkout -b learn/week01-own-uv`: create a new label, pointing at the same commit HEAD points to
- `git stash pop`: apply parked changes onto the current working tree, delete `ref/stash`

### delete branch
- On GitHub, open the merged PR and click Delete branch
- Locally:
  - `git branch -D learn/week01-uv`
  - `git branch -D learn/week01-setup`
  - `git fetch --prune`: compares local `refs/remotes/origin/*`  refs against the remote's actual branch and deletes any local ref with no counterpart. It never deletes local branches, never changes files on disk and never removes commits made. `git fetch --prune --dry-run` preview `git fetch --prune`
  - `git branch -a`
  - `git remote set-head origin master`: set remote HEAD to master in local file `.git/refs/remotes/origin/HEAD`

  ### Workflow after every merged PR
  - On GitHub, squash merge, then click Delete branch on the PR page
  - Get off the branch and catch up `master` locally: this step not only sync local master to remote, also moves off the feature branch. As in in the next step, the feature branch cannot be deleted, if it's still the active branch
    - `git checkout master`
    - `git pull`
  - Verify then delete the local feature branch:
    - `git diff learn/week02-ci origin/master --stat'`: compare the local feature branch with remote master after squash merge. if the result is blank, it's safe to remove the local feature branch
    - `git branch -D learn/week02-ci`
  - Clear remote tracking refs:
    - `git fetch --prune`: this can be made automatic by `git config --global fetch.prune true`
  - Confirm actually in sync:
    - `git status`
    - `git branch -a`
    - `git log --oneline --graph --decorate --all`: we see remote forks now
    - `git ls-remote`: list all hashes on remote repo
    - Delete remote featured branches as well (in Code tab)
    - `git fetch prune`
    - `git log --oneline --graph --decorate --all`

  # WEEK2, DAY1
  ## Reflect questions:
  - Your laptop has .venv/ with pytest installed. A GitHub runner starts empty. What has to happen, in order, before pytest can run there:
    - `actions/checkout@v7` clones repo on GitHub at the triggering commit. Now `pyproject.toml`, `uv.lock` and test/ exists on runner
    - `astral-sh/setup-uv@v10.0.1` downloads uv binary and adds it to PATH
    - `uv sync --group dev` reads `pyproject.toml` and `uv.lock`, obtains a Python on that satisfies `>=3.12`, creates `.venv` on the runner, and installs pytest plus `colorama`, `iniconfig`, `packaging`, `pluggy`, `pygments`
    - `uv run pytest` executes from that fresh `.venv`

  - If CI runs uv sync from your committed uv.lock, which pytest version does it get:
    - CI runs test using pytest version in `uv.lock` file if it is committed
    - If `uv.lock` is not committed, `uv sync` would refer `pyproject.toml` file, which as `pytest>=8.0`, a declaration not a constraint. Without a committed `uv.lock`, CI can pick up different pytest version at each run time which may fail the tests

  - Who decides which Python version the runner uses — your pyproject.toml, the workflow file, or both:
    - Both can specify, but workflow file override `pyproject.toml`
    - `uv.lock` pins every package but not the interpreter. CI doesn't reproduce laptop's environment, just a compatible one

  ## Actions:
  - Create `.github/workflows/ci.yml` file with
    - `name:`: what appears on GitHub Actions tab
    - `on:`: the trigger, such as `pull_request`
    - `jobs:`: the map of job IDs, free names, such as "test"
    - `runs-on:`: which VM, i.e., `ubuntu-latest`
    - `steps:`: on ordered list:
      - `uses: actions/checkout@<version>`: clones your repo onto the empty runner. For version, read README.md at https://github.com/actions/checkout
      - `uses: astral-sh/setup-uv@<version>`: installs uv, for version, read https://github.com/astral-sh/setup-uv
      - `run: uv sync --group dev`
      - `run: uv run pytest`
  - push and watch CI:
    - `git add .`
    - `git diff --cached`
    - `git commit -m "learn: first CI workflow"`
    - `git push -u origin learn/week02-ci`
  - Open PR, go to Actions tab, and watch the job run live

# WEEK2, DAY2
## Actions:
- Create `spec/methodology.md` file with the methodology of the index
- Create fixture files with prices and calendar: `spec/fixtures/prices.csv` and `spec/fixtures/calendar.csv`
- Create `spec/config.ymal` with parameters: 
- Install a python library and a small script or `python -c` to read `spec/config.ymal`: either
  - `uv add pyyaml`: library to convert YAML to python dictionary
    ```
    import yaml
    from pathlib import Path

    config = yaml.load(Path('spec/config.yaml').read_text(), Loader=yaml.FullLoader)
    print(config)
    ```
  - `uv add ruamel.yaml`: library to convert YAML to python dictionary, allows code to write YMAL as well. Typical use: create a YAML() object, then .load() / .dump()

- Use installed library to read `spec/config.yaml` and print the parameters: 
  - Either using the script above in a python file
  - Or from PowerShell: `python -c "import yaml; print(yaml.load(Path('spec/config.yaml').read_text(), Loader=yaml.FullLoader))"`
