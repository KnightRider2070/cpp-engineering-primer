#!/usr/bin/env python3
"""Read course/stages/*.json -- the single source of truth for stage content.

Both `ttt` and the VitePress site read these files. Neither one owns the text.

Usage:
    stagejson.py field   <stage> <key>        e.g. field 5 title
    stagejson.py hint    <stage> <level>      1-4
    stagejson.py checks  <stage>
    stagejson.py concepts <stage>
    stagejson.py prompt  <stage> <id>         composed, ready to paste
    stagejson.py prompts <stage>              list titles
    stagejson.py list                         all stages, "id<TAB>title<TAB>tagline"
    stagejson.py validate                     structural self-check
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
STAGES_DIR = os.path.join(ROOT, "course", "stages")

MAX_STAGE = 8
HINT_LEVELS = 4


def die(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def load(stage):
    path = os.path.join(STAGES_DIR, "%02d.json" % int(stage))
    if not os.path.exists(path):
        die("No such stage: %s (expected %s)" % (stage, path))
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def all_stages():
    out = []
    for n in range(0, MAX_STAGE + 1):
        path = os.path.join(STAGES_DIR, "%02d.json" % n)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                out.append(json.load(fh))
    return out


def compose_prompt(data, prompt):
    """Wrap a stage prompt in the tutor contract and the stage's knowledge bounds.

    The 'do not use' list is what stops an assistant from answering a Stage 2
    question with std::vector and lambdas. It is built from the stage JSON, so
    it stays correct as the course changes.
    """
    knows = ", ".join(data.get("knows", [])) or "very little C++ so far"
    not_yet = ", ".join(data.get("notYet", []))

    header = (
        "You are my tutor. Follow the rules in docs/ai/tutor-contract.md -- "
        "especially: do not give me a complete implementation unless I have used\n"
        "hint levels 1 through 4 and then explicitly say \"give me the answer\", and\n"
        "prefer syntax examples that are NOT about tic-tac-toe so I still have to\n"
        "apply the idea myself.\n\n"
        "I am on Stage %d (%s) of a C++ course.\n\n"
        "At this point I know: %s.\n"
        % (data["id"], data["title"], knows)
    )
    if not_yet:
        header += (
            "I have NOT learned yet: %s.\n"
            "Do not use anything from that list in your answer. If the good solution\n"
            "genuinely needs one of them, say so and tell me why, but do not teach it\n"
            "to me here.\n" % not_yet
        )
    header += "\nAsk me what I expected to happen before you tell me anything.\n\n---\n\n"
    return header + prompt["body"] + "\n"


def main():
    if len(sys.argv) < 2:
        die(__doc__)
    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "list":
        for data in all_stages():
            print("%d\t%s\t%s" % (data["id"], data["title"], data.get("tagline", "")))
        return

    if cmd == "validate":
        problems = []
        seen = 0
        for n in range(0, MAX_STAGE + 1):
            path = os.path.join(STAGES_DIR, "%02d.json" % n)
            if not os.path.exists(path):
                problems.append("stage %d: missing %s" % (n, path))
                continue
            seen += 1
            try:
                with open(path, encoding="utf-8") as fh:
                    data = json.load(fh)
            except ValueError as exc:
                problems.append("stage %d: invalid JSON (%s)" % (n, exc))
                continue

            for key in ("id", "slug", "title", "objective", "checks", "hints", "prompts"):
                if key not in data:
                    problems.append("stage %d: missing key '%s'" % (n, key))
            if data.get("id") != n:
                problems.append("stage %d: id field says %r" % (n, data.get("id")))
            if len(data.get("hints", [])) != HINT_LEVELS:
                problems.append(
                    "stage %d: has %d hints, needs exactly %d"
                    % (n, len(data.get("hints", [])), HINT_LEVELS)
                )
            if not data.get("checks"):
                problems.append("stage %d: no checks listed" % n)
            if not data.get("prompts"):
                problems.append("stage %d: no AI prompts" % n)

            slug = data.get("slug", "")
            doc = os.path.join(ROOT, "docs", "stages", "%d-%s.md" % (n, slug))
            if not os.path.exists(doc):
                problems.append("stage %d: no docs page at docs/stages/%d-%s.md" % (n, n, slug))

        for p in problems:
            print("FAIL  " + p)
        if problems:
            print("\n%d problem(s) across %d stage file(s)." % (len(problems), seen))
            sys.exit(1)
        print("OK    %d stages, all structurally valid." % seen)
        return

    if not args:
        die("%s needs a stage number" % cmd)
    data = load(args[0])

    if cmd == "field":
        if len(args) < 2:
            die("field needs a key")
        value = data.get(args[1], "")
        if isinstance(value, (list, dict)):
            print(json.dumps(value))
        else:
            print(value)

    elif cmd == "hint":
        if len(args) < 2:
            die("hint needs a level")
        level = int(args[1])
        hints = data.get("hints", [])
        if not 1 <= level <= len(hints):
            die("Stage %s has hint levels 1-%d" % (data["id"], len(hints)))
        print(hints[level - 1])

    elif cmd == "checks":
        for item in data.get("checks", []):
            print(item)

    elif cmd == "concepts":
        concepts = data.get("concepts", {})
        for track in ("cpp", "linux", "git"):
            items = concepts.get(track, [])
            if items:
                label = {"cpp": "C++", "linux": "Linux/tooling", "git": "Git"}[track]
                print("%s\t%s" % (label, ", ".join(items)))

    elif cmd == "prompts":
        for prompt in data.get("prompts", []):
            print("%d\t%s" % (prompt["id"], prompt["title"]))

    elif cmd == "prompt":
        if len(args) < 2:
            die("prompt needs an id")
        want = int(args[1])
        for prompt in data.get("prompts", []):
            if prompt["id"] == want:
                sys.stdout.write(compose_prompt(data, prompt))
                return
        die("Stage %s has no prompt %d" % (data["id"], want))

    else:
        die("Unknown command: %s\n%s" % (cmd, __doc__))


if __name__ == "__main__":
    main()
