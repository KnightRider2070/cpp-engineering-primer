# C++ Engineering Primer

Build a Tic-Tac-Toe game from an empty folder. Learn the C++ that interviews
actually ask about — loops, functions, classes, `const`, references, pointers,
`virtual`/`override` — plus the Linux, Git, and Docker skills that surround it.

Nine stages. By the end you have a game you designed, playable in a browser,
served by your own C++ backend, running in a container you wrote.

## Start here

```bash
./ttt doctor
```

That checks your machine and tells you what to fix. Then:

```bash
./ttt status
```

Everything else you need is at **[the course site](https://knightrider2070.github.io/cpp-engineering-primer/)**,
or in `docs/` if you'd rather read it locally.

## What's in here

| Folder | Whose is it? |
| --- | --- |
| `my-game/` | **Yours.** Every line of the game. Starts empty. |
| `my-notes/` | **Yours.** Stuck log, interview answers, code reviews. |
| `course/` | Don't edit. The contract, the web server, the tests, the stage content. |
| `docs/` | The course site. |

The one rule: **anything under `course/` is off-limits.** You can read it —
please do, reading other people's code is half the job — but if you change it,
the tests stop meaning anything.

## The one command

```bash
./ttt status          # where am I, what's next
./ttt check 3         # am I done with stage 3? (re-runs stages 1-3)
./ttt check 3 --explain   # ...and show me exactly what you tested
./ttt hint 3 1        # nudge, not answer. levels 1-4, increasingly direct
./ttt reveal 3        # the reference solution. gated on purpose.
./ttt play            # run your game in the terminal
./ttt serve           # run your game in a browser
./ttt prompt 3 2      # an AI prompt tuned to what you know so far
```

## Requirements

Windows with **WSL2 + Ubuntu** (Stage 0 walks you through it), or any Linux
or macOS box. You need `g++` 11+, `cmake` 3.22+, `git`, and `python3`.
Docker arrives at Stage 8, not before.

## A note on the tests

The tests never mention your class names, your file names, or your design.
They check what your program *does*, not how you wrote it — which is why you
get to design the thing yourself. See `docs/reference/build-contract.md` for
the four names the course does pin down, and why.
