# There are `<<<<<<<` markers in my file

```
<<<<<<< HEAD
// the version on your branch
=======
// the version on the branch you are merging in
>>>>>>> exercise/tidy-the-header
```

Nothing is broken. Git is telling you that two branches changed the same lines
and it will not guess which you meant.

## What the markers mean

| Marker | Below it is |
| --- | --- |
| `<<<<<<< HEAD` | what **your current branch** says |
| `=======` | the divider |
| `>>>>>>> other` | what the **incoming branch** says |

## Resolving it

```bash
git status        # which files are "both modified"
```

Open each one and decide what it should actually say. You may keep either
version, or write a third thing — resolving is an editorial decision, not a
mechanical one.

Then **delete all three marker lines**, and:

```bash
git add <file>
git commit
cmake --build build     # make sure it still compiles
```

That last step matters. A conflict resolved into code that does not build is
very easy to commit.

## Getting out entirely

```bash
git merge --abort
```

Back to exactly where you were before the merge, as if nothing happened.

For the course exercise specifically:

```bash
./ttt exercise conflict --reset
```

## Seeing what you are choosing between

```bash
git diff                       # the conflicted regions
git log --oneline --graph --all    # how the branches diverged
git checkout --ours   <file>   # take your side wholesale
git checkout --theirs <file>   # take their side wholesale
```

The last two are blunt instruments — they discard the other side of the file
completely. Usually you want to edit by hand.

## Why the course makes you do this on purpose

Your first merge conflict should not happen at work, on a deadline, in a file
you did not write. `./ttt exercise conflict` builds one in a file **you** wrote,
that you can throw away.
