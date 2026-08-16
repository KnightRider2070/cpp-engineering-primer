#!/usr/bin/env python3
"""Extract a tic-tac-toe board out of arbitrary program output.

The student designs their own output. The checker still has to find the board
in it. So the course publishes a deliberately loose contract (documented for
the student at docs/reference/board-output-contract.md):

    Somewhere in your output, print the board as THREE CONSECUTIVE LINES,
    each containing EXACTLY THREE cell tokens.

    A cell token is:
        X or x          -> X
        O or o          -> O
        . _ - * # space -> empty
        1-9             -> empty (a position label on an empty cell)

    Anything else on the line (|, +, spaces) is ignored.

This accepts every plausible beginner rendering:

    . . .        1 2 3       X | O | .      X O X
    . . .        4 5 6       --+---+--      O X O
    . . .        7 8 9       . | X | O      X O X

and rejects prose ("Invalid move." has letters), prompts ("Move> " has one
token), and separator rules ("---+---+---" yields nine tokens, not three).
"""

import re
import sys

EMPTY = "."
CELL_RE = re.compile(r"[XxOo.\_\-*#1-9]")
LETTER_RE = re.compile(r"[A-Za-z]")
MARK_LETTERS = set("XxOo")
# Drawing characters used for rules between rows.
SEPARATOR_CHARS = set(" \t-+|=")


def is_separator(line):
    """True for rules like '---+---+---' that sit between board rows.

    Careful: '- - -' is a legitimate empty row, so we only treat a line as a
    separator when it is made purely of drawing characters AND uses enough of
    them that it cannot be three cells.
    """
    if not line.strip():
        return False
    if any(ch not in SEPARATOR_CHARS for ch in line):
        return False
    return sum(1 for ch in line if ch in "-+|=") >= 4


def tokens_in(line):
    """Return the normalised cell tokens on one line, or None if it can't be a board row."""
    # Any letter other than a mark means this is prose, not a board row.
    if any(ch not in MARK_LETTERS for ch in LETTER_RE.findall(line)):
        return None
    found = CELL_RE.findall(line)
    if len(found) != 3:
        return None
    out = []
    for ch in found:
        if ch in "Xx":
            out.append("X")
        elif ch in "Oo":
            out.append("O")
        else:
            out.append(EMPTY)
    return out


def find_frames(text):
    """Every board in the output, as (start_line_no, rows, raw_lines).

    Separator lines between rows are stepped over, so a board drawn as
    'X | O | .' / '---+---+---' / '. | X | O' is still one frame.
    """
    lines = text.splitlines()
    # Keep only lines that could be rows, remembering where they came from.
    candidates = [
        (i, tokens_in(ln), ln)
        for i, ln in enumerate(lines)
        if not is_separator(ln)
    ]
    frames = []
    i = 0
    while i + 2 < len(candidates) + 1:
        window = candidates[i:i + 3]
        if len(window) == 3 and all(w[1] is not None for w in window):
            frames.append({
                "line_numbers": [w[0] + 1 for w in window],   # 1-based, real
                "rows": [w[1] for w in window],
                "raw": [w[2] for w in window],
            })
            i += 3          # a frame is consumed whole; don't overlap boards
        else:
            i += 1
    return frames


def last_frame(text):
    """The final board the program printed, as a flat list of 9, or None."""
    frames = find_frames(text)
    if not frames:
        return None
    return [cell for row in frames[-1]["rows"] for cell in row]


def last_frame_detail(text):
    frames = find_frames(text)
    if not frames:
        return None
    last = frames[-1]
    return {
        "line_numbers": last["line_numbers"],
        "board": [cell for row in last["rows"] for cell in row],
        "raw": last["raw"],
    }


def render(board):
    """Render a flat board for an error message."""
    return "\n".join("    " + " ".join(board[r * 3:r * 3 + 3]) for r in range(3))


def describe(text, limit=40):
    """Human-readable account of what the checker saw. Used by --explain."""
    detail = last_frame_detail(text)
    out = []
    lines = text.splitlines()
    shown = lines[-limit:] if len(lines) > limit else lines
    if not shown:
        out.append("  (your program printed nothing at all)")
        return "\n".join(out)
    if detail is None:
        out.append("  I could not find a board in your output.")
        out.append("  I was looking for three consecutive lines with exactly three")
        out.append("  cell tokens each. Here is what you printed:")
        out.append("")
        for ln in shown:
            out.append("    | " + ln)
        return "\n".join(out)
    nums = detail["line_numbers"]
    out.append("  I found this board in your output (lines %s):"
               % ", ".join(str(n) for n in nums))
    out.append("")
    for num, raw in zip(nums, detail["raw"]):
        out.append("    line %-3d | %s" % (num, raw))
    out.append("")
    out.append("  which I read as:")
    out.append("")
    out.append(render(detail["board"]))
    return "\n".join(out)


if __name__ == "__main__":
    data = sys.stdin.read()
    print(describe(data))
    b = last_frame(data)
    print("\nflat: %r" % (b,))
