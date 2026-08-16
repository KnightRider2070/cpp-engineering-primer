# This folder is yours

Everything in here is code **you** write. The course never edits it.

Right now it's empty except for this file. That's on purpose — there is no
skeleton to fill in, no `// TODO` to complete. You build the game, and you
decide what it looks like.

Start here:

```bash
./ttt status
```

## What the course will and won't tell you

The course fixes exactly **four** names. Everything else is your call.

| Name | Arrives at | Why it's fixed |
| --- | --- | --- |
| `my-game/main.cpp` | Stage 1 | the checker has to know what to compile |
| CMake target `my_game` | Stage 3 | the tests have to know what to link |
| CMake target `ttt-cli` | Stage 3 | `./ttt play` has to know what to run |
| `ttt::createGame()` | Stage 5 | the web server has to find your game |

That's it. Your classes, your structs, your member names, your other file
names, how you store the board, how you track whose turn it is — none of that
is the course's business, and no test will ever mention them.

If you want to call your board class `Grid`, call it `Grid`. If you want to
store the board as nine `char`s, or as a `std::array<Mark, 9>`, or as three
rows of three, that's a real design decision and it's yours to make.

## A warning about copying

You will be tempted to ask an AI to write a stage for you. The course is built
to make that unsatisfying: the tests check *behaviour*, not code, so a pasted
answer will usually pass — and you'll have learned nothing, in a course whose
only purpose is the interview you're preparing for.

Use `./ttt prompt <stage> <n>` instead. Those prompts are written to make an
assistant ask you questions rather than hand you code.
