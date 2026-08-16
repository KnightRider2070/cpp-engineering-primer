// =============================================================================
//  Turning game types into JSON.
// =============================================================================
//
//  Worth reading even though you didn't write it, for one specific reason:
//  every `switch` below has NO `default:` case.
//
//  That is deliberate. When a switch over an `enum class` is missing a case,
//  the compiler warns you (-Wswitch, which -Wall turns on). If somebody adds a
//  fourth Status tomorrow, this file stops compiling and tells them exactly
//  which function forgot about it.
//
//  Add a `default:` and you throw that away: the code would still compile and
//  would silently send the wrong string. This is what people mean when they say
//  "let the type system do the work".
// =============================================================================

#include "Json.hpp"

#include <nlohmann/json.hpp>

namespace ttt::json {
namespace {

const char* name(Mark mark) {
    switch (mark) {
        case Mark::Empty: return "empty";
        case Mark::X:     return "x";
        case Mark::O:     return "o";
    }
    return "empty";  // not reachable for a valid Mark
}

const char* name(Player player) {
    switch (player) {
        case Player::X: return "x";
        case Player::O: return "o";
    }
    return "x";
}

const char* name(Status status) {
    switch (status) {
        case Status::InProgress: return "in_progress";
        case Status::Won:        return "won";
        case Status::Draw:       return "draw";
    }
    return "in_progress";
}

const char* name(MoveError error) {
    switch (error) {
        case MoveError::None:       return "none";
        case MoveError::OutOfRange: return "out_of_range";
        case MoveError::CellTaken:  return "cell_taken";
        case MoveError::GameOver:   return "game_over";
    }
    return "none";
}

nlohmann::json toJson(const Snapshot& snapshot) {
    nlohmann::json cells = nlohmann::json::array();
    for (Mark mark : snapshot.board) {
        cells.push_back(name(mark));
    }

    return nlohmann::json{
        {"board",  cells},
        {"turn",   name(snapshot.turn)},
        {"status", name(snapshot.status)},
        // An absent winner becomes JSON null rather than a made-up value.
        {"winner", snapshot.winner ? nlohmann::json(name(*snapshot.winner))
                                   : nlohmann::json(nullptr)},
    };
}

}  // namespace

std::string encode(const Snapshot& snapshot) {
    return toJson(snapshot).dump();
}

std::string encode(const MoveResult& result) {
    return nlohmann::json{
        {"ok",    result.ok()},
        {"error", name(result.error)},
        {"state", toJson(result.snapshot)},
    }.dump();
}

}  // namespace ttt::json
