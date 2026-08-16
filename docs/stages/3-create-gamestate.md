# Stage 3 — Create GameState

<StageHeader :stage="3" />

## What you'll have when this is done

The same game, behaving identically, built by CMake out of several files with
your own classes in them.

**Identical behaviour is the point.** The check re-runs every Stage 2 test
against your new code.

## Before you start

- `./ttt check 2` is green
- `git switch -c stage-3`

## The problem

Your `main.cpp` now holds the board, the turn, the drawing and the rules all at
once. It still fits on a screen, but only just.

The question this stage asks is: **what are the things in this program?** Not
"how do I write a class" — that is syntax, and you can look it up. Deciding
what deserves to *be* a class is the actual skill.

## New C++ in this stage

<table class="tracks">
<tr><td>C++</td><td><code>struct</code> vs <code>class</code>, member variables and functions, constructors, <code>const</code> member functions, <code>#pragma once</code>, splitting headers from sources, your own <code>enum class</code></td></tr>
<tr><td>Linux</td><td>CMake, out-of-source builds, <strong>compiler errors versus linker errors</strong></td></tr>
<tr><td>Git</td><td>a real merge conflict, in a file you wrote</td></tr>
</table>

## Build it

1. Write down the things your program remembers between moves. That list is
   your state.
2. Decide whether the board and the rules are one type or two, and be able to
   say why. Both are defensible.
3. Decide what an empty square is. `char` works. A `enum class` of your own
   works better and the compiler starts helping you.
4. Split into headers (`.hpp`) and sources (`.cpp`). A header says what exists;
   a source says what it does.
5. Write `my-game/CMakeLists.txt`. The course needs two target names —
   everything else is yours:

```cmake
add_library(my_game Board.cpp Game.cpp)     # your file names
target_include_directories(my_game PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(my_game PUBLIC ttt_contract)
target_compile_options(my_game PRIVATE -Wall -Wextra)

add_executable(ttt-cli main.cpp)
target_link_libraries(ttt-cli PRIVATE my_game)
```

6. Build it:

```bash
cmake -S . -B build
cmake --build build
```

The `build/` folder holds everything the compiler generates. It is
gitignored, and you can delete it at any time — that is what "out-of-source
build" means, and it is why `rm -rf build` is a safe first move when something
is behaving strangely.

## The error you are about to hit

Add a second `.cpp` and forget to list it in `add_library(...)`. You get:

```
undefined reference to `Board::place(int, Square)'
```

::: tip This is a linker error, not a compiler error, and the difference is worth knowing
- The **compiler** reads one file at a time. It saw your declaration in the
  header, believed you, and moved on. No complaint.
- The **linker** then tries to assemble all those pieces into one program, goes
  looking for the *body* of that function, and cannot find it.

So: "this text does not make sense" is a compiler error. "This makes sense, but
the thing it refers to does not exist anywhere" is a linker error.

Nine times out of ten at this stage, the cause is a `.cpp` missing from
`CMakeLists.txt`. Full details: [undefined reference](/help/undefined-reference).
:::

## Git exercise — a real merge conflict

```bash
git add my-game && git commit -m "stage 3: classes and cmake"
./ttt exercise conflict
```

This builds a genuine three-way merge conflict in a header **you wrote**, so
`git status`, `git diff` and the conflict markers all refer to your own code.
Resolve it, commit it, and make sure it still builds.

`./ttt exercise conflict --reset` puts everything back if you want out.

## Definition of done

<StageChecks :stage="3" />

## If you're stuck

<Hint :stage="3" :level="1" />
<Hint :stage="3" :level="2" />
<Hint :stage="3" :level="3" />
<Hint :stage="3" :level="4" />

Still stuck? Write an entry in `my-notes/stuck-log.md`, then `./ttt reveal 3`.

## Ask the AI

<AiPrompt :stage="3" :id="1" />
<AiPrompt :stage="3" :id="2" />

## Interview checkpoint

In `my-notes/interview/stage-3.md`:

> What does `const` at the end of a member function promise, and who enforces
> that promise?
