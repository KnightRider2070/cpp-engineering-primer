# gdb notes

A debugger lets you stop a program mid-run and look at it. It is much faster
than adding print statements, and unlike print statements it does not change
the program.

## Build with symbols

```bash
g++ -std=c++17 -g -O0 -o game main.cpp
```

`-g` keeps the names of your variables and functions in the binary. Without it
gdb can only show you addresses. CMake's default `Debug` build already does
this.

## A session

```bash
gdb ./build/course/exercises/exercise_outofbounds
```

```
break countMarks     # stop when this function is entered
break main.cpp:42    # or at a line
run                  # start
print i              # show a variable
print board[i]       # show an expression
next                 # next line (over function calls)
step                 # next line (into function calls)
continue             # run on to the next breakpoint
bt                   # backtrace: how did I get here
finish               # run until this function returns
quit
```

`n`, `s`, `c`, `p`, `bt` are the short forms. You will use `next`, `print` and
`bt` more than everything else combined.

## Watching a variable change

```
watch count          # stop whenever count changes
```

## When it crashes

```
run
# ... Segmentation fault
bt                   # where it died, and how it got there
frame 1              # move up the stack
print somevar        # look around
```

`bt` after a crash is the single highest-value thing gdb does.

## gdb or AddressSanitizer?

Different jobs.

- **gdb** — "what is happening right now, and what are the values?"
- **ASan** — "something touched memory it should not have; here is exactly
  where and what."

For memory bugs, reach for the sanitizer first: it points at the cause, whereas
gdb shows you the symptom.

```bash
g++ -fsanitize=address,undefined -g -o game main.cpp
```
