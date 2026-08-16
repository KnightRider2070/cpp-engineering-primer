# Docker notes

## The three words

- **Image** — a filesystem plus a command. Does not run. Like a class.
- **Container** — a running instance of an image. Like an object.
- **Registry** — where images are shared (Docker Hub, ghcr.io).

## Commands

```bash
docker build -t my-ttt .              # build an image from ./Dockerfile
docker run --rm -p 8080:8080 my-ttt   # run it, publish a port, clean up after
docker run -d ...                     # in the background
docker ps                             # running containers
docker ps -a                          # ...including stopped ones
docker logs <id>                      # its output
docker exec -it <id> bash             # a shell inside a running container
docker images                         # local images and their sizes
docker rm -f <id>                     # kill and remove
```

## Dockerfile instructions

| Instruction | Does |
| --- | --- |
| `FROM` | the base image (and starts a stage) |
| `RUN` | run a command **at build time**, creating a layer |
| `COPY` | copy from the build context into the image |
| `COPY --from=stage` | copy from an earlier build stage |
| `WORKDIR` | set the working directory |
| `USER` | who the process runs as |
| `EXPOSE` | documentation only — publishes nothing |
| `HEALTHCHECK` | how Docker tests that it is alive |
| `CMD` | what runs when the container starts |

## Layers and caching

Each instruction makes a layer. Docker reuses cached layers until it reaches
one whose inputs changed, then rebuilds everything from there down.

So copy the things that rarely change **first**:

```dockerfile
COPY CMakeLists.txt ./       # rarely changes
COPY course/ ./course/       # rarely changes
COPY my-game/ ./my-game/     # changes constantly
RUN cmake ... && cmake --build ...
```

Copy everything in one go and every edit re-runs the whole build.

## Multi-stage builds

```dockerfile
FROM ubuntu:24.04 AS build
RUN apt-get install -y g++ cmake make
COPY . .
RUN cmake -S . -B build && cmake --build build

FROM ubuntu:24.04 AS run
COPY --from=build /src/build/.../ttt-server /app/ttt-server
CMD ["/app/ttt-server"]
```

Only the last stage ships. The compiler stays behind. ~1 GB becomes ~32 MB.

## The build context

`docker build -t my-ttt .` sends **that entire `.` folder** to the Docker daemon
before doing anything. `.dockerignore` keeps `build/`, `.git/` and friends out
of it. Without one, builds are slow for no reason.

## 0.0.0.0, always

A server bound to `127.0.0.1` inside a container is unreachable from the host,
no matter what `-p` you passed — because inside the container, `127.0.0.1` is
the container.

Bind `0.0.0.0`. See
[container connection refused](/help/container-connection-refused).

## Do not run as root

```dockerfile
RUN useradd --create-home ttt
USER ttt
```

One line, and it is the first thing anyone reviewing your Dockerfile looks for.
