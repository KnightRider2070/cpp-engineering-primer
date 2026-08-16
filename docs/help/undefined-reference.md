# `undefined reference to ...`

```
/usr/bin/ld: main.cpp.o: in function `main':
main.cpp:(.text+0x1a): undefined reference to `mygame::Board::place(int, Square)'
collect2: error: ld returned 1 exit status
```

## What it means

**This is a linker error, not a compiler error**, and that distinction is the
whole fix.

- The **compiler** reads one `.cpp` at a time. It saw your declaration in the
  header, believed you that a body existed somewhere, and moved on happily.
- The **linker** then tries to assemble all the pieces into one program. It goes
  looking for that body, and cannot find it.

So the message is not "you wrote this wrong". It is "you promised me this
function exists and I cannot find it".

## The cause, nine times out of ten

You created a new `.cpp` and did not add it to `my-game/CMakeLists.txt`:

```cmake
add_library(my_game
    Board.cpp
    Game.cpp
    Adapter.cpp    # <-- the one you just created and forgot
)
```

Add it, then:

```bash
cmake -S . -B build && cmake --build build
```

## The other causes

**You declared it but never wrote it.** The header says
`void place(int, Square);` and no `.cpp` has a `Board::place` in it.

**The signature does not match.** The header says `place(int, Square)`, the
`.cpp` defines `place(int, Square) const`, or takes a `Square&`. To the linker
those are different functions. Compare them character by character.

**You forgot the class qualifier.** In the `.cpp` it must be
`void Board::place(...)`, not `void place(...)` — the second one defines a
brand-new free function, and `Board::place` still does not exist.

**A namespace mismatch.** Declared inside `namespace mygame`, defined outside
it.

## For `ttt::createGame`

```
undefined reference to `ttt::createGame()'
```

You have not implemented it yet (it arrives at Stage 5), or it is not in a file
listed in `CMakeLists.txt`, or you defined it outside `namespace ttt`. It must
be exactly:

```cpp
namespace ttt {
std::unique_ptr<Game> createGame() {
    return std::make_unique<mygame::Adapter>();
}
}
```

Put it at the bottom of your adapter's `.cpp` — a one-function file is a file
you forget to list.

## Why this is worth knowing properly

This is one of the most common C++ interview questions, phrased as "what is the
difference between a compiler error and a linker error?". You now have a real
answer, from a bug you actually had.
