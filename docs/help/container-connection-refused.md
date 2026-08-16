# Container runs, but connection refused

```bash
docker run --rm -p 8080:8080 my-ttt
# ... starts fine, docker ps shows it running
curl localhost:8080/api/health
# curl: (56) Recv failure: Connection reset by peer
```

This is the single most common first-Docker problem, and the cause is worth
understanding rather than just fixing.

## The cause

Your server is probably listening on **`127.0.0.1`**.

`127.0.0.1` means *"only accept connections that started on this machine"*.

Inside a container, **this machine is the container.** A container has its own
network namespace, so its `127.0.0.1` is not your `127.0.0.1`. When you pass
`-p 8080:8080`, Docker forwards traffic to the container's network interface —
which a process bound to 127.0.0.1 is deliberately not listening on.

So the port forward works perfectly and delivers to a door nobody is watching.

## The fix

Bind `0.0.0.0` — "accept connections on every interface":

```cpp
server.listen("0.0.0.0", 8080);
```

The course server already does this. Open `course/server/Main.cpp`, go to the
bottom, and there is a comment explaining exactly this. Now you know why it is
there.

## If you are not writing the bind address

Then check the other candidates:

**Is `-p` actually there?** `docker run my-ttt` without `-p 8080:8080` publishes
nothing. `EXPOSE` in the Dockerfile does **not** publish a port — it is
documentation.

**Is the port right on both sides?** `-p 18080:8080` means host 18080 → container
8080. If your server listens on 9000 inside, the second number must be 9000.

**Did the program die immediately?**

```bash
docker ps -a          # is it actually up, or exited?
docker logs <id>      # what did it say on the way out
```

A missing `--web-root`, or a path that does not exist inside the image, will
stop the server on startup.

**Is the web root inside the image?** Paths in `CMD` are container paths, not
host paths. If you `COPY --from=build /src/course/web /app/web`, then the flag
must say `/app/web`.

## Look inside

```bash
docker exec -it <id> sh
ls /app
```

Being able to open a shell inside a running container is the debugging move
that makes Docker stop feeling like a black box.
