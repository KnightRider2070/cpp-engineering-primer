// =============================================================================
//  The contract tests.
// =============================================================================
//
//  Look at the includes. There are two, and neither of them is yours.
//
//  This file does not know the name of a single one of your classes, your
//  members, or your files. It reaches your entire game through one free
//  function, ttt::createGame(), and then only ever calls the three methods on
//  ttt::Game.
//
//  That is why you get to design the thing yourself. It is also the practical
//  answer to "why does that factory function exist?" -- without it, a test
//  would have to name one of your types, and then your design would not be
//  yours any more.
// =============================================================================

#include <gtest/gtest.h>

#include <ttt/Game.hpp>

namespace {

using ttt::Mark;
using ttt::MoveError;
using ttt::Player;
using ttt::Snapshot;
using ttt::Status;

// Play a list of cells in order, returning the final snapshot.
Snapshot playAll(ttt::Game& game, std::initializer_list<int> cells) {
    Snapshot snapshot = game.snapshot();
    for (int cell : cells) {
        snapshot = game.play(cell).snapshot;
    }
    return snapshot;
}

int countMarks(const Snapshot& snapshot) {
    int n = 0;
    for (Mark mark : snapshot.board) {
        if (mark != Mark::Empty) ++n;
    }
    return n;
}

// The eight winning lines, and the moves that reach each one.
// X takes the line; O plays two throwaway cells that are not on it.
struct WinCase {
    const char* name;
    int line[3];
};

const WinCase kLines[] = {
    {"top row",        {0, 1, 2}},
    {"middle row",     {3, 4, 5}},
    {"bottom row",     {6, 7, 8}},
    {"left column",    {0, 3, 6}},
    {"middle column",  {1, 4, 7}},
    {"right column",   {2, 5, 8}},
    {"main diagonal",  {0, 4, 8}},
    {"anti diagonal",  {2, 4, 6}},
};

bool onLine(const int line[3], int cell) {
    return cell == line[0] || cell == line[1] || cell == line[2];
}

// Is this set of three cells itself a winning line?
bool isWinningTriple(int a, int b, int c) {
    for (const auto& item : kLines) {
        int hits = 0;
        for (int cell : item.line) {
            if (cell == a || cell == b || cell == c) ++hits;
        }
        if (hits == 3) return true;
    }
    return false;
}

// Three throwaway cells for the *other* player: none on the target line, and
// crucially not themselves a winning line -- otherwise the distraction moves
// win the game before the line under test is finished. (Getting this wrong is
// exactly how this test was broken the first time it was written.)
bool safeFillers(const int line[3], int out[3]) {
    int off[9];
    int count = 0;
    for (int cell = 0; cell < 9; ++cell) {
        if (!onLine(line, cell)) off[count++] = cell;
    }
    for (int i = 0; i < count; ++i) {
        for (int j = i + 1; j < count; ++j) {
            for (int k = j + 1; k < count; ++k) {
                if (!isWinningTriple(off[i], off[j], off[k])) {
                    out[0] = off[i];
                    out[1] = off[j];
                    out[2] = off[k];
                    return true;
                }
            }
        }
    }
    return false;
}

}  // namespace

// --- the basics -------------------------------------------------------------

TEST(Contract, CreateGameReturnsSomething) {
    auto game = ttt::createGame();
    ASSERT_NE(game, nullptr) << "ttt::createGame() returned nullptr";
}

TEST(Contract, ANewGameIsEmptyAndXStarts) {
    auto game = ttt::createGame();
    Snapshot snapshot = game->snapshot();

    EXPECT_EQ(countMarks(snapshot), 0) << "a new game should have an empty board";
    EXPECT_EQ(snapshot.turn, Player::X) << "X moves first";
    EXPECT_EQ(snapshot.status, Status::InProgress);
    EXPECT_FALSE(snapshot.winner.has_value());
}

TEST(Contract, AMoveLandsOnTheCellYouAskedFor) {
    auto game = ttt::createGame();
    auto result = game->play(4);

    EXPECT_TRUE(result.ok()) << "playing cell 4 on an empty board should work";
    EXPECT_EQ(result.error, MoveError::None);
    EXPECT_EQ(result.snapshot.board[4], Mark::X);
}

TEST(Contract, PlayersAlternate) {
    auto game = ttt::createGame();
    Snapshot snapshot = playAll(*game, {0, 4});

    EXPECT_EQ(snapshot.board[0], Mark::X);
    EXPECT_EQ(snapshot.board[4], Mark::O);
    EXPECT_EQ(snapshot.turn, Player::X);
}

TEST(Contract, SnapshotMatchesTheOneReturnedByPlay) {
    auto game = ttt::createGame();
    auto result = game->play(2);
    Snapshot later = game->snapshot();

    EXPECT_EQ(result.snapshot.board, later.board)
        << "play() and snapshot() disagree about the board";
    EXPECT_EQ(result.snapshot.turn, later.turn);
}

// --- refusing bad moves ------------------------------------------------------

TEST(Contract, OutOfRangeIsReportedAsOutOfRange) {
    auto game = ttt::createGame();

    EXPECT_EQ(game->play(-1).error, MoveError::OutOfRange);
    EXPECT_EQ(game->play(9).error, MoveError::OutOfRange);
    EXPECT_EQ(game->play(100).error, MoveError::OutOfRange);
    EXPECT_EQ(countMarks(game->snapshot()), 0) << "a refused move must not change the board";
}

TEST(Contract, TakenCellIsReportedAsCellTaken) {
    auto game = ttt::createGame();
    game->play(4);
    auto result = game->play(4);

    EXPECT_EQ(result.error, MoveError::CellTaken);
    EXPECT_FALSE(result.ok());
    EXPECT_EQ(result.snapshot.board[4], Mark::X) << "the original mark must survive";
    EXPECT_EQ(countMarks(result.snapshot), 1);
}

TEST(Contract, ARefusedMoveDoesNotChangeWhoseTurnItIs) {
    auto game = ttt::createGame();
    game->play(0);                       // X
    Player before = game->snapshot().turn;
    game->play(0);                       // refused
    EXPECT_EQ(game->snapshot().turn, before) << "a refused move must not pass the turn";
}

TEST(Contract, MovesAfterTheGameEndsAreReportedAsGameOver) {
    auto game = ttt::createGame();
    playAll(*game, {0, 3, 1, 4, 2});     // X takes the top row

    ASSERT_EQ(game->snapshot().status, Status::Won);
    EXPECT_EQ(game->play(8).error, MoveError::GameOver);
}

// --- winning and drawing -----------------------------------------------------

TEST(Contract, EveryWinningLineIsDetectedForX) {
    for (const auto& item : kLines) {
        auto game = ttt::createGame();
        int filler[3] = {-1, -1, -1};
        ASSERT_TRUE(safeFillers(item.line, filler)) << "no safe filler cells for " << item.name;

        game->play(item.line[0]);   // X
        game->play(filler[0]);      // O
        game->play(item.line[1]);   // X
        game->play(filler[1]);      // O
        auto result = game->play(item.line[2]);  // X completes the line

        EXPECT_EQ(result.snapshot.status, Status::Won) << "X should have won on the " << item.name;
        ASSERT_TRUE(result.snapshot.winner.has_value()) << "no winner set on the " << item.name;
        EXPECT_EQ(*result.snapshot.winner, Player::X) << "wrong winner on the " << item.name;
    }
}

TEST(Contract, EveryWinningLineIsDetectedForO) {
    for (const auto& item : kLines) {
        auto game = ttt::createGame();
        int filler[3] = {-1, -1, -1};
        ASSERT_TRUE(safeFillers(item.line, filler)) << "no safe filler cells for " << item.name;

        // X wastes three moves that do not form a line; O builds the line.
        game->play(filler[0]);      // X
        game->play(item.line[0]);   // O
        game->play(filler[1]);      // X
        game->play(item.line[1]);   // O
        game->play(filler[2]);      // X
        auto result = game->play(item.line[2]);  // O completes the line

        EXPECT_EQ(result.snapshot.status, Status::Won) << "O should have won on the " << item.name;
        ASSERT_TRUE(result.snapshot.winner.has_value()) << "no winner set on the " << item.name;
        EXPECT_EQ(*result.snapshot.winner, Player::O) << "wrong winner on the " << item.name;
    }
}

TEST(Contract, AFullBoardWithNoLineIsADraw) {
    auto game = ttt::createGame();
    //  X O X
    //  X O O
    //  O X X
    Snapshot snapshot = playAll(*game, {0, 1, 2, 4, 3, 5, 7, 6, 8});

    EXPECT_EQ(countMarks(snapshot), 9) << "the board should be full";
    EXPECT_EQ(snapshot.status, Status::Draw) << "nobody has three in a row here";
    EXPECT_FALSE(snapshot.winner.has_value()) << "a draw has no winner";
}

TEST(Contract, AWinStopsTheGameEarly) {
    auto game = ttt::createGame();
    Snapshot snapshot = playAll(*game, {0, 3, 1, 4, 2});

    EXPECT_EQ(snapshot.status, Status::Won);
    EXPECT_EQ(countMarks(snapshot), 5) << "the game should have ended the moment X won";
}

// --- reset -------------------------------------------------------------------

TEST(Contract, ResetClearsEverything) {
    auto game = ttt::createGame();
    playAll(*game, {0, 3, 1, 4, 2});     // X wins
    game->reset();

    Snapshot snapshot = game->snapshot();
    EXPECT_EQ(countMarks(snapshot), 0);
    EXPECT_EQ(snapshot.status, Status::InProgress);
    EXPECT_EQ(snapshot.turn, Player::X);
    EXPECT_FALSE(snapshot.winner.has_value());
}

TEST(Contract, YouCanPlayAgainAfterReset) {
    auto game = ttt::createGame();
    playAll(*game, {0, 3, 1, 4, 2});
    game->reset();
    EXPECT_TRUE(game->play(4).ok()) << "after reset the board should accept moves again";
}

// --- the two that catch structural mistakes ----------------------------------

TEST(Contract, SnapshotsAreIndependentCopies) {
    auto game = ttt::createGame();
    Snapshot before = game->snapshot();
    game->play(4);

    EXPECT_EQ(before.board[4], Mark::Empty)
        << "a snapshot taken earlier changed when the game moved on. snapshot() must hand "
           "back a copy, not a view into your live state.";
}

TEST(Contract, TwoGamesAreIndependent) {
    auto first = ttt::createGame();
    auto second = ttt::createGame();

    first->play(0);

    EXPECT_EQ(second->snapshot().board[0], Mark::Empty)
        << "playing on one game changed another one. That normally means the board is a "
           "global or a static, rather than a member of your class.";
    EXPECT_EQ(countMarks(second->snapshot()), 0);
}
