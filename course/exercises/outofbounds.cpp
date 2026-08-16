// =============================================================================
//  Stage 4 exercise: your first gdb session.
// =============================================================================
//
//      cmake --build build --target exercise_outofbounds
//      gdb ./build/course/exercises/exercise_outofbounds
//
//  Inside gdb:
//
//      break countMarks      # stop when we enter the function
//      run                   # start the program
//      print count           # what is it now?
//      print i               # and the loop variable?
//      next                  # one line at a time
//      print board[i]        # what are we actually reading?
//      bt                    # how did we get here?
//      continue              # let it finish
//
//  The bug is one character. Find it with gdb rather than by staring -- the
//  point of this exercise is the tool, not the bug.
// =============================================================================

#include <iostream>

constexpr int kCellCount = 9;

// BROKEN ON PURPOSE. Reads one element past the end of the array.
int countMarks(const char board[kCellCount]) {
    int count = 0;
    for (int i = 0; i <= kCellCount; ++i) {  // <-- look very carefully at this
        if (board[i] != '.') {
            ++count;
        }
    }
    return count;
}

int main() {
    const char board[kCellCount] = {'X', 'O', '.', '.', 'X', '.', '.', '.', 'O'};

    std::cout << "marks on the board: " << countMarks(board) << "\n";
    std::cout << "(the right answer is 4 -- is that what you got?)\n";

    return 0;
}
