# Stage 4 — Validate Moves + Errors

<StageHeader :stage="4" />

## What you'll have when this is done

A game that cannot be broken by anything typed at it. Numbers off the board,
squares already taken, letters instead of digits, input stopping mid-game — all
handled, all explained to the player.

## Before you start

- `./ttt check 3` is green
- `git switch -c stage-4`

## The problem

Right now a bad move is probably ignored in silence. The player types `99`,
nothing happens, and they have no idea why.

Two jobs, then: **notice** that a move is impossible, and **say which kind of
impossible it was.**

## New C++ in this stage

<table class="tracks">
<tr><td>C++</td><td>returning a reason instead of a <code>bool</code>, <code>switch</code> over <code>enum class</code>, <code>-Wswitch</code>, early return, recovering <code>std::cin</code></td></tr>
<tr><td>Linux</td><td>your first <code>gdb</code> session, compiling with <code>-g</code>, reading warnings as information</td></tr>
<tr><td>Git</td><td><code>git add -p</code>, commit messages with a subject and a body</td></tr>
</table>

## Build it

1. List every distinct way a move can fail. There are three or four. Write them
   down before writing code.
2. Notice that `bool` cannot carry that list. It can say "no" but not "why
   not", and "why not" is exactly what the player needs.
3. Make that list a type of your own — an `enum class`.
4. Decide the **order** of your checks. Playing square 99 after the game has
   already ended is both off-the-board *and* after-the-end. Something has to
   win. Whichever you choose, choose it on purpose.
5. Handle non-numeric input (below).
6. Turn on `-Werror` for your targets and let the compiler hold you to it:

```cmake
target_compile_options(my_game PRIVATE -Wall -Wextra -Werror)
```

## The switch with no default

```cpp
switch (error) {
    case Refusal::OffTheBoard:  ...
    case Refusal::AlreadyTaken: ...
}   // no default:
```

Leave `default:` out, and if you forget a case the compiler tells you
(`-Wswitch`, included in `-Wall`). Add `default:` and you throw that away —
adding a fifth enumerator later would compile cleanly and quietly do the wrong
thing.

The course's own `course/server/Json.cpp` is written this way. Go and look: it
is four `switch` statements, none with a `default:`, for exactly this reason.

## When someone types "abc"

```cpp
if (!(std::cin >> shown)) {
    if (std::cin.eof()) break;          // input ended: stop
    std::cin.clear();                   // clear the failure flag
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    std::cout << "That is not a number.\n";
    continue;
}
```

Two different failures land in the same branch and need opposite responses.

- **End of input** — nothing left. Stop.
- **Bad text** — the stream is now in a *failed state*, and every later read
  fails instantly until you `clear()` it. The offending text is also still
  sitting in the buffer, which is what `ignore()` throws away.

Miss `clear()` and every later read fails. Miss `ignore()` and the same text
fails again immediately. Either way: infinite loop. Most self-taught C++
programmers have never been told this.

## Your first gdb session

```bash
cmake --build build --target exercise_outofbounds
gdb ./build/course/exercises/exercise_outofbounds
```

Then, inside gdb:

```
break countMarks     # stop when we get there
run                  # start it
print i              # look at a variable
next                 # one line at a time
print board[i]       # what are we actually reading?
bt                   # how did we get here?
continue             # let it run
```

The bug is one character. Find it with the debugger rather than by staring —
the tool is the point, not the bug.

## Definition of done

<StageChecks :stage="4" />

The checker types this at your program: `0`, `10`, `-1`, `abc`, `5`, `5`, `99`,
a blank line, `4`. Exactly two of those are legal.

## If you're stuck

<Hint :stage="4" :level="1" />
<Hint :stage="4" :level="2" />
<Hint :stage="4" :level="3" />
<Hint :stage="4" :level="4" />

Still stuck? Write an entry in `my-notes/stuck-log.md`, then `./ttt reveal 4`.

## Ask the AI

<AiPrompt :stage="4" :id="1" />
<AiPrompt :stage="4" :id="2" />

## Interview checkpoint

In `my-notes/interview/stage-4.md`:

> Why return an error value instead of throwing an exception here? Give one
> argument for each side.
