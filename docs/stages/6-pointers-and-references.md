# Stage 6 — Pointers & References

<StageHeader :stage="6" />

## What you'll have when this is done

An understanding of the code you already wrote — and a CLI that drives the game
through `ttt::Game`, exactly like the web server does. One code path, two front
ends.

## Before you start

- `./ttt check 5` is green
- `git switch -c stage-6`

## The problem

At Stage 5 you wrote this and were told to copy the shape:

```cpp
std::unique_ptr<Game> createGame() {
    return std::make_unique<mygame::Adapter>();
}
```

Now: **why a pointer at all?** Why can't `createGame()` just return a `Game`?

That question opens onto the part of C++ that interviews care about most, and
that most self-taught programmers stay vague about: what object exists, where
it lives, and how long it stays valid.

## New C++ in this stage

<table class="tracks">
<tr><td>C++</td><td><code>&amp;</code> vs <code>*</code>, value vs <code>const&amp;</code>, <code>-&gt;</code> vs <code>.</code>, <code>nullptr</code>, <code>std::unique_ptr</code>, object lifetime, stack vs heap</td></tr>
<tr><td>Linux</td><td><strong>AddressSanitizer</strong>, gdb on a broken program</td></tr>
<tr><td>Git</td><td><code>reflog</code>, recovering a lost commit, <code>stash</code>, <code>restore</code></td></tr>
</table>

## Why it cannot return by value

`ttt::Game` is **abstract** — it has pure virtual functions and no
implementation. You cannot make one. And even if you could, returning your
`Adapter` as a `Game` by value would **slice** it: the derived part copied away,
leaving only the base.

So `createGame()` has to return something that *refers* to your object. A raw
pointer would work and put you in charge of remembering `delete`.
`std::unique_ptr` does the same job and cannot be forgotten.

## Reference or pointer?

- A **reference** is another name for an object that already exists. It must be
  bound when it is created, can never be re-bound, and cannot be null.
- A **pointer** is a variable holding an address. It can be null, and it can be
  pointed somewhere else later.

Use a reference when the thing definitely exists. Use a pointer when "nothing"
is a legal answer, or when ownership is changing hands.

```cpp
auto game = ttt::createGame();   // unique_ptr: owns the object
ttt::Game& board = *game;        // reference: it definitely exists
board.play(4);                   // a dot, not an arrow
```

## Paying off some debt

Since Stage 2 you have been passing the board around **by value** — copying the
whole thing on every call. It worked, and it kept things simple while you had
other problems.

It is also wasteful, and now you can see it:

```cpp
void show(const Board& b);        // no copy, and show() cannot modify it
void apply(Board& b, int cell);   // no copy, and apply() CAN modify it
Board copyOf(Board b);            // a copy -- occasionally what you want
```

Print `&board` inside and outside a by-value function. Different addresses. That
is the copy, made visible.

Go through everything from Stage 2 onward and decide, per parameter: does this
function need to *change* it, only *read* it, or genuinely want its own copy?

## See a dangling reference die

```bash
cmake --build build --target exercise_dangling exercise_dangling_asan
./build/course/exercises/exercise_dangling
./build/course/exercises/exercise_dangling_asan
```

Watch the order of events:

1. **The compiler already warned you** during the build.
   (`warning: reference to stack memory associated with local variable`)
2. **The plain build does not crash.** It prints an empty string where it should
   print `cell #4`. Not an error — just quietly wrong.
3. **The sanitizer names the culprit**: `stack-use-after-return`, with the exact
   variable, function and line.

Step 2 is the lesson. Undefined behaviour is under no obligation to look
broken. It can work perfectly on your machine for a year and fail in front of
the person you were trying to impress.

## Rewrite the CLI through the contract

Your `main.cpp` currently talks to your own classes. Change it to go through
`ttt::createGame()` and the three methods on `ttt::Game`.

That is not busywork: after it, your terminal game and your browser game run
the *same* code path, so a bug can no longer hide in one and not the other.

## Git exercise — losing a commit and getting it back

```bash
./ttt exercise reflog
```

You will make a commit on a detached HEAD, walk away from it, and watch it
vanish from `git log`. Then get it back with `git reflog`.

Everyone does this to themselves eventually, always at the worst moment. Doing
it once on purpose, safely, is worth five pages of documentation.

## Definition of done

<StageChecks :stage="6" />

The sanitizer check is the one to note: your CLI gets rebuilt with
`-fsanitize=address,undefined`, played through a whole game, and must exit
clean. It verifies your pointer discipline without naming a single one of your
types.

## If you're stuck

<Hint :stage="6" :level="1" />
<Hint :stage="6" :level="2" />
<Hint :stage="6" :level="3" />
<Hint :stage="6" :level="4" />

Still stuck? Write an entry in `my-notes/stuck-log.md`, then `./ttt reveal 6`.

## Ask the AI

<AiPrompt :stage="6" :id="1" />
<AiPrompt :stage="6" :id="3" />

## Interview checkpoint

In `my-notes/interview/stage-6.md`:

> A function returns a reference to a local variable. Explain precisely what is
> wrong — what object existed, where, and for how long.
