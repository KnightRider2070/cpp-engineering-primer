# When something breaks

Pages are titled with the **error you will paste into a search box**, not with
the topic. Find the one that matches what you are looking at.

| It says | Page |
| --- | --- |
| `undefined reference to ...` | [undefined reference](/help/undefined-reference) |
| `g++: command not found` | [g++ not found](/help/gpp-command-not-found) |
| `localhost:8080` refused, from Windows | [localhost refused](/help/localhost-refused-from-windows) |
| Container runs, connection refused | [container connection refused](/help/container-connection-refused) |
| `<<<<<<< HEAD` in my file | [merge conflict recovery](/help/merge-conflict-recovery) |
| It just sits there / never stops | [program hangs](/help/program-hangs) |

## First, always

```bash
./ttt doctor
```

Checks every tool, prints the versions it found, and gives you the fix command
for anything missing.

## When a check fails and you disagree

```bash
./ttt check N --explain
```

Prints what it compiled, what it typed in, and exactly what it saw. If it read
your program wrongly, that output shows how — and that is a bug in the course,
not in you.

## The reset switches

```bash
rm -rf build && cmake -S . -B build     # a confused build
./ttt exercise conflict --reset         # get out of the merge exercise
./ttt exercise reflog --reset           # get out of the reflog exercise
git merge --abort                       # abandon any merge
git restore <file>                      # throw away changes to one file
```

Nothing under `build/` is precious. Deleting it is always safe.
