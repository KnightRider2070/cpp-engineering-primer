# The web server. Only built once you have implemented ttt::createGame().

add_executable(ttt-server
    Main.cpp
    Json.cpp
)

target_link_libraries(ttt-server PRIVATE
    my_game          # your code
    ttt_contract     # the contract
    ttt_vendor       # httplib + nlohmann/json
)

find_package(Threads REQUIRED)
target_link_libraries(ttt-server PRIVATE Threads::Threads)

# The course's own code builds clean too.
target_compile_options(ttt-server PRIVATE -Wall -Wextra)
