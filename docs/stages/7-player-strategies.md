# Stage 7 — Player Strategies

<StageHeader :stage="7" />

## What you'll have when this is done

An opponent. `./ttt play --vs-computer` and the machine answers your moves —
and it is genuinely hard to beat.

## Before you start

- `./ttt check 6` is green
- `git switch -c stage-7`

## The problem

You want three kinds of opponent: a human at the same keyboard, one that plays
anywhere, and one that actually tries.

You could write one function with a `switch` in it. Then adding a fourth kind
means editing that function, and the choosing logic for all four sits in one
place, tangled together.

The alternative is the reason `virtual` exists.

## New C++ in this stage

<table class="tracks">
<tr><td>C++</td><td>pure virtual functions, <code>override</code>, <strong>virtual destructors</strong>, object slicing, <code>vector&lt;unique_ptr&lt;T&gt;&gt;</code>, seeded <code>mt19937</code>, <code>final</code></td></tr>
<tr><td>Linux</td><td>writing your <em>own</em> GoogleTest cases, <code>ctest -R</code></td></tr>
<tr><td>Git</td><td>reviewing your own diff before anyone else does</td></tr>
</table>

## Build it

This is the **second** interface you have met, and the first you design. At
Stage 5 you implemented one somebody handed you; this one is yours.

1. Every strategy answers the same question — *given this board, where do you
   want to play?* — differently. Write that sentence down as a function
   signature.
2. Your base class has no sensible default answer, so its function has no body.
   Look up what `= 0` does, and what it makes the class.
3. Implement three: human, random, and one that takes an immediate win, blocks
   an immediate loss, and otherwise prefers the centre.
4. Add `--vs-computer` to your CLI. The course checks for that exact flag.
5. Write your own tests.

## Three things that will bite you

### The virtual destructor

```cpp
class Player {
public:
    virtual ~Player() = default;    // not decoration
    virtual int chooseMove(...) const = 0;
};
```

Delete a `BlockingPlayer` through a `Player*` without that, and **only
`~Player` runs**. The derived part is never destroyed. Today your strategies
have no members and you may leak nothing at all — right up until someone adds a
`std::vector` to one, and then it leaks quietly forever.

**Rule: if a class is meant to be inherited from and deleted through a base
pointer, its destructor is virtual.** Expect to be asked this.

### What `override` actually buys you

Nothing at runtime. At compile time it checks you really are overriding
something.

Try it: write your derived function with a slightly wrong signature — drop the
`const`, or take the snapshot by value. Without `override` it compiles fine,
and you have quietly created a brand-new function that nobody ever calls. Your
strategy silently does nothing. With `override`, it will not build.

### Slicing

```cpp
std::vector<Player> players;                    // wrong: slices everything
std::vector<std::unique_ptr<Player>> players;   // right
```

Polymorphism only works through a pointer or a reference. Store derived objects
by value in a base-typed container and the derived parts are shaved off.

## Make the randomness testable

```cpp
std::mt19937 rng{12345};        // a fixed seed
```

The same game now plays out identically every time. Randomness you cannot
reproduce is randomness you cannot test — and that is a choice you made, not a
fact of life.

## Why the opponent is not inside `createGame()`

You might expect to put the computer inside your adapter, so the web UI gets an
opponent too. Don't — and the reason is a real API design lesson.

The course's contract tests drive **both** players by hand to check win
detection, draws and turn order. They cannot do that if O answers
automatically. Putting the opponent inside `createGame()` would break every one
of those tests.

So the opponent lives in the CLI, behind a flag, and `ttt::createGame()` stays
a two-player game. Generalised: **do not bake a policy into an interface that
other callers need to control.**

## Write your own tests

For the first time, the course cannot test this for you — it does not know your
class names. Set up positions and assert what your strategy does:

```cpp
TEST(BlockingPlayer, BlocksAnImmediateLoss) {
    // X X .      <- X wins at cell 2 unless O takes it
    // O . .
    // . . .
    EXPECT_EQ(player.chooseMove(position("XX.O....."), ttt::Player::O), 2);
}
```

Register them with `add_test()` so `ctest` runs them. The check verifies your
tests exist and pass — not what they contain. Whether they are *good* tests is
between you and the self-review.

## Self-review

```bash
./ttt exercise self-review
```

Writes your whole diff into a review template with a checklist. Read it as
though a stranger wrote it and you have to approve it. Find at least one thing
you would change — if you find nothing, you are not looking.

## Definition of done

<StageChecks :stage="7" />

## If you're stuck

<Hint :stage="7" :level="1" />
<Hint :stage="7" :level="2" />
<Hint :stage="7" :level="3" />
<Hint :stage="7" :level="4" />

Still stuck? Write an entry in `my-notes/stuck-log.md`, then `./ttt reveal 7`.

## Ask the AI

<AiPrompt :stage="7" :id="2" />
<AiPrompt :stage="7" :id="3" />

## Interview checkpoint

In `my-notes/interview/stage-7.md` — these three come up constantly:

> 1. What is a vtable, and when does it get used?
> 2. Why does a base class need a virtual destructor?
> 3. What is object slicing, and how would you cause it by accident?
