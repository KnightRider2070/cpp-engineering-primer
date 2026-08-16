#pragma once

// The boundary between C++ types and the wire.
//
// This is the ONLY place in the whole project where a Mark, a Player, a Status
// or a MoveError turns into a string. Everywhere else they stay as enums, where
// the compiler can check them.

#include <string>

#include <ttt/Game.hpp>

namespace ttt::json {

std::string encode(const Snapshot& snapshot);
std::string encode(const MoveResult& result);

}  // namespace ttt::json
