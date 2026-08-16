# Git notes

## The loop you will use constantly

```bash
git status                    # what has changed
git diff                      # ...in detail, unstaged
git add my-game               # stage it
git diff --staged             # what you are about to commit
git commit -m "message"       # commit it
git log --oneline             # history
```

## Branching

```bash
git switch -c stage-3         # new branch
git switch main               # move to an existing one
git branch                    # list
```

Each stage suggests a branch. It is not required, but it makes
`git diff main...HEAD` meaningful at Stage 7.

## Undoing things

| You want to | Command |
| --- | --- |
| discard unstaged changes to a file | `git restore file` |
| unstage a file, keep the changes | `git restore --staged file` |
| fix the last commit message | `git commit --amend` |
| add a forgotten file to the last commit | `git add file && git commit --amend --no-edit` |
| put changes aside for a moment | `git stash` then `git stash pop` |
| stop tracking a file, keep it on disk | `git rm --cached file` |

## Merge conflicts

```
<<<<<<< HEAD
what is on your branch
=======
what is on the branch you are merging
>>>>>>> other-branch
```

Edit the file so it says what it *should* say — you may keep either side or
write a third thing — then delete all three marker lines, `git add` it, and
`git commit`.

`git merge --abort` backs out entirely.

Practise on a real one: `./ttt exercise conflict`.

## When you have lost something

```bash
git reflog                    # everywhere HEAD has been
git switch -c rescued <id>    # give a lost commit a name
git cherry-pick <id>          # bring just that change here
```

Git keeps unreferenced commits for around two weeks. Almost nothing committed is
ever truly lost — but you have to know `reflog` exists.

Practise: `./ttt exercise reflog`.

## Staging part of a file

```bash
git add -p
```

Walks you through each change and asks whether to stage it. Use it to keep
unrelated changes in separate commits.

## Tags

```bash
git tag -a v1.0.0 -m "first working version"
git tag
```
