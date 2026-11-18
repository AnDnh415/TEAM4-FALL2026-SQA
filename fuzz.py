import random
import string
import sys

import parser
import scanner
import graphtaint

random.seed(5710)
ITERATIONS = 1000
REPORT_FILE = "fuzz_report.txt"
crashes = []


# shared helpers feeding unexpected inputs automatically and watching whether it crashes
def randomString(max_len=50):
    pool = string.printable + "äöü漢字😀\x00"
    return "".join(random.choice(pool) for _ in range(random.randint(0, max_len)))


def randomValue(depth=0):
    choices = [
        lambda: None,
        lambda: random.randint(-10**9, 10**9),
        lambda: random.random(),
        lambda: randomString(),
        lambda: True,
        lambda: b"\xff\xfe",
    ]
    if depth < 3:
        choices.append(lambda: [randomValue(depth + 1) for _ in range(random.randint(0, 4))])
        choices.append(lambda: {randomString(10): randomValue(depth + 1) for _ in range(random.randint(0, 4))})
    return random.choice(choices)()


def deepNest(levels=2000):
    d = "leaf"
    for i in range(levels):
        d = {"k" + str(i): d}
    return d


def runFuzz(name, func, input_gen, iterations=ITERATIONS):
    seen = set()
    for _ in range(iterations):
        args = input_gen()
        try:
            func(*args)
        except Exception as e:
            sig = (name, type(e).__name__)
            if sig not in seen:
                seen.add(sig)
                crashes.append((name, type(e).__name__, str(e)[:120], repr(args)[:120]))
    print(f"[{name}] {iterations} inputs, {len(seen)} distinct crash type(s)")


# ================= SECTION 1: parser.py =================

# 1. parser.checkIfWeirdYAML  (example of the pattern)
def fuzz_checkIfWeirdYAML():
    runFuzz("parser.checkIfWeirdYAML", parser.checkIfWeirdYAML,
            lambda: (randomValue(),))

# 2. parser.keyMiner(dic_, value)
# TODO

# 3. parser.getKeyRecursively(dict_, list2hold, depth_)
# TODO

# 4. parser.getValuesRecursively(dict_)   -- generator: call list() on it
# TODO

# 5. parser.getValsFromKey(dict_, target, list_holder)
# TODO

SECTION_1 = [
    fuzz_checkIfWeirdYAML,
    # add the other Section 1 functions here
]


# ================= SECTION 2: scanner.py / graphtaint.py =================

# 6. scanner.isValidUserName(uName)
# TODO
def fuzz_isValidUserName():
    runFuzz("scanner.isValidUserName", scanner.isValidUserName, lambda: randomString(),)

# 7. scanner.isValidPasswordName(pName)
# TODO

# 8. scanner.isValidKey(keyName)
# TODO

# 9. scanner.checkIfValidSecret(single_config_val)
# TODO

# 10. graphtaint.constructHelmString(hiera_tuple)
# TODO

SECTION_2 = [
    # add Section 2 functions here
    fuzz_isValidUserName,
]

# report entries
def writeReport():
    with open(REPORT_FILE, "w") as f:
        f.write(f"Fuzzing report: {len(crashes)} distinct crash(es)\n\n")
        for name, etype, msg, args in crashes:
            f.write(f"METHOD: {name}\nEXCEPTION: {etype}: {msg}\nINPUT: {args}\n\n")
    print(f"Report written to {REPORT_FILE}")


if __name__ == "__main__":
    for fuzzer in SECTION_1 + SECTION_2:
        fuzzer()
    writeReport()
    sys.exit(0)