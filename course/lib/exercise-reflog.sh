#!/usr/bin/env bash
# Stage 6 exercise: lose a commit, then get it back.
#
# Everyone does this to themselves eventually, usually at the worst moment.
# Doing it once deliberately, on a throwaway commit, is worth more than reading
# five pages about it.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 1

STATE="$ROOT/.primer/reflog-origin"

bold() { printf '\033[1m%s\033[0m\n' "$*"; }
dim()  { printf '\033[2m%s\033[0m\n' "$*"; }

if [[ "${1:-}" == "--reset" ]]; then
    if [[ -f "$STATE" ]]; then
        origin="$(cat "$STATE")"
        git switch --force "$origin" 2>/dev/null
        rm -f "$STATE" "$ROOT/my-notes/LOST-NOTE.md"
        echo "Reset. You are back on '$origin'."
    else
        echo "No reflog exercise in progress."
    fi
    exit 0
fi

if ! git rev-parse HEAD >/dev/null 2>&1; then
    echo "You need at least one commit before you can lose one." >&2
    exit 1
fi
if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
    echo "Commit or stash your changes first -- this exercise moves HEAD around." >&2
    exit 1
fi

ORIGIN="$(git rev-parse --abbrev-ref HEAD)"
printf '%s' "$ORIGIN" > "$STATE"

# Make a commit somewhere it is easy to "lose": on a detached HEAD.
git switch -q --detach

cat > my-notes/LOST-NOTE.md <<'MD'
# The commit you are about to lose

This file exists only inside one commit, made on a detached HEAD.

If you switch away from here without writing down the commit id, nothing in
`git log` or `git branch` will mention it ever existed. It is still in the
repository -- git does not delete commits for a fortnight or so -- but you have
no name for it any more.

Getting it back is what `git reflog` is for.
MD

git add my-notes/LOST-NOTE.md >/dev/null
git commit -q -m "notes: a commit that is about to go missing"
LOST="$(git rev-parse --short HEAD)"

# Walk away from it.
git switch -q --force "$ORIGIN"

echo
bold "You just lost a commit."
echo
echo "While your HEAD was detached you made a commit containing"
echo "my-notes/LOST-NOTE.md, and then switched back to '$ORIGIN'."
echo
echo "That commit is not on any branch now. Check for yourself:"
echo
echo "    git log --oneline -5        # not there"
echo "    ls my-notes/                # LOST-NOTE.md is gone"
echo
bold "Get it back"
echo "  1. git reflog"
echo "     Every position HEAD has held, most recent first. Find the entry"
echo "     for the commit whose message mentions going missing."
echo "  2. git show <that-id>"
echo "     Confirm it is the right one before you do anything with it."
echo "  3. Give it a name so it stops being lost:"
echo "         git switch -c rescued <that-id>"
echo "     or bring just that change onto your branch:"
echo "         git cherry-pick <that-id>"
echo
dim "The commit you are looking for is $LOST -- but try to find it with"
dim "git reflog first. Finding it is the entire exercise."
echo
dim "Want out:  ./ttt exercise reflog --reset"
echo
