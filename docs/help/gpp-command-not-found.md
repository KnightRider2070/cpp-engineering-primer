# `g++: command not found`

```
bash: g++: command not found
```

## Fix

```bash
sudo apt update
sudo apt install -y build-essential
```

`build-essential` is the package that brings `g++`, `make` and the standard
library headers. Ubuntu ships without a compiler.

Then check:

```bash
which g++
g++ --version
```

## If you are in PowerShell

Look at your prompt. If it says `PS C:\>` you are in **Windows PowerShell**, not
Ubuntu — there is no `g++` there and there is not meant to be.

Open the **Ubuntu** app from the Start menu, or type `wsl` in PowerShell.

## While you are there

The course also wants:

```bash
sudo apt install -y gdb cmake git python3
```

Then `./ttt doctor` confirms the lot.

## `cmake: command not found`

Same thing: `sudo apt install -y cmake`. If the version is older than 3.22,
Ubuntu 24.04 or newer will have a current one.
