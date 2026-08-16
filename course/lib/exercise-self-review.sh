#!/usr/bin/env bash
# Stage 7 exercise: review your own diff the way a reviewer would.
#
# Before anyone else reads your code, you read it. This is the habit that
# separates "it works on my machine" from "I am confident in this".
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 1

NOTES="$ROOT/my-notes/reviews/stage-7.md"
BASE="${1:-main}"

bold() { printf '\033[1m%s\033[0m\n' "$*"; }
dim()  { printf '\033[2m%s\033[0m\n' "$*"; }

if ! git rev-parse HEAD >/dev/null 2>&1; then
    echo "No commits yet -- nothing to review." >&2
    exit 1
fi

mkdir -p "$(dirname "$NOTES")"

# What has changed in my-game since the base?
if git rev-parse --verify "$BASE" >/dev/null 2>&1; then
    DIFF="$(git diff "$BASE"...HEAD -- my-game 2>/dev/null)"
    RANGE="$BASE...HEAD"
else
    DIFF="$(git diff HEAD~5..HEAD -- my-game 2>/dev/null || git diff -- my-game)"
    RANGE="the last few commits"
fi

if [[ -z "$DIFF" ]]; then
    echo "No changes in my-game/ to review against '$BASE'." >&2
    echo "Pass a different base:  ./ttt exercise self-review <branch-or-commit>" >&2
    exit 1
fi

{
    echo "# Self-review — Stage 7"
    echo
    echo "Reviewing my own changes across $RANGE."
    echo
    echo "Go through the checklist honestly. The point is to find at least one"
    echo "thing you would change -- if you find nothing, you are not looking."
    echo
    echo "## Checklist"
    echo
    echo "- [ ] Does every class have one clear responsibility I can state in a sentence?"
    echo "- [ ] Does my abstract base class have a **virtual destructor**? Can I say why it matters here?"
    echo "- [ ] Is every method that does not modify state marked \`const\`?"
    echo "- [ ] Am I passing anything big by value that should be \`const&\`?"
    echo "- [ ] Is \`override\` on every overriding function?"
    echo "- [ ] Is there logic written twice that should exist once?"
    echo "- [ ] Would a stranger understand my names without asking me?"
    echo "- [ ] Do my tests cover the cases that actually matter (taking a win, blocking a loss), or only the easy ones?"
    echo "- [ ] Is there anything here I would be embarrassed to explain in an interview?"
    echo
    echo "## What I would change"
    echo
    echo "1. "
    echo "2. "
    echo
    echo "## What I am happy with, and why"
    echo
    echo "1. "
    echo
    echo "---"
    echo
    echo "## The diff"
    echo
    echo '```diff'
    echo "$DIFF"
    echo '```'
} > "$NOTES"

echo
bold "Self-review ready"
echo
echo "Your diff has been written into:"
echo "    $NOTES"
echo
echo "Work through the checklist at the top and fill in the two sections at the"
echo "bottom. Read the diff as though somebody else wrote it and you have to"
echo "approve it."
echo
dim "This is what reviewing a pull request feels like, minus the pull request."
echo
