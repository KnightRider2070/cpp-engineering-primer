# Linux notes

Everything this course needs, and not much more.

## Moving around

```bash
pwd                # where am I
ls                 # what is here
ls -la             # ...including hidden files, with detail
cd some/folder     # go there
cd ..              # up one
cd ~               # home
mkdir -p a/b/c     # make folders, parents included
```

## Looking at files

```bash
cat file           # dump it
less file          # page through it (q to quit, / to search)
head -20 file      # first 20 lines
tail -20 file      # last 20 lines
grep "text" file   # lines containing text
grep -rn "text" .  # ...recursively, with line numbers
find . -name "*.cpp"
```

## Redirection and pipes

This is the part that turns the shell into a tool rather than a menu.

```bash
./game > out.txt          # stdout to a file (overwrite)
./game >> out.txt         # append
./game < moves.txt        # a file as stdin
./game 2> errors.txt      # stderr only
./game > out.txt 2>&1     # both to one file

printf '1\n5\n9\n' | ./game     # feed input straight in
./game | grep "X"               # filter output
```

Three separate streams: **stdin** (0), **stdout** (1), **stderr** (2). Errors go
to stderr precisely so that `./game > out.txt` does not swallow them.

## Exit codes

```bash
./game
echo $?        # 0 means success
```

Every command returns one. `0` is success, anything else is a failure. This is
how scripts — including `./ttt` — know whether something worked.

```bash
cmake --build build && ./build/ttt-cli    # only run if the build succeeded
```

## Processes

```bash
ps aux | grep ttt      # what is running
kill <pid>             # ask it to stop
kill -9 <pid>          # make it stop
Ctrl-C                 # stop what is in front of you
Ctrl-D                 # end of input (not the same thing)
```

`Ctrl-D` matters here: it is how you signal end-of-input to a program reading
stdin, which is what makes your Stage 2 loop finish.

## Permissions

```bash
chmod +x ttt       # make it runnable
ls -l ttt          # -rwxr-xr-x  <- the x's
```

## WSL-specific

```bash
explorer.exe .            # open this folder in Windows Explorer
code .                    # open in VS Code
some-command | clip.exe   # copy output to the Windows clipboard
```
