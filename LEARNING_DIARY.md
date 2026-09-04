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
  - `git fetch --prune`
  - `git branch -a`
