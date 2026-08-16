# Your first run

```bash
cd ~/cpp-engineering-primer
./ttt doctor
```

`doctor` checks your compiler, CMake, git identity, python3, gdb, Docker and the
repository itself, printing the version it actually found for each. Anything
missing comes with the command to fix it.

Then:

```bash
./ttt status
```

```
C++ ENGINEERING PRIMER

  [o]-[.]-[.]-[.]-[.]-[.]-[.]-[.]-[.]
   0   1   2   3   4   5   6   7   8

Current stage: 0 -- Environment Setup

Objective
  Get a working Linux toolchain on your Windows machine...

Done when
  - g++ 11 or newer is installed and on your PATH.
  ...

Next
  ./ttt check 0
```

The line across the top is the course. `#` is passed, `o` is where you are,
`.` is ahead of you.

## Then what

Go to [Stage 0](/stages/0-environment-setup) and work down the page. When
`./ttt check 0` is green it moves you on by itself.

## If a check fails

Read what it says — it names the specific thing that did not hold. Then:

```bash
./ttt check 0 --explain
```

which additionally prints what it compiled, what input it used, and what it
actually saw. If you disagree with the verdict, that output is where to look
first.
