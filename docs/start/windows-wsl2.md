# Windows + WSL2 setup

The full walkthrough lives in [Stage 0](/stages/0-environment-setup). This page
is the short version and the fixes for when it goes wrong.

## The short version

```powershell
# PowerShell, as Administrator
wsl --install -d Ubuntu
```

Reboot. Launch **Ubuntu** (not PowerShell) and set a username and password —
the password is invisible as you type. Then:

```bash
sudo apt update && sudo apt install -y build-essential gdb cmake git python3
cd ~
git clone https://github.com/KnightRider2070/cpp-engineering-primer.git
cd cpp-engineering-primer
chmod +x ttt
./ttt doctor
```

## Work in `~`, not `/mnt/c`

::: danger
`/mnt/c` is your Windows drive seen from Linux. Every file access crosses
between two operating systems: builds are around **ten times slower** and file
permissions misbehave badly enough that `chmod +x` can silently do nothing.

`./ttt doctor` checks for this and will tell you.
:::

You can still reach your Linux files from Windows — type `\\wsl$` into Explorer,
or run `explorer.exe .` from Ubuntu.

## Useful things

| Task | How |
| --- | --- |
| Open the current folder in Explorer | `explorer.exe .` |
| Open VS Code here | `code .` (install the WSL extension) |
| Copy to the Windows clipboard | `some-command \| clip.exe` |
| Shut WSL down properly | `wsl --shutdown` in PowerShell |

`clip.exe` is worth remembering: `./ttt prompt 5 2 | clip.exe` puts an AI prompt
straight on your Windows clipboard, ready to paste into a browser.

## When it goes wrong

**`wsl --install` says it is not recognised** — you are on an older Windows 10.
Update, or follow Microsoft's manual install steps.

**Virtualisation errors** — enable virtualisation in your BIOS/UEFI. It is
usually called Intel VT-x, AMD-V, or SVM.

**Ubuntu starts and immediately closes** — run `wsl --shutdown`, then start it
again.

**`g++: command not found`** — see [that page](/help/gpp-command-not-found).
