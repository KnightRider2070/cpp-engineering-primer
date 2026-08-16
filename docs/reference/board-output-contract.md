# Board output contract

Stages 1 and 2 are checked by running your program and reading what it prints.
So the checker has to be able to find the board in your output — while leaving
you free to draw it however you like.

The rule is deliberately loose:

> Somewhere in your output, print the board as **three consecutive lines**, each
> containing **exactly three cell tokens**.

A cell token is:

| Token | Means |
| --- | --- |
| `X` or `x` | X |
| `O` or `o` | O |
| `.` `_` `-` `*` `#` or a space | empty |
| `1`–`9` | empty (a position label) |

Anything else on the line — `|`, `+`, spaces — is ignored. Lines made only of
drawing characters (`---+---+---`) are treated as rules **between** rows and
stepped over.

If your program prints several boards, the checker uses the **last** one.

## All of these work

```
. . .        1 2 3       X | O | .       XOX
. . .        4 5 6      ---+---+---      OXO
. . .        7 8 9       . | X | O       XOX
```

## What gets rejected, and why

- `Invalid move.` — contains letters other than X and O, so it is prose.
- `Move> ` — one token, not three.
- `---+---+---` on its own — a rule, not a row.

That is the whole trick: a line with any letter that is not `X`, `x`, `O` or `o`
cannot be a board row.

## Seeing what the checker saw

```bash
./ttt check 1 --explain
```

```
  I found this board in your output (lines 12, 13, 14):

    line 12  | X | O | .
    line 13  | . | X | O
    line 14  | . | . | X

  which I read as:

    X O .
    . X O
    . . X
```

If it read your board wrongly, that output tells you exactly how — and it is a
bug in the checker, not in you. Say so.
