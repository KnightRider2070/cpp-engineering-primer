// =============================================================================
//  Stage 6 exercise: the reference that outlived the thing it referred to.
// =============================================================================
//
//  Run it twice:
//
//      cmake --build build --target exercise_dangling
//      ./build/course/exercises/exercise_dangling
//
//      cmake --build build --target exercise_dangling_asan
//      ./build/course/exercises/exercise_dangling_asan
//
//  Three things to notice, in this order:
//
//  1. THE COMPILER ALREADY TOLD YOU. Scroll up through the build output and
//     find the warning about returning a reference to stack memory. You got
//     that for free, before you ran anything. This is why -Wall -Wextra is
//     switched on for every target in this course.
//
//  2. THE PLAIN BUILD DOES NOT CRASH. It prints an empty string where it
//     should print "cell #4". Not a crash, not an error -- just a quietly
//     wrong answer. That is the genuinely dangerous part of undefined
//     behaviour: it is under no obligation to look broken. On a different
//     compiler, or a different day, this same program might print garbage,
//     or the right answer, or crash.
//
//  3. THE ASAN BUILD NAMES THE CULPRIT. Same source, one extra compiler flag,
//     and now you get the exact variable, the exact function, and the exact
//     line. Read the report from the top: "stack-use-after-return", then the
//     READ that went wrong, then the frame where the memory used to live.
//
//  Question to answer before you move on: why does `makeLabel` compile at all?
//  What is the compiler allowed to assume about how long `label` lives?
// =============================================================================

#include <iostream>
#include <string>

// Turn on stack-use-after-return checking without needing an env var.
// (Normally you would type ASAN_OPTIONS=detect_stack_use_after_return=1
//  in front of the command. This just bakes the default into the binary.)
// Under a non-ASan build nothing calls this, and it costs nothing.
extern "C" const char* __asan_default_options() {
    return "detect_stack_use_after_return=1";
}

// BROKEN ON PURPOSE.
// `label` lives on the stack for exactly as long as this function runs.
// The moment we return, that stack space belongs to somebody else.
const std::string& makeLabel(int cell) {
    std::string label = "cell #" + std::to_string(cell);
    return label;  // <-- returning a reference to a local
}

// The honest version. Costs one copy -- and usually not even that, because
// the compiler is allowed to move it straight out. Correctness first.
std::string makeLabelSafely(int cell) {
    std::string label = "cell #" + std::to_string(cell);
    return label;
}

int main() {
    std::cout << "--- the broken one ---\n";
    const std::string& bad = makeLabel(4);

    // Call another function before reading `bad`. This hands the stack space
    // that `label` used to occupy to somebody else, which is what turns
    // "seems to work" into visibly wrong.
    const std::string noise = makeLabelSafely(7);
    (void)noise;

    std::cout << "bad  = \"" << bad << "\"   <-- should say \"cell #4\"\n";

    std::cout << "--- the safe one ---\n";
    const std::string good = makeLabelSafely(4);
    std::cout << "good = \"" << good << "\"\n";

    return 0;
}
