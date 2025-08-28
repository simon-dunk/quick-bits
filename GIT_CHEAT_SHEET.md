# Git Documentation Markdown

## Table of Contents
1. [Getting Started](#getting-started)
2. [Repository Setup](#repository-setup)
3. [Branch Management](#branch-management)
4. [Staging and Adding Files](#staging-and-adding-files)
5. [Commit](#commit)
   - [Concept Overview](#concept-overview)
   - [Basic Commits](#basic-commits)
   - [Undoing Commits](#undoing-commits)
6. [Stashing](#stashing)
   - [Concept Overview](#concept-overview-1)
7. [Repository (push/pull)](#repository)
   - [Remote Management](#remote-management)
8. [Merge](#merge)
   - [Concept Overview](#concept-overview-2)
   - [Helpful for resolving conflicts](#helpful-for-resolving-conflicts)
9. [Rebasing](#rebasing)
   - [Concept Overview](#concept-overview-3)
10. [Untracking Files](#untracking-files)
11. [Viewing History](#viewing-history)
12. [Tags](#tags)
13. [Configuration](#configuration)
14. [Troubleshooting](#troubleshooting)
15. [Advanced Commands](#advanced-commands)

<br>
<br>

# Getting Started

#### Check Git version
```sh
git --version
```

---

#### Get help for any Git command
```sh
git help <command>
```
```sh
git <command> --help
```

---

#### Initialize a new Git repository
```sh
git init
```

---

#### Clone an existing repository
```sh
git clone <repository-url>
```

---

#### Clone to a specific directory
```sh
git clone <repository-url> <directory-name>
```

---

<br>
<br>

# Repository Setup

#### Add a remote repository
```sh
git remote add origin <repository-url>
```

---

#### View all remote repositories
```sh
git remote -v
```

---

#### Change remote repository URL
```sh
git remote set-url origin <new-repository-url>
```

---

#### Remove a remote repository
```sh
git remote remove <remote-name>
```

---

<br>
<br>

# Branch Management

#### Create a new branch and switch to it
```sh
git checkout -b new-branch-name
```

---

#### Create a new branch without switching to it
```sh
git branch new-branch-name
```

---

#### List all branches (local)
```sh
git branch
```

---

#### List all branches (local and remote)
```sh
git branch -a
```

---

#### List only remote branches
```sh
git branch -r
```

---

#### Switch to an existing branch
```sh
git checkout existing-branch-name
```
or
```sh
git switch existing-branch-name
```
Use `git switch` if you only need to switch branches.
Use `git checkout` if you're working with an older Git version or need to check out specific files.

---

#### Using `checkout` to check out specific files
```sh
git checkout remote-branch-name -- "path/to/file.txt"
```

---

#### Rename the current branch
```sh
git branch -m new-branch-name
```

---

#### Rename a different branch
```sh
git branch -m old-branch-name new-branch-name
```

---

#### Delete a local branch
```sh
git branch -d branch-name
```

---

#### Force delete a local branch (even if not merged)
```sh
git branch -D branch-name
```

---

#### Delete a remote branch
```sh
git push origin --delete branch-name
```

---

#### Track a remote branch
```sh
git branch --set-upstream-to=origin/branch-name
```

---

#### Create and push a new branch to remote
```sh
git checkout -b new-branch
git push -u origin new-branch
```

---

<br>
<br>

# Staging and Adding Files

#### Stage specific files
```sh
git add file1.txt file2.txt
```

---

#### Stage all changes in current directory and subdirectories
```sh
git add .
```

---

#### Stage all changes in the repository
```sh
git add -A
```

---

#### Stage all modified and deleted files (not new files)
```sh
git add -u
```

---

#### Interactively stage changes
```sh
git add -i
```

---

#### Stage parts of a file (patch mode)
```sh
git add -p
```

---

#### Unstage a file
```sh
git reset HEAD <file>
```

---

#### Unstage all files
```sh
git reset HEAD
```

---

<br>
<br>

# Commit

#### Concept Overview
**Committing** saves changes to the local repository, creating a snapshot of the project at that point in time. Each commit has a unique hash and a message describing the changes. This allows for easy version tracking and rollback if needed. Before committing, changes must be staged using git add.

---

## Basic Commits

#### Commit staged changes
```sh
git commit -m "Your commit message"
```

---

#### Commit with a multi-line message
```sh
git commit -m "Short description" -m "Longer description with more details"
```

---

#### Stage and commit all modified files in one command
```sh
git commit -am "Your commit message"
```

---

#### Commit with an editor for the message
```sh
git commit
```

---

#### Amend the last commit (change message or add files)
```sh
git commit --amend -m "New commit message"
```

---

#### Amend without changing the commit message
```sh
git commit --amend --no-edit
```

---

## Undoing Commits

#### See current status of working directory and staging area
```sh
git status
```

---

#### Undo most recent commit but keep changes in the working directory (soft reset)
```sh
git reset --soft HEAD~1
```

---

#### Undo the last commit and discard changes (hard reset)
```sh
git reset --hard HEAD~1
```

---

#### Undo a commit but keep the changes staged (mixed reset)
```sh
git reset --mixed HEAD~1
```

**Note:** `HEAD~1` refers to 1 commit back. To go more than one commit back, change 1 to however many commits back you want to reset. 

---

#### Reset to a specific commit
```sh
git reset --hard <commit-hash>
```

---

#### Undo a commit with `git revert` (safe, creates a new commit)
```sh
git revert <commit-hash>
```
This will create a new commit that undoes the changes from the specified commit. This is great when you want to "reverse" a commit but keep a clean history.

---

#### Revert a merge commit
```sh
git revert -m 1 <merge-commit-hash>
```

---

<br>
<br>

# Stashing

#### Concept Overview
**Stashing** in Git allows you to temporarily save your changes without committing them. This is useful when you need to switch branches or pull updates but aren't ready to commit your current work. Stashed changes can be reapplied later using git stash pop or git stash apply.

---

#### Save changes temporarily (stash)
```sh
git stash
```

---

#### Stash with a custom message
```sh
git stash push -m "Work in progress on feature X"
```

---

#### Stash only specific files
```sh
git stash push -m "Stashing specific files" -- file1.txt file2.txt
```

---

#### Stash including untracked files
```sh
git stash -u
```

---

#### Stash including ignored files
```sh
git stash -a
```

---

#### List all stashed changes
```sh
git stash list
```

---

#### Show the contents of a stash
```sh
git stash show stash@{0}
```

---

#### Show detailed diff of a stash
```sh
git stash show -p stash@{0}
```

---

#### Apply the most recent stash and remove it from the stash list
```sh
git stash pop
```

---

#### Apply a specific stash without removing it from the stash list
```sh
git stash apply stash@{index}
```

---

#### Create a branch from a stash
```sh
git stash branch new-branch-name stash@{0}
```

---

#### Drop a specific stash
```sh
git stash drop stash@{index}
```

---

#### Remove all stashed changes
```sh
git stash clear
```

---

<br>
<br>

# Repository

**Note:** Sometimes including `origin/branch-name` or `origin branch-name` might be necessary for pushing and pulling.

#### Fetch latest changes from remote without merging
```sh
git fetch
```

---

#### Fetch from a specific remote
```sh
git fetch origin
```

---

#### Fetch and prune deleted remote branches
```sh
git fetch --prune
```

---

#### Pull latest changes from remote and merge
```sh
git pull
```

---

#### Pull from a specific branch
```sh
git pull origin branch-name
```

---

#### Pull with rebase instead of merge
```sh
git pull --rebase
```

---

#### Push changes to remote repository
```sh
git push
```

---

#### Push to a specific branch
```sh
git push origin branch-name
```

---

#### Push and set upstream tracking
```sh
git push -u origin branch-name
```

---

#### Force push (use with caution)
```sh
git push --force
```

---

#### Safer force push
```sh
git push --force-with-lease
```

---

#### Push all branches
```sh
git push --all origin
```

---

#### Push tags
```sh
git push --tags
```

**Note:** Pushing can only be done after a commit.

---

## Remote Management

#### Show remote repository information
```sh
git remote show origin
```

---

#### Rename a remote
```sh
git remote rename old-name new-name
```

---

#### Update remote tracking branches
```sh
git remote update
```

---

<br>
<br>

# Merge

#### Concept Overview
**Merging** is the process of combining changes from one branch into another. This is commonly used in collaborative workflows when integrating feature branches into the main branch. If there are conflicting changes between branches, Git requires manual conflict resolution before completing the merge.

---

#### Merge a branch into the current branch
```sh
git merge branch-name
```

---

#### Merge without creating a merge commit (fast-forward)
```sh
git merge --ff-only branch-name
```

---

#### Always create a merge commit
```sh
git merge --no-ff branch-name
```

---

#### Merge with a custom commit message
```sh
git merge branch-name -m "Custom merge message"
```

---

#### Undo merge before commit
```sh
git merge --abort
```

---

#### Check if branches can be merged cleanly
```sh
git merge-tree $(git merge-base branch1 branch2) branch1 branch2
```

---

## Helpful for resolving conflicts

Let's assume we want to merge the changes from the `production` branch into the `in-progress-behind` branch.

#### To manually resolve any conflicts that might occur, use this command
```sh
git checkout production
git merge csv-validation
```

---

#### Merge favoring current branch changes
```sh
git checkout production
git merge in-progress-behind --strategy=ours
```
`ours` in `--strategy=ours` refers to the `production` branch since we called a `git checkout production` first.

---

#### Merge favoring incoming branch changes
```sh
git merge branch-name -X theirs
```

---

#### Show conflicts in a merge
```sh
git status
```

---

#### Use a merge tool to resolve conflicts
```sh
git mergetool
```

---

#### Override local changes and checkout exactly what is in remote
```sh
git fetch origin
git reset --hard origin/current-branch
```

---

<br>
<br>

# Rebasing

#### Concept Overview
**Rebasing** is an alternative to merging that rewrites commit history by moving commits from one branch to another. Unlike merging, which preserves the original branch structure, rebasing creates a linear history by replaying commits on top of another branch. This results in a cleaner project history but should be used carefully, especially on shared branches.

---

#### Rebase current branch onto another branch
```sh
git rebase branch-name
```

---

#### Interactive rebase to edit, squash, or reorder commits
```sh
git rebase -i HEAD~3
```

---

#### Continue rebase after resolving conflicts
```sh
git rebase --continue
```

---

#### Skip current commit during rebase
```sh
git rebase --skip
```

---

#### Abort rebase and return to original state
```sh
git rebase --abort
```

---

#### Rebase onto a specific commit
```sh
git rebase --onto target-branch start-commit end-commit
```

---

#### Rebase and preserve merge commits
```sh
git rebase --preserve-merges branch-name
```

---

<br>
<br>

# Untracking Files

#### Untrack specific files
```sh
git rm --cached path/to/file.txt
```

---

#### Untrack all files in a folder
```sh
git rm --cached -r path/to/folder
```

---

#### Untrack all files in `.gitignore`
```sh
git rm -r --cached .
git add .
git commit -m "Untracked files now ignored"
```

---

#### Programmatically add single file to `.gitignore`  
```sh
echo "path/to/file.txt" >> .gitignore
```

---

#### Add multiple patterns to `.gitignore`
```sh
echo -e "*.log\n*.tmp\nnode_modules/" >> .gitignore
```

---

#### Remove file from working directory and Git
```sh
git rm file.txt
```

---

#### Remove directory from working directory and Git
```sh
git rm -r directory/
```

---

<br>
<br>

# Viewing History

#### View commit history
```sh
git log
```

---

#### View compact commit history
```sh
git log --oneline
```

---

#### View graphical commit history
```sh
git log --graph --oneline --all
```

---

#### View commit history with file changes
```sh
git log --stat
```

---

#### View detailed commit history with diffs
```sh
git log -p
```

---

#### View commits by specific author
```sh
git log --author="Author Name"
```

---

#### View commits within a date range
```sh
git log --since="2023-01-01" --until="2023-12-31"
```

---

#### View commits that modified a specific file
```sh
git log -- path/to/file.txt
```

---

#### View changes made in the last commit
```sh
git show
```

---

#### View changes in a specific commit
```sh
git show <commit-hash>
```

---

#### View changes between two commits
```sh
git diff commit-hash-1 commit-hash-2
```

---

#### View changes between branches
```sh
git diff branch1..branch2
```

---

#### View changes in working directory
```sh
git diff
```

---

#### View staged changes
```sh
git diff --staged
```

---

#### View file at a specific commit
```sh
git show commit-hash:path/to/file.txt
```

---

#### Find commits that introduced or removed a string
```sh
git log -S "search-string"
```

---

#### Search commit messages
```sh
git log --grep="search-term"
```

---

#### Show who last modified each line of a file
```sh
git blame file.txt
```

---

#### Find when a bug was introduced using binary search
```sh
git bisect start
git bisect bad
git bisect good <commit-hash>
```

---

<br>
<br>

# Tags

#### List all tags
```sh
git tag
```

---

#### Create a lightweight tag
```sh
git tag v1.0.0
```

---

#### Create an annotated tag
```sh
git tag -a v1.0.0 -m "Release version 1.0.0"
```

---

#### Tag a specific commit
```sh
git tag -a v1.0.0 <commit-hash> -m "Release version 1.0.0"
```

---

#### Show tag information
```sh
git show v1.0.0
```

---

#### Delete a local tag
```sh
git tag -d v1.0.
```
