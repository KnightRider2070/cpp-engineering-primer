# How this course works

## The shape of it

You build one program across nine stages. Every stage leaves you with something
that runs, and each one adds C++ you did not know plus a tool you had not used.

There is no lecture. Each stage states a problem, tells you what is new, and
then gets out of the way.

## What is yours and what is not

```
my-game/     ← yours. every line of the game. starts empty.
my-notes/    ← yours. stuck log, interview answers, reviews.
course/      ← don't edit. contract, server, tests, stage content.
docs/        ← this site.
```

One rule: **do not edit anything under `course/`.** Read it — please do, reading
other people's code is half the job — but if you change it, the checks stop
meaning anything.

## The course fixes four names. Everything else is yours.

| Name | Arrives | Why |
| --- | --- | --- |
| `my-game/main.cpp` | Stage 1 | the checker must know what to compile |
| CMake target `my_game` | Stage 3 | the tests must know what to link |
| CMake target `ttt-cli` | Stage 3 | `./ttt play` must know what to run |
| `ttt::createGame()` | Stage 5 | the web server must find your game |

Plus one CLI flag, `--vs-computer`, at Stage 7.

Your classes, your members, your files, your design — never mentioned by any
test. See [the build contract](/reference/build-contract).

## One command

```bash
./ttt status              # where am I, what's next
./ttt check 3             # am I done with stage 3?
./ttt check 3 --explain   # ...and show me exactly what you tested
./ttt hint 3 1            # a nudge. levels 1-4
./ttt reveal 3            # the reference solution (gated)
./ttt play                # run your game in the terminal
./ttt serve               # run your game in a browser
./ttt prompt 3 2          # an AI prompt scoped to what you know
./ttt doctor              # is my machine set up right?
```

## How checking works

`./ttt check N` runs **stages 1 to N**, not just N. Passing stage 5 means
stages 1–4 still pass too. "Done" keeps meaning "still done".

The checks never mention your names. They:

- run your **program** and read its output (stages 1–2),
- build your **CMake targets** (stage 3+),
- call your game through **`ttt::createGame()`** (stage 5+),
- rebuild your CLI under **AddressSanitizer** (stage 6+),
- talk to your **container over HTTP** (stage 8).

And they always show their work. If something fails, `--explain` prints what it
compiled, what it typed in, and exactly what it saw.

::: tip A checker that lies is worse than no checker
Nothing in this course prints a PASS it did not earn. If it says green, it ran
something.
:::

## Hints, and why the answer is behind a gate

Four hint levels per stage:

1. **Direction** — what to think about
2. **Decomposition** — how to break it up
3. **Pseudocode** — the shape of the solution
4. **C++ specifics** — the syntax and the traps

Then `./ttt reveal N` gives you a reference solution — but only after all four
hints **and** a written entry in `my-notes/stuck-log.md`.

That is not bureaucracy. Writing down what you expected, what happened, and
what you tried is the single most effective debugging technique there is. Most
people solve the problem while writing the entry.

The gate is honest, not cryptographic: the bundles are base64, and you could
decode one in a second. That is fine. Doing so is a deliberate choice, which is
exactly the line being drawn.

## Working with an AI

Use one. It is a good tutor and a terrible ghostwriter.

`./ttt prompt <stage> <n>` gives you a prompt that tells the assistant what you
have learned so far and what you have **not** — so it cannot answer a Stage 2
question with templates and lambdas. It also asks it to question you rather
than hand over code.

See [the tutor contract](/ai/tutor-contract).

::: warning
The tests check behaviour, not code, so pasted answers usually pass. You would
be spending real time to arrive at an interview unable to explain your own
repository. The `my-notes/interview/` questions exist to catch this early —
answer them in writing, before looking anything up.
:::
