#!/usr/bin/env python3
import os
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    from check import CHECKS, evaluate
    if len(sys.argv) >= 3:
        homedir = sys.argv[1]
        destdir = sys.argv[2]
        current = os.path.join(homedir, destdir)
        base = os.path.dirname(current)
    else:
        base = os.getcwd()
    result = evaluate(base)
    for name in CHECKS:
        prefix = "Y" if result.get(name, False) else "N"
        print("%s - %s" % (prefix, name))


if __name__ == "__main__":
    main()
