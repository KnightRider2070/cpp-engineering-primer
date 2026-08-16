#!/usr/bin/env bash
# Course-author tool. Packs authoring/reference/stage-NN/ into the committed
# base64 bundles that `ttt reveal` reads.
#
#   ./course/lib/build-reference.sh
#
# Why base64 rather than plaintext: the gate is social, not cryptographic. The
# student can decode it in one command, and that is fine -- doing so is a
# deliberate act, which is exactly the line the stuck-log is drawing. What this
# buys is that nobody stumbles onto an answer while grepping the repo.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC="$ROOT/authoring/reference"
OUT="$ROOT/course/reference"

[[ -d "$SRC" ]] || { echo "No authoring/reference/ -- nothing to pack." >&2; exit 1; }
mkdir -p "$OUT"

for n in 0 1 2 3 4 5 6 7 8; do
    padded="$(printf '%02d' "$n")"
    dir="$SRC/stage-$padded"
    if [[ ! -d "$dir" ]]; then
        echo "skip  stage $padded (no $dir)"
        continue
    fi

    {
        echo "==============================================================="
        echo " Stage $n reference"
        echo "==============================================================="
        echo
        [[ -f "$dir/EXPLANATION.md" ]] && cat "$dir/EXPLANATION.md"
        echo
        for file in "$dir"/*; do
            base="$(basename "$file")"
            [[ "$base" == "EXPLANATION.md" ]] && continue
            [[ -f "$file" ]] || continue
            echo
            echo "--- $base ---------------------------------------------------"
            echo
            cat "$file"
        done
    } | gzip -9 | base64 > "$OUT/stage-$padded.b64"

    printf 'ok    stage %s -> course/reference/stage-%s.b64 (%s bytes)\n' \
        "$padded" "$padded" "$(wc -c < "$OUT/stage-$padded.b64" | tr -d ' ')"
done
