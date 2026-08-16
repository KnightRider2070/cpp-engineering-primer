#!/usr/bin/env bash
# Stage 5 exercise: review somebody else's win detection.
#
# Reviewing code you did not write is a distinct skill from writing it, and it
# is most of what you do on a team. The file under review is course-owned, so
# your own repository stays clean.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SUBJECT="$ROOT/course/exercises/review/board.hpp"
MODEL="$ROOT/course/exercises/review/MODEL-REVIEW.md"
NOTES="$ROOT/my-notes/reviews/stage-5.md"

bold() { printf '\033[1m%s\033[0m\n' "$*"; }
dim()  { printf '\033[2m%s\033[0m\n' "$*"; }

if [[ "${1:-}" == "--answer" ]]; then
    # Count findings the student actually filled in: a non-empty, non-heading
    # line somewhere under a "**What:**" prompt. Checking the file is merely
    # non-empty would pass the blank template, since the template itself is
    # full of prose.
    filled=0
    if [[ -f "$NOTES" ]]; then
        filled="$(awk '
            /^\*\*What:\*\*/            { grab = 1; next }
            /^\*\*Why it matters:\*\*/  { grab = 0 }
            /^---/                      { grab = 0 }
            grab && NF                  { count++ }
            END                         { print count + 0 }
        ' "$NOTES")"
    fi

    if (( filled < 2 )); then
        echo
        echo "Not yet -- write your own review first."
        echo
        echo "  $NOTES"
        echo
        echo "I found $filled filled-in finding(s); you need at least 2."
        echo "Write under the **What:** headings."
        echo
        dim "Reading someone else's findings before forming your own teaches you"
        dim "nothing except that you agree with them."
        exit 1
    fi
    echo
    bold "Model review"
    dim "Yours does not have to match. Look for things you missed, and things"
    dim "you found that this list does not mention."
    echo
    cat "$MODEL"
    exit 0
fi

mkdir -p "$(dirname "$NOTES")"
if [[ ! -f "$NOTES" ]]; then
    cat > "$NOTES" <<'MD'
# Code review — course/exercises/review/board.hpp

Reviewing: "add win detection"

Write one finding per block. For each one say WHAT is wrong, WHY it matters,
and HOW you would fix it. Be specific about lines -- "the loop is wrong" is not
a review comment, "the row loop steps one cell at a time so it matches 1-2-3,
which spans two rows" is.

---

### Finding 1

**What:**

**Why it matters:**

**Suggested fix:**

---

### Finding 2

**What:**

**Why it matters:**

**Suggested fix:**

---

### Finding 3

**What:**

**Why it matters:**

**Suggested fix:**

---

## Would you approve this pull request?

MD
fi

echo
bold "Code review exercise"
echo
echo "Read this file:"
echo "    $SUBJECT"
echo
echo "It compiles. It passes the one test its author wrote. It is still wrong"
echo "in at least three separate ways, and one of them reads memory that does"
echo "not belong to it."
echo
echo "Write your findings here:"
echo "    $NOTES"
echo
dim "Do not run it, and do not fix it. Read it. Finding bugs by reading is the"
dim "skill being practised -- it is also most of what a technical interview is."
echo
echo "When you are done:  ./ttt exercise review --answer"
echo
