# My program never stops

Either it sits there doing nothing, or it prints the same thing forever, or
`./ttt check` reports that it stopped your program for running away.

`Ctrl-C` to get out.

## The usual cause: `while (true)` with `std::cin`

```cpp
while (true) {
    std::cin >> shown;      // fails silently when input runs out
    // ... and round we go, forever
}
```

When input ends, `std::cin >> shown` **fails and leaves `shown` unchanged**.
With `while (true)` nothing notices.

```cpp
while (std::cin >> shown) { ... }
```

The stream converts to `false` when the read fails, so the loop ends by itself.

This is also how the course tests your program: it pipes moves in and expects
the program to finish when they run out.

## The other cause: bad input, not cleared

Someone types `abc`. The read fails and the stream stays in a **failed state** —
every later read fails instantly, without consuming anything. The offending text
is still sitting in the buffer.

```cpp
if (!(std::cin >> shown)) {
    if (std::cin.eof()) break;      // input ended: stop
    std::cin.clear();               // clear the failure flag
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    continue;
}
```

Miss `clear()` and every later read fails. Miss `ignore()` and the same text
fails again immediately. Either way you loop forever.

## Reproduce it deliberately

```bash
printf '1\n5\n9\n' | ./build/.../ttt-cli    # should end on its own
printf 'abc\n' | ./build/.../ttt-cli        # should recover, then end
```

If either hangs, you have found it. `Ctrl-C`, then fix.

## "it printed more than 8 MB"

That is the checker telling you your program ran away. It stops it as soon as
the output makes the conclusion obvious rather than waiting for the full
timeout — the flood *is* the diagnosis.

## A game loop that never ends

Separately: your loop should also stop when the game is over.

```cpp
while (board.snapshot().status == ttt::Status::InProgress && ...)
```

Otherwise a finished game keeps asking for moves and refusing all of them.
