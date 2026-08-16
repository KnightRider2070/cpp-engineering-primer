---
layout: home

hero:
  name: C++ Engineering Primer
  text: Build a game. Learn the C++ interviews ask about.
  tagline: >
    Nine stages, starting from an empty folder and one terminal. You finish with
    a Tic-Tac-Toe game you designed, playable in a browser, served by your own
    C++ backend, running in a container you wrote.
  actions:
    - theme: brand
      text: Start at Stage 0
      link: /stages/0-environment-setup
    - theme: alt
      text: How this works
      link: /start/how-this-works
    - theme: alt
      text: GitHub
      link: https://github.com/KnightRider2070/cpp-engineering-primer

features:
  - title: You design it, not us
    details: >
      my-game/ ships empty. There is no skeleton to fill in and no TODO to
      complete. The course fixes four names; every class, file and design
      decision past that is yours.
  - title: Tests that never mention your code
    details: >
      The checks run your program and reach your logic through one function.
      They do not know your class names, so they cannot dictate your design —
      and they always show you exactly what they tested.
  - title: The compiler as a teacher
    details: >
      -Wall -Wextra from the first command, gdb at Stage 4, AddressSanitizer at
      Stage 6. You learn to read what the tools are already telling you.
  - title: Hints, not answers
    details: >
      Four levels per stage, from a nudge to near-code. The reference solution
      unlocks only after all four and a written stuck-log entry — which usually
      solves it before you get there.
---

## The line

<StageLine />

## What you actually end up with

A browser tab at `localhost:8080` playing a game whose every rule you wrote,
talking over HTTP to a C++ binary you built, in a container you can hand to
anyone.

Along the way: arrays, loops, functions, classes, `const`, references,
pointers, object lifetime, `virtual`/`override`, polymorphism — and the Linux,
Git, gdb and Docker habits that surround them.

## Who this is for

Someone who can program a little, needs C++ for interviews, and would rather
build one real thing than work through a hundred exercises.

You need a Windows machine (WSL2 — [Stage 0](/stages/0-environment-setup) walks
you through it), Linux, or a Mac. No prior C++.
