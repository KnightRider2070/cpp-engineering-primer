// =============================================================================
//  Somebody else's code. Review it.
// =============================================================================
//
//  This arrived as a pull request titled "add win detection". It compiles.
//  It even passes the one test its author wrote.
//
//  Your job is not to run it. Your job is to read it and write down what is
//  wrong, the way you would in a code review -- specific, and with a reason.
//
//  Write your findings in my-notes/reviews/stage-5.md before you look at the
//  model review. There are at least three separate problems in here, and one
//  of them will crash on some inputs.
// =============================================================================

#pragma once

#include <cstddef>

namespace review {

struct Board {
    char cells[9];

    void clear() {
        for (int i = 0; i < 9; i++) {
            cells[i] = ' ';
        }
    }

    bool is_valid_move(int pos) {
        if (pos < 0 || pos > 9) {
            return false;
        }
        return cells[pos] == ' ';
    }

    // Returns true if X has three in a row.
    bool is_winner() {
        for (int i = 0; i <= 8; i++) {
            if (cells[i] == 'X' && cells[i + 1] == 'X' && cells[i + 2] == 'X') {
                return true;
            }
        }

        for (int i = 0; i < 3; i++) {
            if (cells[i] == 'X' && cells[i + 3] == 'X' && cells[i + 6] == 'X') {
                return true;
            }
        }

        return false;
    }
};

}  // namespace review
