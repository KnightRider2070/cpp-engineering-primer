#!/usr/bin/env python3
"""The grader.

Rules this file exists to enforce:

  1. Never print a PASS it did not earn. There is no canned output anywhere.
  2. Always be able to show its work (--explain). The student cannot read the
     reference solution, so the checker must explain what it did instead.
  3. Everything runs under a timeout. A beginner's while-loop will hang.
  4. Checks are cumulative: `run.py 4` re-runs stages 1..4, so "done" keeps
     meaning "still done".
  5. Never mention a name the student chose. See docs/reference/build-contract.md.

Usage:
    run.py <stage> [--explain]
    run.py --all [--report] [--explain]
"""

import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MY_GAME = os.path.join(ROOT, "my-game")
BUILD = os.path.join(ROOT, "build")
MAX_STAGE = 8
TIMEOUT = 10

sys.path.insert(0, HERE)
import frame  # noqa: E402

USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def c(code, text):
    return "\033[%sm%s\033[0m" % (code, text) if USE_COLOR else text


BOLD = lambda s: c("1", s)
DIM = lambda s: c("2", s)
RED = lambda s: c("31", s)
GREEN = lambda s: c("32", s)
YELLOW = lambda s: c("33", s)


class Result:
    """One assertion, plus enough context to explain itself."""

    def __init__(self, name, passed, detail="", explain=""):
        self.name = name
        self.passed = passed
        self.detail = detail
        self.explain = explain


class Skip(Exception):
    """Raised when a stage cannot be checked yet (e.g. no files written)."""


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def run(cmd, **kw):
    kw.setdefault("capture_output", True)
    kw.setdefault("text", True)
    kw.setdefault("timeout", TIMEOUT)
    try:
        return subprocess.run(cmd, **kw)
    except subprocess.TimeoutExpired:
        return None


def student_sources():
    """Every .cpp the student has written, excluding scratch work."""
    out = []
    for path in glob.glob(os.path.join(MY_GAME, "**", "*.cpp"), recursive=True):
        if os.sep + "scratch" + os.sep in path:
            continue
        out.append(path)
    return sorted(out)


def uses_cmake():
    return os.path.exists(os.path.join(MY_GAME, "CMakeLists.txt"))


def compile_student(extra_flags=None, out_name="game"):
    """Compile my-game/*.cpp by hand. Used for stages 1-2, before CMake exists.

    Test files are skipped: they carry their own main() from GoogleTest and
    would collide with the student's.

    Returns (binary_path_or_None, compiler_output, tmpdir).
    """
    srcs = [s for s in student_sources()
            if "test" not in os.path.basename(s).lower()]
    if not srcs:
        raise Skip("my-game/ has no .cpp files yet")
    tmp = tempfile.mkdtemp(prefix="ttt-check-")
    binary = os.path.join(tmp, out_name)
    cxx = shutil.which("g++") or shutil.which("clang++")
    if not cxx:
        raise Skip("no C++ compiler found")
    cmd = ([cxx, "-std=c++17", "-Wall", "-Wextra",
            "-I", os.path.join(ROOT, "course", "include"),
            "-I", MY_GAME,
            "-o", binary] + srcs + (extra_flags or []))
    proc = run(cmd, timeout=120)
    if proc is None:
        return None, "compiler timed out", tmp
    if proc.returncode != 0:
        return None, proc.stdout + proc.stderr, tmp
    return binary, proc.stdout + proc.stderr, tmp


def student_binary():
    """The student's playable game, however it currently gets built.

    Stages 1-2 have no build system, so we compile by hand. From Stage 3 the
    student owns a CMakeLists.txt and we use that instead -- otherwise these
    early checks would break the moment their project grows past one file,
    which is exactly when we most want them still running as regressions.

    Returns (binary, compiler_output, tmpdir_or_None).
    """
    if uses_cmake():
        proc = cmake_configure()
        if not (proc and proc.returncode == 0):
            return None, (proc.stdout + proc.stderr) if proc else "cmake timed out", None
        proc = cmake_build("ttt-cli")
        if not (proc and proc.returncode == 0):
            return None, (proc.stdout + proc.stderr) if proc else "build timed out", None
        binary = find_binary("ttt-cli")
        if not binary:
            return None, "built successfully but no ttt-cli binary was produced", None
        return binary, proc.stdout + proc.stderr, None
    return compile_student()


MAX_CAPTURE = 256 * 1024        # only ever read back the tail of a program's output
RUNAWAY_BYTES = 8 * 1024 * 1024  # past this, the program is clearly in a loop


def play(binary, moves, timeout=TIMEOUT):
    """Feed newline-separated moves to a binary.

    Returns (output, returncode, stop_reason) where stop_reason is None if the
    program ended by itself, "timeout" if it was still running, or "runaway" if
    it flooded stdout. Callers treat any non-None reason as "did not finish".

    Output goes to a temp file rather than a pipe. A student program stuck in a
    loop can emit hundreds of megabytes in a few seconds; buffering that in
    memory makes the checker itself unusable, and filling a pipe that nobody
    drains can wedge the child instead of killing it. We keep only the tail.
    """
    stdin = "".join("%s\n" % m for m in moves)
    with tempfile.TemporaryFile(mode="w+b") as sink, \
         tempfile.TemporaryFile(mode="w+b") as feed:
        feed.write(stdin.encode())
        feed.seek(0)
        proc = subprocess.Popen([binary], stdin=feed, stdout=sink,
                                stderr=subprocess.STDOUT, start_new_session=True)
        stop_reason = None
        deadline = time.time() + timeout
        while proc.poll() is None:
            # A program printing this much has run away; that IS the answer,
            # so stop now instead of filling the disk for the full timeout.
            if os.fstat(sink.fileno()).st_size > RUNAWAY_BYTES:
                stop_reason = "runaway"
                break
            if time.time() > deadline:
                stop_reason = "timeout"
                break
            time.sleep(0.02)
        if stop_reason:
            _kill_tree(proc)
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                pass

        size = sink.seek(0, os.SEEK_END)
        sink.seek(max(0, size - MAX_CAPTURE))
        text = sink.read().decode("utf-8", "replace")
        if size > MAX_CAPTURE:
            text = ("[... %d bytes of earlier output not shown ...]\n" % (size - MAX_CAPTURE)) + text
        return text, (None if stop_reason else proc.returncode), stop_reason


def stuck_message(reason, context):
    """An accurate account of why we stopped the program."""
    if reason == "runaway":
        return ("it printed more than %d MB %s, so I stopped it. That much output means a loop "
                "that never ends." % (RUNAWAY_BYTES // (1024 * 1024), context))
    return "it was still running %ds %s, so I stopped it." % (TIMEOUT, context)


def _kill_tree(proc):
    """Kill the child and anything it spawned."""
    import signal
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def cmake_configure():
    proc = run(["cmake", "-S", ROOT, "-B", BUILD], timeout=180)
    return proc


def cmake_build(target=None):
    cmd = ["cmake", "--build", BUILD]
    if target:
        cmd += ["--target", target]
    return run(cmd, timeout=600)


def find_binary(name):
    for path in glob.glob(os.path.join(BUILD, "**", name), recursive=True):
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    return None


def has_target(name):
    proc = run(["cmake", "--build", BUILD, "--target", "help"], timeout=60)
    if proc and proc.returncode == 0 and re.search(r"^\.\.\.\s*%s\b" % re.escape(name),
                                                   proc.stdout, re.M):
        return True
    return find_binary(name) is not None


# ---------------------------------------------------------------------------
# Stage 0 -- environment
# ---------------------------------------------------------------------------
def check_stage_0():
    results = []

    cxx = shutil.which("g++") or shutil.which("clang++")
    results.append(Result("A C++ compiler is installed", cxx is not None,
                          cxx or "install with: sudo apt install build-essential"))

    cm = shutil.which("cmake")
    ver = ""
    if cm:
        proc = run(["cmake", "--version"])
        if proc:
            m = re.search(r"(\d+\.\d+\.\d+)", proc.stdout)
            ver = m.group(1) if m else ""
    results.append(Result("cmake 3.22 or newer", bool(ver) and _ver_ge(ver, "3.22"),
                          ("found %s" % ver) if ver else "install with: sudo apt install cmake"))

    # Your git identity is a property of your machine, not of your work, so
    # there is nothing to check on a CI runner (where it is never configured).
    if not os.environ.get("CI"):
        name = run(["git", "config", "--get", "user.name"])
        email = run(["git", "config", "--get", "user.email"])
        have_id = bool(name and name.stdout.strip()) and bool(email and email.stdout.strip())
        results.append(Result("git knows who you are", have_id,
                              "%s <%s>" % (name.stdout.strip(), email.stdout.strip())
                              if have_id else 'run: git config --global user.name "Your Name"'))

    proc = cmake_configure()
    results.append(Result("The project configures with an empty my-game/",
                          proc is not None and proc.returncode == 0,
                          "" if (proc and proc.returncode == 0)
                          else (proc.stdout + proc.stderr)[-600:] if proc else "cmake timed out"))

    hello = glob.glob(os.path.join(MY_GAME, "scratch", "*.cpp"))
    if not hello:
        # Not started rather than broken -- same distinction as every other stage.
        raise Skip("no my-game/scratch/hello.cpp yet -- write one that prints something")
    if True:
        tmp = tempfile.mkdtemp(prefix="ttt-hello-")
        binary = os.path.join(tmp, "hello")
        proc = run([cxx, "-std=c++17", "-o", binary] + hello, timeout=60)
        if proc and proc.returncode == 0:
            out, _, timed = play(binary, [])
            results.append(Result("hello compiles and prints something",
                                  bool(out.strip()) and not timed,
                                  "printed: %r" % out.strip()[:60]))
        else:
            results.append(Result("hello compiles", False,
                                  (proc.stdout + proc.stderr)[-600:] if proc else "timed out"))
        shutil.rmtree(tmp, ignore_errors=True)

    return results


def _ver_ge(have, want):
    def parts(v):
        return [int(x) for x in re.findall(r"\d+", v)]
    return parts(have) >= parts(want)


# ---------------------------------------------------------------------------
# Stage 1 -- an empty board on stdout
# ---------------------------------------------------------------------------
def check_stage_1():
    results = []
    binary, compiler_out, tmp = student_binary()
    try:
        if binary is None:
            results.append(Result("my-game compiles with -Wall -Wextra", False,
                                  compiler_out[-1500:]))
            return results
        warnings = [ln for ln in compiler_out.splitlines() if "warning:" in ln]
        results.append(Result("my-game compiles with -Wall -Wextra", True,
                              "%d warning(s)" % len(warnings) if warnings else "no warnings"))

        out, code, stuck = play(binary, [])
        if stuck:
            results.append(Result(
                "The program finishes on its own", False,
                stuck_message(stuck, "with no input at all") +
                "\n  At this stage the program should print the board and then end. If you "
                "already\n  have an input loop, it needs to stop when input runs out.",
                frame.describe(out)))
            return results

        board = frame.last_frame(out)
        results.append(Result("The output contains a 3x3 board", board is not None,
                              "" if board else "no three consecutive lines of three cells",
                              frame.describe(out)))
        if board is not None:
            empty = all(cell == "." for cell in board)
            results.append(Result("All nine cells are empty", empty,
                                  "" if empty else "found marks: %s" % "".join(board),
                                  frame.describe(out)))
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)
    return results


# ---------------------------------------------------------------------------
# Stage 2 -- moves land, players alternate, EOF ends it
# ---------------------------------------------------------------------------
def check_stage_2():
    results = []
    binary, compiler_out, tmp = student_binary()
    try:
        if binary is None:
            results.append(Result("my-game compiles", False, compiler_out[-1500:]))
            return results

        moves = [1, 5, 9, 3]          # human numbering: X=0, O=4, X=8, O=2
        out, code, stuck = play(binary, moves)

        results.append(Result(
            "The program exits when input runs out", not stuck,
            "" if not stuck else
            stuck_message(stuck, "after I stopped feeding it moves") +
            "\n  Use `while (std::cin >> n)` as your loop condition: it becomes false when "
            "there\n  is no more input, which is what ends the program.",
            frame.describe(out)))
        if stuck:
            return results

        results.append(Result("It exits with code 0", code == 0, "exit code was %s" % code))

        board = frame.last_frame(out)
        if board is None:
            results.append(Result("The output contains a board after the moves", False,
                                  "no board found", frame.describe(out)))
            return results

        expected = {0: "X", 4: "O", 8: "X", 2: "O"}
        wrong = {i: (board[i], want) for i, want in expected.items() if board[i] != want}
        results.append(Result(
            "Moves 1,5,9,3 land on the right cells with players alternating",
            not wrong,
            "" if not wrong else
            "; ".join("cell %d (typed %d) is %r, expected %r" % (i, i + 1, got, want)
                      for i, (got, want) in sorted(wrong.items())),
            frame.describe(out) + "\n\n  I typed: 1, 5, 9, 3\n"
            "  Expecting X at cell 0, O at cell 4, X at cell 8, O at cell 2\n"
            "  (cells count from 0; the numbers typed count from 1)"))

        others = [i for i in range(9) if i not in expected and board[i] != "."]
        results.append(Result("No other cells were touched", not others,
                              "" if not others else "unexpected marks at cells %s" % others,
                              frame.describe(out)))
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)
    return results


# ---------------------------------------------------------------------------
# Stage 3 -- CMake and the build contract
# ---------------------------------------------------------------------------
def check_stage_3():
    results = []
    cml = os.path.join(MY_GAME, "CMakeLists.txt")
    if not os.path.exists(cml):
        # Not started, as opposed to broken. The difference matters: CI should
        # not paint work you have not reached yet as a failure.
        raise Skip("no my-game/CMakeLists.txt yet -- this stage is where CMake arrives")
    results.append(Result("my-game/CMakeLists.txt exists", True))

    proc = cmake_configure()
    okc = proc is not None and proc.returncode == 0
    results.append(Result("cmake configures", okc,
                          "" if okc else (proc.stdout + proc.stderr)[-1500:] if proc
                          else "cmake timed out"))
    if not okc:
        return results

    # Only the student's own targets: building everything would also fetch and
    # compile GoogleTest, which is slow on a cold cache and has nothing to do
    # with whether THEIR code builds.
    proc = cmake_build("ttt-cli")
    okb = proc is not None and proc.returncode == 0
    detail = ""
    if not okb and proc:
        text = proc.stdout + proc.stderr
        detail = text[-1500:]
        if "undefined reference" in text or "Undefined symbols" in text:
            detail += ("\n\n  That is a LINKER error, not a compiler error. The compiler was "
                       "happy;\n  nothing could find the body of a function you declared. The "
                       "usual cause at\n  this stage is a .cpp file that is not listed in "
                       "my-game/CMakeLists.txt.")
    results.append(Result("the project builds", okb,
                          detail if not okb else "", detail))
    if not okb:
        return results

    warnings = [ln for ln in (proc.stdout + proc.stderr).splitlines() if "warning:" in ln]
    results.append(Result("builds without warnings", not warnings,
                          "\n".join("  " + w for w in warnings[:8]) if warnings else ""))

    for target in ("my_game", "ttt-cli"):
        found = has_target(target)
        results.append(Result("CMake target `%s` exists" % target, found,
                              "" if found else
                              "the course needs this exact name -- see "
                              "docs/reference/build-contract.md"))

    # Behaviour must not have changed: re-run the Stage 2 assertions on the CMake binary.
    binary = find_binary("ttt-cli")
    if not binary:
        results.append(Result("the ttt-cli binary was produced", False,
                              "the build reported success but no ttt-cli executable appeared"))
        return results
    if True:
        out, code, stuck = play(binary, [1, 5, 9, 3])
        board = frame.last_frame(out) if not stuck else None
        if stuck:
            results.append(Result("the refactored game still plays moves", False,
                                  stuck_message(stuck, "after the moves ran out"),
                                  frame.describe(out)))
        elif board is None:
            results.append(Result("the refactored game still prints a board", False,
                                  "no board found", frame.describe(out)))
        else:
            expected = {0: "X", 4: "O", 8: "X", 2: "O"}
            wrong = {i: board[i] for i, w in expected.items() if board[i] != w}
            results.append(Result(
                "the refactored game behaves exactly as it did at Stage 2", not wrong,
                "" if not wrong else "cells wrong: %s" % wrong,
                frame.describe(out) + "\n\n  A refactor that changes behaviour is not a refactor."))
    return results


# ---------------------------------------------------------------------------
# Stage 4 -- hostile input
# ---------------------------------------------------------------------------
def check_stage_4():
    results = []
    binary, compiler_out, tmp = student_binary()
    if binary is None:
        results.append(Result("the project builds", False, compiler_out[-1200:]))
        return results

    hostile = ["0", "10", "-1", "abc", "5", "5", "99", "", "4"]
    out, code, stuck = play(binary, hostile, timeout=TIMEOUT)

    results.append(Result(
        "hostile input does not hang the program", not stuck,
        "" if not stuck else
        stuck_message(stuck, "while I fed it bad input") +
        "\n  After `std::cin >> n` fails on something like 'abc', the stream stays in a\n"
        "  failed state and every later read fails instantly. You need std::cin.clear()\n"
        "  followed by std::cin.ignore(...) to recover.",
        frame.describe(out)))
    if stuck:
        return results

    crashed = code is not None and code < 0
    results.append(Result("hostile input does not crash it", not crashed,
                          "killed by signal %s" % (-code if crashed else "")))
    results.append(Result("it still exits cleanly (code 0)", code == 0,
                          "exit code was %s" % code))

    board = frame.last_frame(out)
    if board is not None:
        # '5' was played once (X at cell 4), the repeat must be refused,
        # and '4' then goes to O at cell 3.
        good = board[4] == "X" and board[3] == "O"
        others = [i for i in range(9) if i not in (3, 4) and board[i] != "."]
        results.append(Result(
            "refused moves left the board untouched", good and not others,
            "" if (good and not others) else
            "expected exactly X at cell 4 and O at cell 3; got %s" % "".join(board),
            frame.describe(out) +
            "\n\n  I typed: 0, 10, -1, abc, 5, 5, 99, <blank>, 4\n"
            "  Only two of those are legal moves: the first 5 (X -> cell 4)\n"
            "  and the 4 (O -> cell 3). Everything else must be refused."))
    return results


# ---------------------------------------------------------------------------
# Stages 5-7 -- the contract tests (never mention a student name)
# ---------------------------------------------------------------------------
def _contract_tests(stage, gtest_filter=None):
    results = []
    if not os.path.exists(os.path.join(MY_GAME, "CMakeLists.txt")):
        raise Skip("no my-game/CMakeLists.txt yet")
    proc = cmake_configure()
    if not (proc and proc.returncode == 0):
        results.append(Result("cmake configures", False,
                              (proc.stdout + proc.stderr)[-1200:] if proc else "timed out"))
        return results

    proc = cmake_build("ttt-contract-tests")
    if not (proc and proc.returncode == 0):
        text = (proc.stdout + proc.stderr) if proc else "timed out"
        hint = ""
        if "createGame" in text:
            hint = ("\n\n  The course could not find ttt::createGame(). You implement it -- "
                    "usually at\n  the bottom of the same .cpp as your adapter class. See "
                    "docs/reference/contract.md.")
        results.append(Result("the contract tests build", False, text[-1500:] + hint))
        return results

    binary = find_binary("ttt-contract-tests")
    if not binary:
        raise Skip("contract test binary not built")

    cmd = [binary, "--gtest_brief=0"]
    if gtest_filter:
        cmd.append("--gtest_filter=%s" % gtest_filter)
    proc = run(cmd, timeout=120)
    if proc is None:
        results.append(Result("the contract tests finish", False, "timed out"))
        return results

    passed = re.findall(r"\[       OK \] (\S+)", proc.stdout)
    failed = re.findall(r"\[  FAILED  \] (\S+)(?: \(|$)", proc.stdout)
    failed = [f for f in dict.fromkeys(failed) if "." in f]

    if proc.returncode == 0:
        results.append(Result("all %d contract tests pass" % len(passed), True))
    else:
        for name in failed:
            block = _gtest_failure_block(proc.stdout, name)
            results.append(Result(name, False, block))
        if not failed:
            results.append(Result("contract tests pass", False, proc.stdout[-1500:]))
    return results


def _gtest_failure_block(output, test_name):
    lines = output.splitlines()
    try:
        start = next(i for i, ln in enumerate(lines) if ln.startswith("[ RUN      ] " + test_name))
    except StopIteration:
        return ""
    out = []
    for ln in lines[start + 1:]:
        if ln.startswith("[") and ("OK ]" in ln or "FAILED  ]" in ln):
            break
        out.append("  " + ln)
    return "\n".join(out[:25])


def check_stage_5():
    return _contract_tests(5, gtest_filter="Contract.*")


def check_stage_6():
    results = _contract_tests(6, gtest_filter="Contract.*")
    if any(not r.passed for r in results):
        return results

    # Tier D: rebuild the student's CLI under sanitizers and play a full game.
    binary, compiler_out, tmp = compile_student(
        extra_flags=["-fsanitize=address,undefined", "-g", "-fno-omit-frame-pointer"],
        out_name="game-asan")
    try:
        if binary is None:
            results.append(Result("your code builds under AddressSanitizer", False,
                                  compiler_out[-1200:]))
            return results
        env = dict(os.environ, ASAN_OPTIONS="detect_stack_use_after_return=1",
                   UBSAN_OPTIONS="print_stacktrace=1")
        try:
            proc = subprocess.run([binary], input="1\n5\n9\n3\n7\n2\n8\n",
                                  capture_output=True, text=True, timeout=30, env=env)
            combined = proc.stdout + proc.stderr
            clean = ("ERROR: AddressSanitizer" not in combined
                     and "runtime error:" not in combined
                     and proc.returncode == 0)
            results.append(Result(
                "a full game under AddressSanitizer finishes clean", clean,
                "" if clean else _asan_summary(combined),
                combined[-2000:] if not clean else ""))
        except subprocess.TimeoutExpired:
            results.append(Result("a full game under AddressSanitizer finishes clean", False,
                                  "timed out"))
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)
    return results


def _asan_summary(text):
    m = re.search(r"ERROR: AddressSanitizer: (\S+)", text)
    if m:
        return ("AddressSanitizer reported %s. Run ./ttt check 6 --explain for the full report."
                % m.group(1))
    m = re.search(r"runtime error: (.+)", text)
    if m:
        return "UndefinedBehaviorSanitizer: %s" % m.group(1).strip()
    return "the sanitised build did not exit cleanly"


def check_stage_7():
    """Strategies, graded without naming a single one of the student's types.

    The computer opponent deliberately does NOT live inside createGame(): the
    contract tests drive both players by hand, and they must keep working. So
    the opponent is wired into the CLI behind --vs-computer, and graded through
    stdout plus the student's own test suite.
    """
    results = _contract_tests(7, gtest_filter="Contract.*")
    if any(not r.passed for r in results):
        return results

    binary = find_binary("ttt-cli")
    if not binary:
        raise Skip("no ttt-cli binary")

    out, code, stuck = _play_args(binary, ["--vs-computer"], ["5"])
    if stuck:
        results.append(Result("`ttt-cli --vs-computer` answers a move", False,
                              stuck_message(stuck, "in --vs-computer mode"),
                              frame.describe(out)))
        return results
    board = frame.last_frame(out)
    if board is None:
        results.append(Result(
            "`ttt-cli --vs-computer` prints a board after your move", False,
            "no board found in the output. The course needs this exact flag -- see "
            "docs/reference/build-contract.md",
            frame.describe(out)))
        return results

    marks = [i for i, cell in enumerate(board) if cell != "."]
    two_marks = len(marks) == 2
    results.append(Result(
        "the computer answers your move", two_marks,
        "" if two_marks else
        "after I typed one move I expected two marks on the board (yours and the "
        "computer's),\n  but found %d: %s" % (len(marks), "".join(board)),
        frame.describe(out) + "\n\n  I ran: ttt-cli --vs-computer, and typed: 5"))

    if two_marks:
        yours_landed = board[4] == "X"
        results.append(Result("your move still goes where you asked", yours_landed,
                              "" if yours_landed else "cell 4 holds %r, expected X" % board[4]))

    # The student writes their own tests this stage; we check they run and pass.
    # Build everything first: their test target has a name we cannot know, and
    # ctest will not build it for us. GoogleTest is already warm from Stage 5.
    built = cmake_build()
    if not (built and built.returncode == 0):
        results.append(Result("your own test target builds", False,
                              (built.stdout + built.stderr)[-1200:] if built else "timed out"))
        return results

    proc = run(["ctest", "--test-dir", BUILD, "--output-on-failure"], timeout=300)
    if proc is None:
        results.append(Result("your own tests pass under ctest", False, "ctest timed out"))
    else:
        total = len(re.findall(r"Test\s+#\d+:", proc.stdout))
        own = total - 1  # the course's contract suite is one of them
        passed = proc.returncode == 0
        results.append(Result(
            "you have written your own tests, and they pass", passed and own >= 1,
            "" if (passed and own >= 1) else
            ("ctest reported failures:\n" + proc.stdout[-1200:]) if not passed else
            "I only found the course's own test suite registered with ctest.\n"
            "  Add your strategy tests with add_test() in my-game/CMakeLists.txt."))
    return results


def _play_args(binary, args, moves, timeout=TIMEOUT):
    """Like play(), but with command-line arguments."""
    stdin = "".join("%s\n" % m for m in moves)
    with tempfile.TemporaryFile(mode="w+b") as sink, \
         tempfile.TemporaryFile(mode="w+b") as feed:
        feed.write(stdin.encode())
        feed.seek(0)
        proc = subprocess.Popen([binary] + args, stdin=feed, stdout=sink,
                                stderr=subprocess.STDOUT, start_new_session=True)
        stop_reason = None
        deadline = time.time() + timeout
        while proc.poll() is None:
            if os.fstat(sink.fileno()).st_size > RUNAWAY_BYTES:
                stop_reason = "runaway"
                break
            if time.time() > deadline:
                stop_reason = "timeout"
                break
            time.sleep(0.02)
        if stop_reason:
            _kill_tree(proc)
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                pass
        size = sink.seek(0, os.SEEK_END)
        sink.seek(max(0, size - MAX_CAPTURE))
        return (sink.read().decode("utf-8", "replace"),
                None if stop_reason else proc.returncode, stop_reason)


# ---------------------------------------------------------------------------
# Stage 8 -- the container, entirely black-box
# ---------------------------------------------------------------------------
def check_stage_8():
    import socket
    results = []
    dockerfile = os.path.join(ROOT, "Dockerfile")
    if not os.path.exists(dockerfile):
        raise Skip("no Dockerfile yet -- you write that one yourself this stage")
    results.append(Result("Dockerfile exists", True))

    if not shutil.which("docker"):
        raise Skip("docker is not installed")
    if run(["docker", "info"], timeout=30) is None:
        raise Skip("the docker daemon is not responding")

    tag = "ttt-course-check:latest"
    proc = run(["docker", "build", "-t", tag, ROOT], timeout=1800)
    built = proc is not None and proc.returncode == 0
    results.append(Result("docker build succeeds", built,
                          "" if built else (proc.stdout + proc.stderr)[-1500:] if proc
                          else "timed out"))
    if not built:
        return results

    proc = run(["docker", "image", "inspect", tag, "--format", "{{.Size}}"])
    if proc and proc.returncode == 0:
        size_mb = int(proc.stdout.strip()) / 1_000_000
        results.append(Result("the final image is under 150 MB", size_mb < 150,
                              "image is %.0f MB -- a multi-stage build keeps the compiler out "
                              "of the final image" % size_mb))

    # Find a free host port rather than assuming one.
    sock = socket.socket()
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()

    proc = run(["docker", "run", "-d", "--rm", "-p", "%d:8080" % port, tag], timeout=60)
    if not (proc and proc.returncode == 0):
        results.append(Result("the container starts", False,
                              (proc.stdout + proc.stderr)[-800:] if proc else "timed out"))
        return results
    cid = proc.stdout.strip()
    try:
        import time
        import urllib.error
        import urllib.request

        base = "http://127.0.0.1:%d" % port
        healthy = False
        for _ in range(30):
            try:
                with urllib.request.urlopen(base + "/api/health", timeout=2) as resp:
                    if resp.status == 200:
                        healthy = True
                        break
            except Exception:
                time.sleep(1)
        logs = run(["docker", "logs", cid], timeout=30)
        results.append(Result("the container answers /api/health", healthy,
                              "" if healthy else
                              "nothing answered on port 8080 inside the container.\n"
                              "  The most common cause is a server bound to 127.0.0.1 instead of "
                              "0.0.0.0:\n  inside a container, 127.0.0.1 is not reachable from your "
                              "machine.",
                              (logs.stdout + logs.stderr)[-1200:] if logs else ""))
        if healthy:
            req = urllib.request.Request(
                base + "/api/move", data=json.dumps({"cell": 4}).encode(),
                headers={"Content-Type": "application/json"}, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=5) as resp:
                    payload = json.load(resp)
                landed = payload.get("state", {}).get("board", [None] * 9)[4] == "x"
                results.append(Result("a move posted over HTTP lands on the board", landed,
                                      "" if landed else "response was: %s" % json.dumps(payload)[:400]))
            except Exception as exc:
                results.append(Result("a move posted over HTTP lands on the board", False, str(exc)))

            who = run(["docker", "exec", cid, "id", "-u"], timeout=30)
            if who and who.returncode == 0:
                nonroot = who.stdout.strip() != "0"
                results.append(Result("the container does not run as root", nonroot,
                                      "" if nonroot else
                                      "it runs as uid 0. Add a USER line to your Dockerfile."))
    finally:
        run(["docker", "rm", "-f", cid], timeout=60)
    return results


CHECKS = {
    0: check_stage_0, 1: check_stage_1, 2: check_stage_2, 3: check_stage_3,
    4: check_stage_4, 5: check_stage_5, 6: check_stage_6, 7: check_stage_7,
    8: check_stage_8,
}


# ---------------------------------------------------------------------------
# reporting
# ---------------------------------------------------------------------------
def stage_title(n):
    path = os.path.join(ROOT, "course", "stages", "%02d.json" % n)
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)["title"]
    except Exception:
        return "Stage %d" % n


def run_stage(n, explain=False, quiet=False):
    """Returns 'pass' | 'fail' | 'skip'."""
    try:
        results = CHECKS[n]()
    except Skip as exc:
        if not quiet:
            print("  %s %s" % (YELLOW("[skip]"), "Stage %d -- %s" % (n, exc)))
        return "skip"

    passed = all(r.passed for r in results) and bool(results)
    if not quiet:
        print("\n%s" % BOLD("Stage %d -- %s" % (n, stage_title(n))))
        for r in results:
            mark = GREEN("  PASS  ") if r.passed else RED("  FAIL  ")
            print("%s%s" % (mark, r.name))
            if not r.passed and r.detail:
                for line in str(r.detail).rstrip().splitlines():
                    print("        %s" % line)
            if explain and r.explain:
                print(DIM("        --- what I checked ---"))
                for line in str(r.explain).rstrip().splitlines():
                    print(DIM("        %s" % line))
    return "pass" if passed else "fail"


def main():
    args = sys.argv[1:]
    explain = "--explain" in args
    report = "--report" in args
    do_all = "--all" in args
    positional = [a for a in args if not a.startswith("-")]

    if do_all:
        outcomes = {}
        for n in range(0, MAX_STAGE + 1):
            outcomes[n] = run_stage(n, explain=explain)

        print("\n" + BOLD("Summary"))
        rows = []
        for n in range(0, MAX_STAGE + 1):
            sym = {"pass": "PASS", "fail": "FAIL", "skip": "--"}[outcomes[n]]
            rows.append("  %-4s Stage %d  %s" % (sym, n, stage_title(n)))
        print("\n".join(rows))

        # Contiguous-prefix rule: everything before the highest pass must pass.
        highest = max([n for n, o in outcomes.items() if o == "pass"], default=-1)
        regressions = [n for n in range(0, highest) if outcomes[n] == "fail"]

        if report and os.environ.get("GITHUB_STEP_SUMMARY"):
            with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
                fh.write("## Course checks\n\n| | Stage | |\n|---|---|---|\n")
                for n in range(0, MAX_STAGE + 1):
                    icon = {"pass": "✅", "fail": "❌", "skip": "⬜"}[outcomes[n]]
                    fh.write("| %s | %d | %s |\n" % (icon, n, stage_title(n)))
                fh.write("\nHighest stage passing: **%s**\n"
                         % (highest if highest >= 0 else "none yet"))
                if regressions:
                    fh.write("\n> **Regression:** stage(s) %s used to pass and now fail.\n"
                             % ", ".join(str(r) for r in regressions))

        if regressions:
            print("\n%s stage(s) %s fail but come before stage %d, which passes."
                  % (RED("Regression:"), ", ".join(str(r) for r in regressions), highest))
            return 1
        print("\nHighest stage passing: %s" % (highest if highest >= 0 else "none yet"))
        return 0

    stage = int(positional[0]) if positional else 0
    if stage not in CHECKS:
        print("No such stage: %s" % stage, file=sys.stderr)
        return 2

    worst = 0
    for n in range(0 if stage == 0 else 1, stage + 1):
        outcome = run_stage(n, explain=explain and n == stage, quiet=False)
        if outcome == "fail":
            worst = 1
        elif outcome == "skip" and n == stage:
            # You asked about this stage, so "nothing to check yet" is not a pass.
            worst = 1
    print()
    return worst


if __name__ == "__main__":
    sys.exit(main())
