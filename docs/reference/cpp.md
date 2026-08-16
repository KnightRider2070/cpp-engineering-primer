# C++ notes

Short notes on the things this course uses, in the order you meet them. Not a
tutorial — a place to check something you half-remember.

## Arrays

```cpp
char board[9];                    // nine chars, uninitialised: GARBAGE
char board[9] = {};               // nine chars, all zero
std::array<char, 9> board{};      // same, but knows its own size
```

`std::array` is the same thing with `.size()`, bounds-checked `.at()`, and no
decaying to a pointer when passed to a function. Prefer it once you have met it.

Indexing past the end is **undefined behaviour**. Not an error, not an
exception — anything at all may happen, including appearing to work.

## Functions

```cpp
int  cellFromHumanInput(int shown);        // takes a copy, returns an int
void printBoard(const Board& board);       // no copy, cannot modify
void applyMove(Board& board, int cell);    // no copy, CAN modify
```

Rule of thumb: `const&` for anything bigger than a pointer that you only read;
plain `&` when you intend to change it; by value for small things or when you
genuinely want your own copy.

## `const` on a member function

```cpp
Square at(int cell) const;    // promises not to modify the object
```

The compiler enforces it. It is also what makes `const Board&` useful — without
`const` members, a const reference can barely be used.

## `enum class`

```cpp
enum class Square { Empty, Cross, Nought };
Square s = Square::Empty;
```

Better than a plain `enum` because the names do not leak into the surrounding
scope and it will not silently convert to `int`.

The payoff is the `switch`:

```cpp
switch (s) {
    case Square::Empty:  ...
    case Square::Cross:  ...
    case Square::Nought: ...
}   // NO default: -- so the compiler warns if you forget one
```

## `std::optional`

```cpp
std::optional<Player> winner;      // maybe there is one, maybe not
if (winner) use(*winner);
winner.reset();
```

For "there might not be an answer". Better than a sentinel like `-1` or
`Empty`, because the absence is part of the type and the compiler reminds you.

## References and pointers

|  | Reference `T&` | Pointer `T*` |
| --- | --- | --- |
| Can be null | no | yes |
| Must be initialised | yes | no |
| Can be re-pointed | no | yes |
| Access | `.` | `->` |

Use a reference when the thing definitely exists. Use a pointer when "nothing"
is a legal answer, or when ownership is being handed over.

## `std::unique_ptr`

```cpp
auto game = ttt::createGame();     // owns the object
ttt::Game& g = *game;              // a reference to it
game.reset();                      // destroys it now
```

One owner. Destroyed automatically when it goes out of scope. It cannot be
copied — only moved — which is exactly what "one owner" means.

## Inheritance and `virtual`

```cpp
class Player {
public:
    virtual ~Player() = default;                 // ESSENTIAL
    virtual int chooseMove(const Board&) const = 0;   // = 0: pure virtual
};

class RandomPlayer : public Player {
public:
    int chooseMove(const Board&) const override;      // override: checked
};
```

- `= 0` makes it **pure virtual**: no body, and the class becomes abstract.
- `override` costs nothing at runtime and catches a wrong signature at compile
  time. Without it, a mistyped override silently becomes a new function that is
  never called.
- **The virtual destructor is not optional.** Delete a derived object through a
  base pointer without one, and only the base destructor runs.

## Slicing

```cpp
std::vector<Player> players;                    // wrong: derived parts sliced off
std::vector<std::unique_ptr<Player>> players;   // right
```

Polymorphism works through pointers and references only.

## Compiler, linker, runtime

- **Compiler error** — this text does not make sense. One file at a time.
- **Linker error** — this makes sense, but something it refers to does not exist
  anywhere. Usually a `.cpp` missing from `CMakeLists.txt`.
- **Runtime error** — it built, and then went wrong while running.

Knowing which of the three you are looking at cuts most debugging time in half.
