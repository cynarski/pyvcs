import argparse
from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pyvcs", description="Python project version control system"
    )

    subparsers = parser.add_subparsers(dest="command", title="commands")

    subparsers.add_parser("init", help="Initialize a new PyVCS repository")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "init":
        print("init command is not implemented yet")
        return 0
    raise AssertionError(f"Unhandled command: {args.command}")
