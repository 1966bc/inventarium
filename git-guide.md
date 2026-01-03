# Git Guide

Essential commands for working with Git and GitHub.

## Repository Status

```bash
git status                # show modified, staged, and untracked files
git log --oneline -10     # last 10 commits
git diff                  # differences in modified files
git diff --staged         # differences in staged files
```

## Update from GitHub

```bash
git pull origin main      # download and apply remote changes
```

If you have local changes to preserve:
```bash
git stash                 # set aside local changes
git pull origin main
git stash pop             # reapply local changes
```

## Force Align with GitHub

Overwrites all local changes:
```bash
git fetch origin
git reset --hard origin/main
```

To also remove untracked files:
```bash
git clean -fdn            # preview (dry-run), shows what would be deleted
git clean -fd             # -f = force, -d = directories
```

## Save Changes (commit)

```bash
git add filename.py       # stage a specific file
git add .                 # stage all modified files
git commit -m "Description of changes"
```

## Push to GitHub

```bash
git push origin main
```

## Undo Local Changes

```bash
git checkout -- filename.py      # discard changes to a file
git restore filename.py          # equivalent (Git 2.23+)
git reset HEAD filename.py       # unstage a file
```

## Branches

```bash
git branch                        # list local branches
git branch branch-name            # create new branch
git checkout branch-name          # switch to a branch
git checkout -b branch-name       # create and switch to new branch
git merge branch-name             # merge branch into current
git branch -d branch-name         # delete local branch
```

## History and Differences

```bash
git log --oneline --graph         # graphical history
git show abc1234                  # details of a specific commit
git diff main origin/main         # differences between local and remote
```

## Configuration

```bash
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
git remote -v                     # show linked remote repositories
```
