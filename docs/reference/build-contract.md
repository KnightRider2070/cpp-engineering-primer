# The build contract

Four names, and one flag. That is everything the course pins down.

| What | Kind | From | Why it has to be fixed |
| --- | --- | --- | --- |
| `my-game/main.cpp` | file | Stage 1 | stages 1–2 have no build system, so the checker compiles this by hand |
| `my_game` | CMake library target | Stage 3 | the tests and the server link against it |
| `ttt-cli` | CMake executable target | Stage 3 | `./ttt play` and the CLI checks run it |
| `ttt::createGame()` | function | Stage 5 | the only symbol that reaches your code |
| `--vs-computer` | CLI flag | Stage 7 | the check needs a way to ask for an opponent |

**Everything else is yours**: class names, member names, file names beyond
`main.cpp`, namespaces, how you store the board, how you track turns, how you
report errors, how you draw the game.

No test in this course mentions any of them. You can verify that claim: read
`course/checks/contract/GameContractTests.cpp`.

## The minimum CMakeLists

```cmake
add_library(my_game Board.cpp Game.cpp Adapter.cpp)   # your file names
target_include_directories(my_game PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(my_game PUBLIC ttt_contract)
target_compile_options(my_game PRIVATE -Wall -Wextra)

add_executable(ttt-cli main.cpp)
target_link_libraries(ttt-cli PRIVATE my_game)
```

From Stage 7, your own tests (GoogleTest is already available):

```cmake
add_executable(my-tests PlayerTests.cpp)
target_link_libraries(my-tests PRIVATE my_game GTest::gtest_main)
add_test(NAME my_tests COMMAND my-tests)
```

## Two names, and why that is the deal

The course could have discovered your targets automatically. It does not,
because a build that guesses is a build that fails mysteriously.

Think of it as the trade: **you name your classes; the course names your
targets.** Two identifiers, in exchange for never having a test tell you what
to call anything.
