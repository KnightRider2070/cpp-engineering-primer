# The whole line

Nine stages. Each one leaves you with something that runs.

<StageLine />

## How they fit together

**Stages 1 and 2** are one file and one `g++` command. No classes, no build
system, nothing to configure. You are learning to write C++ and read a compiler
error, and that is enough to be going on with.

**Stage 3** is where the code becomes a project: classes, several files, and
CMake. Nothing about the game changes — that is the test.

**Stages 4 and 5** make it a real game: it survives hostile input, and it knows
when someone has won. At the end of Stage 5 it appears in a browser.

**Stages 6 and 7** go back over things you already used. You wrote a
`unique_ptr` and an `override` at Stage 5 without a full explanation; now you
find out what they were, and you build your own class hierarchy.

**Stage 8** packages the whole thing so somebody with no compiler can play it.

## Two things that are deliberate

**You use some things before they are explained.** At Stage 5 you write
`: public ttt::Game` and `override` having been told only "copy this shape".
That is on purpose. When Stage 7 explains virtual dispatch, you already have a
working example you wrote yourself, and the explanation lands on something
solid instead of hanging in the air.

**Early stages leave a mess for later stages to clean up.** Stages 2 to 5 copy
the board around by value. It works, and it is quietly wasteful. Stage 6 is
where you learn why and fix it — and the fix means something because you wrote
the version that needed fixing.

## Reading a stage page

Every stage page has the same shape:

| Section | What it is |
| --- | --- |
| **What you'll have** | the thing that exists at the end |
| **The problem** | prose only — never the code |
| **New C++** | what is new, and links to the notes |
| **Build it** | an ordered list of decisions, not instructions |
| **Definition of done** | exactly what `./ttt check N` verifies |
| **If you're stuck** | hint 1 inline; 2–4 in the terminal |
| **Interview checkpoint** | a question to answer in writing, before looking anything up |
