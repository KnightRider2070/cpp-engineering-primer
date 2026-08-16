# Stage 8 — Containerize It

<StageHeader :stage="8" />

## What you'll have when this is done

One command that runs your game on any machine with Docker — no compiler, no
CMake, no idea what C++ is required:

```bash
docker run --rm -p 8080:8080 my-ttt
```

That is the thing you put on a CV.

## Before you start

- `./ttt check 7` is green
- Docker Desktop installed, with **WSL2 integration** switched on
  (Settings → Resources → WSL Integration → enable your Ubuntu)
- `docker run hello-world` works **from inside Ubuntu**
- `git switch -c stage-8`

## The problem

Your game currently runs on exactly one machine: yours, after `apt install`,
`cmake`, and a build. Handing it to somebody else means handing them all of
that.

A container is that whole environment, packaged.

**The course does not give you a Dockerfile.** You write it.

## New concepts

<table class="tracks">
<tr><td>Docker</td><td>image vs container vs registry, build context, layer caching and ordering, multi-stage builds, <code>EXPOSE</code> vs <code>-p</code>, non-root, <code>HEALTHCHECK</code></td></tr>
<tr><td>Git</td><td><code>git tag -a</code>, writing a README a stranger will read</td></tr>
</table>

## Image, container, registry

- An **image** is a filesystem plus a command to run. It does not run. Think
  class, or executable file.
- A **container** is a running instance of an image. Think object, or process.
  You can start ten from one image.
- A **registry** is where images are stored and shared (Docker Hub, ghcr.io).

`docker build` makes an image. `docker run` makes a container from it.

## Build it

1. Work out which base image you need, and what has to be installed on it to
   compile your program.
2. Then ask the question this whole stage turns on: **once the program is
   built, does the image still need the compiler?**
3. Copy files in an order that does not defeat the layer cache.
4. Run as somebody other than root.
5. Add a `HEALTHCHECK` against `/api/health`.

```bash
docker build -t my-ttt .
docker run --rm -p 8080:8080 my-ttt
docker ps
docker logs <id>
docker images          # compare your image size
```

## Multi-stage, and why your image is 1 GB otherwise

The build needs `g++`, `cmake` and `make`. The finished program needs the C++
standard library and nothing else. A single-stage image ships an entire
toolchain to everyone who runs your game.

Two `FROM` lines fix it: build in the first, copy only the finished binary into
the second.

```dockerfile
FROM ubuntu:24.04 AS build
# ... install toolchain, copy source, build ...

FROM ubuntu:24.04 AS run
COPY --from=build /src/build/.../ttt-server /app/ttt-server
```

The reference solution comes out around **32 MB**. The check requires under
150 MB, which is not a suggestion you can talk your way around.

## Layer order is a performance decision

Docker caches every instruction and rebuilds from the first one whose inputs
changed. So this:

```dockerfile
COPY CMakeLists.txt ./
COPY course/ ./course/
COPY my-game/ ./my-game/
RUN cmake -S . -B build && cmake --build build
```

is not the same as copying everything at once. Get the order wrong and every
one-character edit re-runs the entire build.

## `.dockerignore` is not optional

Docker sends the **whole build context** — your entire folder — to the daemon
before the build starts. Without `.dockerignore`, that includes `build/`:
hundreds of megabytes of object files, transferred just to be ignored.

Write it, then delete it and watch `docker build` get slower. That is the
lesson landing.

## The one that gets everybody

Your container starts. `docker ps` looks healthy. `localhost:8080` says
**connection refused**.

`127.0.0.1` means "only accept connections that started on this machine".
Inside a container, *this machine* is the container. `-p 8080:8080` forwards
traffic to the container's network interface — which a process bound to
127.0.0.1 is not listening on.

The server must bind **`0.0.0.0`**. The course's server already does: go and
read the last few lines of `course/server/Main.cpp`, where there is a comment
explaining exactly this. Now you know why it is there.

Full write-up: [container connection refused](/help/container-connection-refused).

## `EXPOSE` versus `-p`

`EXPOSE 8080` is documentation. It publishes nothing. `-p 8080:8080` on
`docker run` is what actually forwards the port. Both are useful; only one does
anything.

## Definition of done

<StageChecks :stage="8" />

The check builds your image, runs it, talks to it over HTTP, plays a move,
checks the user, and measures the image. It never looks at your source — it is
the most name-agnostic test in the course, because it does not even need to
know the program is C++.

## If you're stuck

<Hint :stage="8" :level="1" />
<Hint :stage="8" :level="2" />
<Hint :stage="8" :level="3" />
<Hint :stage="8" :level="4" />

Still stuck? Write an entry in `my-notes/stuck-log.md`, then `./ttt reveal 8`.

## Ask the AI

<AiPrompt :stage="8" :id="1" />
<AiPrompt :stage="8" :id="2" />

## Finish it properly

```bash
git tag -a v1.0.0 -m "tic-tac-toe: cli, web and container"
```

Then write a README for `my-game/` aimed at somebody who has never seen the
project: what it is, how to run it, and one paragraph on how it is put
together. You will be glad of it when someone asks you to talk about something
you have built.

## Interview checkpoint

In `my-notes/interview/stage-8.md`:

> Explain the difference between an image and a container to someone who has
> never used Docker. Then explain why a multi-stage build exists.

## You're done

Nine stages. A game you designed, a CLI, a web UI, a container, and a repository
with your own commits, merge conflicts, and code reviews in its history.

Go back and read `my-notes/interview/` end to end. That is your material for
"tell me about something you built".
