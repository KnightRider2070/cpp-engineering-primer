# Stage 0 — Environment Setup

<StageHeader :stage="0" />

## What you'll have when this is done

A real Linux system on your Windows machine, with a C++ compiler in it, and one
program you compiled yourself.

## Before you start

Nothing. This is the beginning.

## The problem

C++ is built and debugged with a set of tools that assume a Unix-like system.
You could install a Windows-native toolchain, but then every Linux instruction
you ever read would need translating, and you would learn none of the shell
skills the job actually wants.

WSL2 gives you a genuine Ubuntu running alongside Windows, sharing your files
and your browser. You get the real thing without giving up your machine.

## Do this

### 1. Install WSL2

Open **PowerShell as Administrator** and run:

```powershell
wsl --install -d Ubuntu
```

Reboot when it asks. On first launch Ubuntu asks for a username and password —
this is a *Linux* account, unrelated to your Windows login. The password is
invisible as you type it. That is normal.

From here on, everything happens in the **Ubuntu** terminal, not PowerShell.

### 2. Install the toolchain

```bash
sudo apt update && sudo apt install -y build-essential gdb cmake git python3
```

`build-essential` is the package that brings `g++`, `make` and the standard
library headers — Ubuntu ships without a compiler.

### 3. Put the repository in your Linux home directory

```bash
cd ~
git clone https://github.com/KnightRider2070/cpp-engineering-primer.git
cd cpp-engineering-primer
chmod +x ttt
```

::: danger This one matters more than it looks
Clone into `~`, **not** into `/mnt/c/...`.

`/mnt/c` is your Windows drive seen from Linux. Every file access there crosses
between two operating systems. Builds run roughly **ten times slower**, and
file permissions behave strangely enough to break `chmod +x`.

If you have already cloned into `/mnt/c`, move it: `cp -r . ~/cpp-engineering-primer`
:::

### 4. Check the machine

```bash
./ttt doctor
```

It checks each tool, prints the version it found, and gives you the exact
command to fix anything missing.

### 5. Tell git who you are

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
```

### 6. Write your first program

Create `my-game/scratch/hello.cpp`, make it print something, then:

```bash
cd my-game/scratch
g++ -std=c++17 -Wall -Wextra -o hello hello.cpp
./hello
echo $?
```

That last line prints the **exit code** of the last command — `0` means
success. You will use it constantly.

## The shell, in six commands

| Command | What it does |
| --- | --- |
| `pwd` | where am I |
| `ls` / `ls -la` | what is here (and the hidden things) |
| `cd somewhere` / `cd ..` | go there / go up |
| `mkdir name` | make a folder |
| `cat file` | dump a file to the screen |
| `less file` | page through a long file (`q` to quit) |

Two more worth knowing now: `which g++` tells you *which* g++ you are actually
running, and `echo $?` tells you whether the last thing worked.

## Definition of done

<StageChecks :stage="0" />

## If you're stuck

<Hint :stage="0" :level="1" />
<Hint :stage="0" :level="2" />
<Hint :stage="0" :level="3" />
<Hint :stage="0" :level="4" />

Still stuck? Write an entry in `my-notes/stuck-log.md`, then `./ttt reveal 0`.

## Ask the AI

<AiPrompt :stage="0" :id="1" />

## Interview checkpoint

Write your answer in `my-notes/interview/stage-0.md`, in your own words:

> What is the difference between an *interpreter* and a *compiler*, and which
> one is `g++`? What does it produce?
