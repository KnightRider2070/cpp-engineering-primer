// =============================================================================
//  The web server. Course-owned -- you never have to write this.
// =============================================================================
//
//  It is about 90 lines, and it is worth reading once you reach Stage 5,
//  because it is the answer to "how does a browser end up running my C++?".
//
//  The whole thing touches your code exactly once:
//
//      auto game = ttt::createGame();
//
//  After that it only ever calls the three functions in ttt::Game. It has no
//  idea what your classes are called. That is the entire point of the contract.
// =============================================================================

#include <atomic>
#include <cstdlib>
#include <iostream>
#include <mutex>
#include <string>

#include <httplib.h>
#include <nlohmann/json.hpp>
#include <ttt/Game.hpp>

#include "Json.hpp"

namespace {

constexpr const char* kJson = "application/json";

std::string webRootFrom(int argc, char** argv) {
    for (int i = 1; i + 1 < argc; ++i) {
        if (std::string(argv[i]) == "--web-root") {
            return argv[i + 1];
        }
    }
    if (const char* env = std::getenv("TTT_WEB_ROOT")) {
        return env;
    }
    return "course/web";
}

int portFrom(int argc, char** argv) {
    for (int i = 1; i + 1 < argc; ++i) {
        if (std::string(argv[i]) == "--port") {
            return std::atoi(argv[i + 1]);
        }
    }
    if (const char* env = std::getenv("TTT_PORT")) {
        return std::atoi(env);
    }
    return 8080;
}

}  // namespace

int main(int argc, char** argv) {
    // The one line that touches the code you wrote.
    auto game = ttt::createGame();
    if (!game) {
        std::cerr << "ttt::createGame() returned nullptr.\n";
        return 1;
    }

    // httplib serves each request on its own thread, so two browser tabs could
    // call play() at the same moment. One mutex keeps the game consistent.
    // (You will meet this problem properly if you ever do concurrent C++;
    //  here it is handled for you.)
    std::mutex mutex;

    httplib::Server server;

    const std::string webRoot = webRootFrom(argc, argv);
    if (!server.set_mount_point("/", webRoot)) {
        std::cerr << "Could not serve files from: " << webRoot << "\n"
                  << "Pass --web-root <dir> or run this through ./ttt serve.\n";
        return 1;
    }

    server.Get("/api/health", [](const httplib::Request&, httplib::Response& res) {
        res.set_content(R"({"ok":true})", kJson);
    });

    server.Get("/api/state", [&](const httplib::Request&, httplib::Response& res) {
        std::lock_guard<std::mutex> lock(mutex);
        res.set_content(ttt::json::encode(game->snapshot()), kJson);
    });

    server.Post("/api/move", [&](const httplib::Request& req, httplib::Response& res) {
        // A malformed *request* is a 400. A refused *move* is a 200 with an
        // error field -- an illegal move is a normal thing for a game to say.
        auto body = nlohmann::json::parse(req.body, nullptr, /*allow_exceptions=*/false);
        if (body.is_discarded() || !body.contains("cell") || !body["cell"].is_number_integer()) {
            res.status = 400;
            res.set_content(
                R"({"ok":false,"error":"bad_request","detail":"field 'cell' must be an integer"})",
                kJson);
            return;
        }

        std::lock_guard<std::mutex> lock(mutex);
        res.set_content(ttt::json::encode(game->play(body["cell"].get<int>())), kJson);
    });

    server.Post("/api/reset", [&](const httplib::Request&, httplib::Response& res) {
        std::lock_guard<std::mutex> lock(mutex);
        game->reset();
        res.set_content(ttt::json::encode(game->snapshot()), kJson);
    });

    const int port = portFrom(argc, argv);

    std::cout << "Your game is running.\n"
              << "  Open http://localhost:" << port << "\n"
              << "  Serving files from: " << webRoot << "\n"
              << "  Ctrl-C to stop.\n";

    // 0.0.0.0, not 127.0.0.1 -- and this matters more than it looks.
    //
    // 127.0.0.1 means "only accept connections that started on this machine".
    // Inside a Docker container, "this machine" is the container, so a server
    // bound to 127.0.0.1 is unreachable from your laptop even with -p 8080:8080.
    // That is the single most common first-Docker failure. You meet it at Stage 8.
    if (!server.listen("0.0.0.0", port)) {
        std::cerr << "Could not listen on port " << port << ".\n"
                  << "Something else is probably already using it.\n";
        return 1;
    }
    return 0;
}
