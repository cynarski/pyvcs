import argparse
from collections.abc import Sequence

from pyvcs.repository import Repository
from pyvcs.status import get_status
from pyvcs.terminal import print_status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pyvcs",
        description="Python project version control system",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
    )

    # pyvcs init [path]
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize a new PyVCS repository",
    )

    init_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path where the repository should be initialized",
    )

    # pyvcs status
    status_parser = subparsers.add_parser(
        "status",
        help="Find changes in repository",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    match args.command:
        case "init":
            repo = Repository.init(args.path)
            print(f"Initialized empty PyVCS repository in {repo.repo_path}")
            return 0
        case "status":
            repo = Repository.find()
            status = get_status(repo)
            print_status(status)
            return 0
        case _:
            raise AssertionError(f"Unhandled command: {args.command}")
