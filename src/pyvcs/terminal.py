import os
import sys

from pyvcs.status import Status


RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BOLD = "\033[1m"


def supports_color() -> bool:
    return sys.stdout.isatty() and "NO_COLOR" not in os.environ


def colorize(text: str, color: str) -> str:
    if not supports_color():
        return text

    return f"{color}{text}{RESET}"


def print_status(status: Status) -> None:
    if not status.modified and not status.deleted and not status.untracked:
        print(colorize("Nothing to commit, working tree clean", GREEN))
        return

    if status.modified:
        print(colorize("Modified files:", BOLD))
        for path in status.modified:
            print(colorize(f"  modified:  {path}", YELLOW))

    if status.deleted:
        print(colorize("Deleted files:", BOLD))
        for path in status.deleted:
            print(colorize(f"  deleted:   {path}", RED))

    if status.untracked:
        print(colorize("Untracked files:", BOLD))
        for path in status.untracked:
            print(colorize(f"  untracked: {path}", RED))
