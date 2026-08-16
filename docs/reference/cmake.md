# CMake notes

CMake does not build anything. It **generates** a build (a Makefile, usually),
which then builds your code.

## The two commands

```bash
cmake -S . -B build        # configure: read CMakeLists.txt, generate a build
cmake --build build        # build: actually compile
cmake --build build -j4    # ...using 4 cores
```

`-S .` is the source directory, `-B build` is where the generated mess goes.
Everything CMake creates lives in `build/`, which is gitignored and safe to
delete at any time. That is what "out-of-source build" means, and it is why
`rm -rf build` is a reasonable first move when something is behaving oddly.

## The pieces you need

```cmake
add_library(my_game Board.cpp Game.cpp)      # a thing to link against
add_executable(ttt-cli main.cpp)             # a thing to run

target_include_directories(my_game PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(ttt-cli PRIVATE my_game)
target_compile_options(my_game PRIVATE -Wall -Wextra)
```

**Every `.cpp` you write must be listed** in `add_library` or `add_executable`.
Forgetting is the single most common CMake mistake, and it produces a linker
error, not a compiler error — see
[undefined reference](/help/undefined-reference).

Headers are *not* listed. They are pulled in by `#include`.

## PUBLIC vs PRIVATE

- `PRIVATE` — needed to build this target, not by whoever links it.
- `PUBLIC` — needed to build this target **and** by whoever links it.

Your include directory is `PUBLIC` because the tests include your headers.
Your warning flags are `PRIVATE` because they are nobody else's business.

## Handy

```bash
cmake --build build --target ttt-cli     # build just one thing
cmake --build build --target help        # list targets
ctest --test-dir build --output-on-failure
rm -rf build && cmake -S . -B build      # start clean
```
