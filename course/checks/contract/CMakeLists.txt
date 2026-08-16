# The contract tests. Only configured once `my_game` exists (Stage 3+),
# and only meaningful once ttt::createGame() is implemented (Stage 5).

# GoogleTest is fetched once in the top-level CMakeLists.txt.

add_executable(ttt-contract-tests
    GameContractTests.cpp
)

target_link_libraries(ttt-contract-tests PRIVATE
    my_game
    ttt_contract
    GTest::gtest_main
)

target_compile_options(ttt-contract-tests PRIVATE -Wall -Wextra)

add_test(NAME contract COMMAND ttt-contract-tests)
