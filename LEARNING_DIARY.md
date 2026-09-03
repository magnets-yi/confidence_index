# WEEK0, DAY1
## Actions:
### Set up basic local folders, files and initiate Git
- Create an empty folder called confidence_index
- `git init -b master`: create .git/ under confidence_index. this is called initialize git repository. `-b` is short for `--branch`
- Create a new file under confidence_index called .gitignore: this file has a list of files and folders that will be ignored in git activities
- Create a new file under confidence_index called README.md: this is the markdown file to explain the repository. For the beginning, we just put in the project name and a short description.

### Create first commit to master branch
- `git add .gitignore README.md LEARNING_GIT_AND_CI.md LEARNING_PLAN.md`
- `git status`
- `git diff -cached`: shows difference between staged changes and last commits, i.e., exactly what will go into the next commit
- `git commit -m ""`
- `git log oneline`

### Create remote repo on GitHub and connect with local
- Open http://github.com/new, name the project confidence_index: create same name repository on GitHub remotely. Make sure don't edit README.md file on GitHub. As if README.md is created remotely, GitHub will produce a commit, which completely separate from local commit. Later PR won't be able to merge from local commit that doesn't share the same history with GitHub commit. If we were to push and PR local commit, it will fail
- `git remote add origin http://github.com/magnets-yi/confidence_index.git`: register a remote repo location with local Git setup
- `git push -u origin master`: GitHub default = master

### Create feature branch, PR loop
- `git checkout -b learn/week01-setup`: create a new local branch
- More local edit and commit
- `git push -u origin learn/week01-setup`: upload local commit to remote repo; learn/week01-setup is the local branch name. `-u` stands for --set upstream
- Create a PR on GitHub and squash merge


## Additional notes:
- **.git/**: is the git database
- **commit** each commit is a snapshot of the whole project a one moment, plus meta data (hash, parent, tree/index, author, message). Git photograpns the index - every tracked path - not a patch. Unchanged file reuse the same blobs. A branch is only a name pointing at that snapshot. The unit of history (commits) is a full tree not only the line edited



# WEEK0, DAY2
## Actions:

### Branch off master
- `git checkout master`
- `git checkout -b learn/week01-uv`

### Type pyproject.toml
- `uv --version`
- Create new file pyproject.toml under project folder, type
  - [project]
  - [dependency-groups]

### uv luck, sync, smoke test
- `uv lock`: uv generate uv.lock file
- `uv sync --group dev`
  - Read uv.lock (exact version) and pyproject.toml. if toml changes, uv will refresh lock file first
  - Create .venv/ if it is missing
  - Install into .venv/: pytest (defined in dev group) and its transitive dependencies (from PyPI) plus the project itself (confidence-index), which is named in pyproject.toml
- Create ./tests folder and a new file named test_smoke.py with assert (1+1==2)
- `uv run pytest`

### Commit and push
- `git status`
- `git add.`
- `git status`
- `git diff -cached`: check what will go into the commit
- `git commit -m "..."`
- `git status`
- `git push -u origin learn/week01-uv`
