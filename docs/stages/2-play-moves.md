# Stage 2 — Play Moves

<StageHeader :stage="2" />

## What you'll have when this is done

A game two people can actually play at one keyboard. Type a number, a mark
appears, the other player's turn.

Still one file. Still no build system.

## Before you start

- `./ttt check 1` is green
- `git switch -c stage-2`

## The problem

Three new things at once: read a number from the keyboard, put the right mark
in the right square, and keep going until there is nowhere left to play.

The interesting part is the third. **When does the program stop?**

## New C++ in this stage

<table class="tracks">
<tr><td>C++</td><td>writing your own functions, parameters and return values, <code>std::cin</code>, <code>while</code>, <code>if</code>/<code>else</code>, <code>bool</code></td></tr>
<tr><td>Linux</td><td>piping input with <code>|</code>, here-docs, redirecting with <code>&lt;</code>, <code>.gitignore</code></td></tr>
<tr><td>Git</td><td><code>commit --amend</code>, <code>diff --staged</code>, <code>rm --cached</code></td></tr>
</table>

## Build it

1. Pull the board-printing out into a function. You are about to call it after
   every move; you do not want that code twice.
2. Decide how a move gets applied, and what happens when it cannot be.
3. Write the input loop. Read the warning below before you choose its shape.
4. Handle the numbering. The player types **1–9** because that is how people
   count squares; your array runs **0–8**. Do that subtraction in exactly one
   place, in a function with a name.

::: danger The bug almost everyone writes first
```cpp
while (true) {
    std::cin >> shown;     // fails silently when input runs out
    // ... and now this loops forever
}
```

When there is no more input, `std::cin >> shown` **fails and leaves `shown`
unchanged**. Nothing notices, and the program spins printing the same board
until you kill it.

```cpp
while (std::cin >> shown) { ... }
```

The stream converts to `false` when the read fails, so the loop ends by itself.

This is also how the course tests your program: it pipes moves in and expects
the program to finish. If it does not, the check reports a runaway rather than
waiting forever — but either way, you have a bug.
:::

## Driving your own program from the shell

Typing nine moves by hand every time you rebuild gets old immediately:

```bash
printf '1\n5\n9\n3\n' | ./game
```

Or keep a file of moves:

```bash
cat > moves.txt <<'EOF'
1
5
9
EOF
./game < moves.txt
```

This is the moment `|` and `<` stop being trivia. They are how you test.

## That binary you committed

`git status` almost certainly shows the compiled `game`. Compiled output does
not belong in git — it is machine-specific, it is large, and it changes on
every build.

```bash
echo "game"  >> .gitignore
echo "*.out" >> .gitignore
git rm --cached game
git add .gitignore
git commit -m "stop tracking the compiled binary"
```

`git rm --cached` removes it from git while leaving the file on disk. If you
had used plain `git rm` you would have deleted your program.

## Definition of done

<StageChecks :stage="2" />

## If you're stuck

<Hint :stage="2" :level="1" />
<Hint :stage="2" :level="2" />
<Hint :stage="2" :level="3" />
<Hint :stage="2" :level="4" />

Still stuck? Write an entry in `my-notes/stuck-log.md`, then `./ttt reveal 2`.

## Ask the AI

<AiPrompt :stage="2" :id="1" />
<AiPrompt :stage="2" :id="2" />

## Interview checkpoint

In `my-notes/interview/stage-2.md`:

> What does `std::cin >> x` actually return, and why can you put it directly in
> a `while` condition?

## Going further

Nothing here is checked — but if the game is fun to play now, it will be much
more fun at Stage 5.

- Print which player's turn it is.
- Stop when the board is full rather than waiting for input to run out.
