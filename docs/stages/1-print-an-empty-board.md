# Stage 1 — Print an Empty Board

<StageHeader :stage="1" />

## What you'll have when this is done

A program that prints this and exits:

```
. . .
. . .
. . .
```

One file. One `g++` command. No classes, no CMake, nothing to configure.

## Before you start

- `./ttt check 0` is green
- `git switch -c stage-1`

## The problem

A tic-tac-toe board is nine squares, and you need somewhere to keep them and a
way to draw them.

That is the whole stage — and it already contains the first real design
decision of the course: **what shape is a board?** Nine separate variables? An
array of nine? Three rows of three? They all work. They are not all equally
easy to loop over, and they are not all equally easy to hand to somebody else
later.

## New C++ in this stage

<table class="tracks">
<tr><td>C++</td><td>arrays and how to initialise them, nested <code>for</code> loops, <code>std::cout</code>, <code>'\n'</code> versus <code>std::endl</code></td></tr>
<tr><td>Linux</td><td>compiling by hand, <code>-o</code>, running <code>./game</code>, redirecting with <code>&gt;</code></td></tr>
<tr><td>Git</td><td><code>switch -c</code>, <code>add</code>, <code>commit</code>, <code>log --oneline</code>, <code>diff</code></td></tr>
</table>

See the [C++ notes](/reference/cpp) for anything unfamiliar.

## Build it

1. Decide how you are storing nine squares, and be able to say why.
2. Decide what an empty square looks like when printed. The checker accepts
   `.` `_` `-` `*` `#`, a space, or a digit — a digit is a nice touch, because
   it doubles as a label showing which number to type.
3. Write the loops. Getting from a (row, column) pair to a position in a flat
   array is the one line worth staring at.
4. Compile it **by typing the command yourself**, at least the first few times:

```bash
g++ -std=c++17 -Wall -Wextra -o game main.cpp
./game
```

`-o game` names the output. Leave it off and you get a file called `a.out` —
which is a 1970s default that has never gone away.

5. Prove you can capture it:

```bash
./game > board.txt
cat board.txt
```

## About those warning flags

`-Wall -Wextra` turn on the warnings that are off by default. Use them from the
very first command, every time.

The reason is not tidiness. The compiler already knows about most of the
mistakes you are about to make, and it will only mention them if you ask. Turn
warnings on later and you meet fifty at once, which means you read none of
them.

## Your first compiler error

Delete a semicolon on purpose and compile. You will get something like:

```
main.cpp:8:34: error: expected ';' before '}' token
```

Read it as three parts: **file**, **line:column**, **complaint**. And learn the
most important habit right now — when there are twenty errors, **fix the first
one and recompile.** The rest are usually the compiler losing its footing after
the first.

## Definition of done

<StageChecks :stage="1" />

## If you're stuck

<Hint :stage="1" :level="1" />
<Hint :stage="1" :level="2" />
<Hint :stage="1" :level="3" />
<Hint :stage="1" :level="4" />

Still stuck? Write an entry in `my-notes/stuck-log.md`, then `./ttt reveal 1`.

## Ask the AI

<AiPrompt :stage="1" :id="1" />
<AiPrompt :stage="1" :id="2" />

## Commit it

```bash
git add my-game
git commit -m "stage 1: print an empty board"
git log --oneline
```

You have probably just committed the compiled `game` binary too. That is fine —
you will find it and fix it at Stage 2, which is a better way to learn what
`.gitignore` is for than being told.

## Interview checkpoint

Write your answer in `my-notes/interview/stage-1.md` **before** looking
anything up:

> You chose a way to store the board. Name one thing that choice makes easy and
> one thing it makes harder.
