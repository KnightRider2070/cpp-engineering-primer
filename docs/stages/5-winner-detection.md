# Stage 5 — Winner Detection

<StageHeader :stage="5" />

## What you'll have when this is done

A game that knows when someone has won — and a browser tab at
`http://localhost:8080` playing **your** C++.

This is the big one. Two halves: the algorithm, then the payoff.

## Before you start

- `./ttt check 4` is green
- `git switch -c stage-5`

## The problem

Right now your game will happily let both players fill all nine squares while
three X's sit in the top row, ignored. Somebody has to notice.

## Part A — winning

### New C++

<table class="tracks">
<tr><td>C++</td><td>a table of winning lines, arrays of arrays, <code>std::optional</code></td></tr>
<tr><td>Linux</td><td>GoogleTest, <code>ctest</code></td></tr>
</table>

### Build it

1. **On paper**, write down every set of three squares that wins. How many are
   there? Getting that count right is most of this stage.
2. Notice that there are two different questions hiding here, and that mixing
   them is what makes this hard:
   - which *triples of positions* are winning lines?
   - do these three squares hold the same non-empty mark?

   Write them as two separate things.
3. Decide where that list of lines lives. A member? A constant? Why?
4. Only then wire it into your move handling.
5. Do not forget the draw. A full board with no line is not a win.

::: tip A test to notice
If you find yourself typing the eighth `if` statement, stop and go back to
step 2. Eight copies of a rule is eight places to get it wrong.
:::

## Part B — the browser

Now the course needs to be able to run your game. It cannot, because it has no
idea what your classes are called.

That is what `ttt::Game` is for:

```cpp
class Adapter : public ttt::Game {
public:
    ttt::Snapshot   snapshot() const override;
    ttt::MoveResult play(int cell) override;
    void            reset() override;
};

// at the BOTTOM of the same .cpp
namespace ttt {
std::unique_ptr<Game> createGame() {
    return std::make_unique<mygame::Adapter>();
}
}
```

Read [the contract](/reference/contract) — it is 45 lines and it is the whole
agreement between you and the course.

::: warning You are about to use two things nobody has explained
`: public ttt::Game`, `override`, and `std::unique_ptr` have not been covered.

**Copy the shape anyway.** This is deliberate: Stage 6 comes back for the
pointer and Stage 7 for the virtual functions, and when they do you will
already have a working example that you wrote. An explanation landing on
something you have built beats one landing on nothing.
:::

### Three things worth getting right

**Your types stay yours.** The adapter is the only file of yours that mentions
`ttt::`. Your board, your enums, your class names never leave the building —
the adapter translates at the boundary. That separation *is* the engineering
lesson of this course: the transport layer does not get to dictate your design.

**`snapshot()` returns a copy.** Not a reference into your live state. If it
handed out a view, anyone holding it would watch the board change underneath
them. There is a test for exactly this.

**Put `createGame()` at the bottom of your adapter's `.cpp`**, not in a file of
its own. A one-function file is a file you forget to add to `CMakeLists.txt`,
and the linker error that follows looks like a mystery.

### Then

```bash
./ttt check 5
./ttt serve
```

Open `http://localhost:8080` in your normal Windows browser — WSL2 forwards the
port automatically. If it does not:
[localhost refused](/help/localhost-refused-from-windows).

## Code review exercise

```bash
./ttt exercise review
```

Somebody else's win detection, submitted as a pull request. It compiles. It
passes its author's test. It is wrong in at least three ways, and one of them
reads memory that does not belong to it.

Write your findings, *then* `./ttt exercise review --answer`.

Reading code for bugs is a different skill from writing it — and it is most of
what a technical interview actually is.

## Definition of done

<StageChecks :stage="5" />

## If you're stuck

<Hint :stage="5" :level="1" />
<Hint :stage="5" :level="2" />
<Hint :stage="5" :level="3" />
<Hint :stage="5" :level="4" />

Still stuck? Write an entry in `my-notes/stuck-log.md`, then `./ttt reveal 5`.

## Ask the AI

<AiPrompt :stage="5" :id="2" />
<AiPrompt :stage="5" :id="3" />

## Interview checkpoint

In `my-notes/interview/stage-5.md`, **before** looking anything up:

> Why is a table of winning lines better than eight `if` statements? What does
> it cost you?

## Going further

- Make the winning line highlight in the browser. (The server already sends
  everything you need. Does it? Check.)
- Add a draw counter to the page.
