# `localhost:8080` refused, from Windows

You ran `./ttt serve`, it says the game is running, and your Windows browser
says it cannot connect.

## First: is it actually running?

In the Ubuntu terminal where you started it, you should see:

```
Your game is running.
  Open http://localhost:8080
```

If instead you got a build error, the server never started. The most likely
cause is that `ttt::createGame()` is not implemented yet — that arrives at
Stage 5.

## Check from inside Linux first

```bash
curl -s localhost:8080/api/health
```

- **`{"ok":true}`** — the server is fine, so this is a WSL networking problem.
  Keep reading.
- **Connection refused** — the server is not running. Look at the terminal you
  started it in.

## WSL2 usually forwards localhost automatically

It normally just works. When it does not, try these in order.

**1. Restart WSL.** Fixes it most of the time. In PowerShell:

```powershell
wsl --shutdown
```

Then reopen Ubuntu and `./ttt serve` again.

**2. Use the WSL machine's own IP.** From Ubuntu:

```bash
hostname -I | awk '{print $1}'
```

Then open `http://<that-address>:8080` in Windows.

**3. Check nothing else has the port.**

```bash
ss -tlnp | grep 8080
```

If something else is on 8080:

```bash
./build/course/server/ttt-server --web-root course/web --port 8090
```

**4. Windows firewall.** Rare for localhost, but if you are on a locked-down
machine it may be blocking the forward. Try a different port first.

## Not related to Docker

If you are at Stage 8 and the *container* is refusing connections, that is a
different problem with a different cause — see
[container connection refused](/help/container-connection-refused).
