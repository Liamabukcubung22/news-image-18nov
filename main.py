"""Entry program for make.fun bounty news-image-20261118.

Copies the pre-rendered poster ``entry.png`` (Wednesday 18 November 2026
world news) to ``$MAKEFUN_OUTPUT_DIR/entry.png`` (default ``/output``).
Standard library only; no network, no rendering at run time.
"""

import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    if not os.path.isfile(SRC):
        raise FileNotFoundError("entry.png missing next to main.py")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
