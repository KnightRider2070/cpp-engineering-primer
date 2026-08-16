#!/usr/bin/env bash
# Stage 3 exercise: a real merge conflict, in a file you actually wrote.
#
# Not a fixture copied over the top of your work -- an honest three-way merge
# that git genuinely cannot resolve, in your own code, so that `git status`,
# `git diff` and `git log` all show you something real.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 1

BRANCH_A="exercise/tidy-the-header"
STATE="$ROOT/.primer/conflict-origin"

bold() { printf '\033[1m%s\033[0m\n' "$*"; }
dim()  { printf '\033[2m%s\033[0m\n' "$*"; }

if [[ "${1:-}" == "--reset" ]]; then
    if [[ ! -f "$STATE" ]]; then
        echo "No conflict exercise in progress."
        exit 0
    fi
    origin="$(cat "$STATE")"
    git merge --abort 2>/dev/null
    git checkout -- . 2>/dev/null
    git switch --force "$origin" 2>/dev/null || git switch --force -c "$origin" 2>/dev/null
    git branch -D "$BRANCH_A" 2>/dev/null
    rm -f "$STATE"
    echo "Reset. You are back on '$origin' with your work as it was."
    exit 0
fi

# --- sanity ------------------------------------------------------------------
if ! git rev-parse --git-dir >/dev/null 2>&1; then
    echo "This is not a git repository yet." >&2
    exit 1
fi
if ! git rev-parse HEAD >/dev/null 2>&1; then
    echo "You have no commits yet. Commit your Stage 3 work first:" >&2
    echo "    git add my-game && git commit -m 'my game so far'" >&2
    exit 1
fi
if [[ -n "$(git status --porcelain my-game 2>/dev/null)" ]]; then
    echo "You have uncommitted changes in my-game/." >&2
    echo "Commit them first -- this exercise rewrites branches and you do not" >&2
    echo "want to lose work:" >&2
    echo "    git add my-game && git commit -m 'my game so far'" >&2
    exit 1
fi

# Pick one of the student's own header files.
TARGET="$(git ls-files 'my-game/*.hpp' | head -1)"
if [[ -z "$TARGET" ]]; then
    TARGET="$(git ls-files 'my-game/*.cpp' | head -1)"
fi
if [[ -z "$TARGET" ]]; then
    echo "No committed files in my-game/ yet. Reach Stage 3 first." >&2
    exit 1
fi

ORIGIN="$(git rev-parse --abbrev-ref HEAD)"
printf '%s' "$ORIGIN" > "$STATE"

bold "Setting up a merge conflict in $TARGET"
echo

# --- branch A: a comment header ---------------------------------------------
git switch -c "$BRANCH_A" >/dev/null 2>&1 || { echo "Could not create branch." >&2; exit 1; }

tmp="$(mktemp)"
{
    echo "// ---------------------------------------------------------------"
    echo "// $(basename "$TARGET") -- part of my tic-tac-toe game"
    echo "// Written during Stage 3."
    echo "// ---------------------------------------------------------------"
    cat "$TARGET"
} > "$tmp"
mv "$tmp" "$TARGET"
git add "$TARGET" >/dev/null
git commit -q -m "docs: add a file header to $(basename "$TARGET")"

# --- back to their branch: a DIFFERENT header at the same lines --------------
git switch -q "$ORIGIN"
tmp="$(mktemp)"
{
    echo "// $(basename "$TARGET")"
    echo "// TODO: tidy this up before Stage 6"
    cat "$TARGET"
} > "$tmp"
mv "$tmp" "$TARGET"
git add "$TARGET" >/dev/null
git commit -q -m "docs: note something to revisit in $(basename "$TARGET")"

# --- the merge ---------------------------------------------------------------
echo
if git merge "$BRANCH_A" >/dev/null 2>&1; then
    echo "git merged that cleanly, which is not what this exercise wanted."
    echo "Run:  ./ttt exercise conflict --reset   and tell the course author."
    exit 1
fi

bold "Done. You now have a real merge conflict."
echo
echo "Both branches added a comment block to the top of $TARGET, and git"
echo "cannot know which one you meant."
echo
bold "Your job"
echo "  1. git status                  -- see which file is 'both modified'"
echo "  2. open $TARGET"
echo "     and find the <<<<<<< ======= >>>>>>> markers"
echo "  3. decide what the top of that file should actually say"
echo "     (you may keep either version, or write a third -- that is the point:"
echo "      resolving is an editorial decision, not a mechanical one)"
echo "  4. delete every marker line"
echo "  5. git add $TARGET"
echo "  6. git commit"
echo "  7. ./ttt check 3               -- it must still build and pass"
echo
dim "Stuck or want out:  ./ttt exercise conflict --reset"
