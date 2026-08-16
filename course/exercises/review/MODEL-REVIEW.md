# Model review — `board.hpp`

Compare this with what you wrote. You do not have to have found all of them,
and you may well have found something here that this list misses.

---

### 1. `is_winner` reads past the end of the array — **crash / undefined behaviour**

```cpp
for (int i = 0; i <= 8; i++) {
    if (cells[i] == 'X' && cells[i + 1] == 'X' && cells[i + 2] == 'X')
```

When `i` is 7, it reads `cells[9]`. When `i` is 8, it reads `cells[9]` and
`cells[10]`. The array has nine elements, indices 0–8. This is out-of-bounds
memory access: it may return garbage, it may crash, it may appear to work for
months.

Severity: highest. This is the one that gets a "request changes".

### 2. `is_winner` reports wins that do not exist — **logic error**

Even with the bounds fixed, the row loop walks `i` one cell at a time, so it
happily matches cells 1-2-3, which spans two rows:

```
 . X X
 X . .
 . . .
```

That is not a win, and this code says it is. Rows start at 0, 3 and 6 only.

### 3. Diagonals are missing entirely — **incomplete**

Rows and columns are checked. `0-4-8` and `2-4-6` are not. Two of the eight
winning lines simply do not exist as far as this code is concerned.

### 4. `is_valid_move` accepts position 9 — **off-by-one**

```cpp
if (pos < 0 || pos > 9) return false;
```

`pos > 9` lets 9 through. Valid indices are 0–8, so this must be `pos >= 9`
(or `pos > 8`). Then `cells[9]` is read on the next line — another
out-of-bounds access, from the function whose entire job is preventing exactly
that.

### 5. It can only ever detect X winning — **design**

The name `is_winner` promises more than it delivers; it is really `is_x_winner`.
O can never win. Either rename it or, better, take the mark as a parameter and
have one function serve both players.

### 6. Neither method is `const` — **API design**

`is_valid_move` and `is_winner` do not modify anything, so both should be
`const`. As written you cannot ask a `const Board&` whether it has a winner,
which makes the type painful to pass around.

### 7. `char cells[9]` is uninitialised until `clear()` is called — **lifetime**

A freshly constructed `Board` holds nine arbitrary bytes. Nothing forces anyone
to call `clear()` first. A constructor, or a default member initialiser, would
make the type impossible to misuse.

### 8. The eight lines are implicit — **maintainability**

The winning lines are spread across hand-written loops rather than written
down. Compare with a table of eight triples: the rule exists once, is trivially
verifiable by eye, and adding the diagonals is two lines of data rather than
another loop.

---

## What to take from this

Bugs 1 and 4 are the kind that a sanitizer finds in seconds and a reader can
miss for months. Bugs 2 and 3 are the kind no tool will ever find for you —
they need someone who knows what the code is *supposed* to do.

That is the argument for code review, in one file.
