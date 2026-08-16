# The contract

`course/include/ttt/Game.hpp` is the only file the course and your game agree
on. It is 45 lines. Everything else about your program is yours.

<div class="plate">
<div class="plate-title">Do not edit</div>
The tests and the web server both depend on this file looking exactly as it
does. Read it as much as you like.
</div>

## What you implement

```cpp
class Game {
public:
    virtual ~Game() = default;

    virtual Snapshot   snapshot() const = 0;   // a picture; must not change the game
    virtual MoveResult play(int cell)   = 0;   // try a move; always returns fresh state
    virtual void       reset()          = 0;   // empty board, X to play
};

std::unique_ptr<Game> createGame();            // you write this; the course calls it
```

## The data

```cpp
enum class Mark      { Empty, X, O };
enum class Player    { X, O };
enum class Status    { InProgress, Won, Draw };
enum class MoveError { None, OutOfRange, CellTaken, GameOver };

struct Snapshot {
    std::array<Mark, 9>   board{};
    Player                turn   = Player::X;
    Status                status = Status::InProgress;
    std::optional<Player> winner{};      // only when status == Won
};

struct MoveResult {
    MoveError error = MoveError::None;
    Snapshot  snapshot{};
    bool ok() const { return error == MoveError::None; }
};
```

## Cells are 0–8

```
 0 | 1 | 2
---+---+---
 3 | 4 | 5
---+---+---
 6 | 7 | 8
```

The web page shows **1–9**, because people count from one. That conversion
happens in exactly two places in the entire system: your CLI's input parser,
and nowhere else.

The browser genuinely never converts — it builds nine buttons in a
`for (let i = 0; i < 9; i++)` loop, so it already has 0–8, and merely *draws*
the label `i + 1`. Which is the lesson: 1-based numbering was never a data
problem, it was a presentation one.

## Why it looks like this

### Why a whole `Snapshot` every time, instead of "cell 4 changed"

- The browser has **one** `render(snapshot)` function used by every endpoint, so
  there is no code trying to keep a local copy in step with the server — and
  therefore no bugs in that code.
- Your C++ stays the only source of truth.
- A test can assert on one comparable value instead of replaying a stream.
- It costs nine enums. There is no performance argument here.

### Why `MoveResult` instead of throwing

An illegal move is not exceptional — it is the *expected* result of untrusted
input. Using exceptions for ordinary control flow is a classic interview
discussion, and this is a concrete example of the other side of it. It also
means you do not have to learn `try`/`catch` at Stage 4 while still getting
comfortable with `if`.

(In C++23 this would be `std::expected<Snapshot, MoveError>`. This course is
C++17, and a plain struct needs no library knowledge to read.)

### Why `enum class` and not strings or ints

A `switch` over an `enum class` **with no `default:`** makes the compiler tell
you when you forget a case (`-Wswitch`, part of `-Wall`). The compiler becomes
a checklist. Strings live at exactly one boundary — `course/server/Json.cpp` —
and that file is written to be read.

### Why `createGame()` exists at all

This is the question people actually ask, and it has a good answer:
**it is the testability seam.**

It is the one symbol that lets a test reach your entire game while knowing
nothing about it. Look at `course/checks/contract/GameContractTests.cpp` — it
includes exactly one header, `<ttt/Game.hpp>`, and never names one of your
types. That is why you get to design your own program.

## Implementing it

Your adapter should be the only file of yours that mentions `ttt::`:

```cpp
class Adapter : public ttt::Game {
public:
    ttt::Snapshot   snapshot() const override;
    ttt::MoveResult play(int cell) override;
    void            reset() override;
private:
    mygame::Game game_{};      // your types, translated at the boundary
};
```

Two traps:

**`snapshot()` must return a copy.** Not a view into your live state — a
snapshot taken before a move must not change when the move happens. There is a
test for this.

**Put `createGame()` at the bottom of your adapter's `.cpp`.** A one-function
file is a file you forget to list in `CMakeLists.txt`, and the linker error
looks like a mystery.

**A name clash to expect:** inside `class Adapter : public ttt::Game`, a bare
`Game` means the *base class* — an inherited name beats one from your own
namespace. If your own class is also called `Game`, qualify it:
`mygame::Game`. The error reads `field type 'Game' is an abstract class`.
