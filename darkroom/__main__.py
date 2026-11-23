"""Command line entry point: launches the local server on 127.0.0.1 (spec: Runtime and ownership)."""

import argparse
import sys

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m darkroom",
        description="Offline RAW photo darkroom. Serves on 127.0.0.1 only.",
    )
    parser.add_argument("--version", action="version", version=f"darkroom {__version__}")
    parser.add_argument("--data-dir", default="./darkroom-data", help="application-owned data root")
    parser.add_argument("--port", type=int, default=8765, help="port on 127.0.0.1")
    sub = parser.add_subparsers(dest="command")
    orphans = sub.add_parser("orphans", help="list or remove unreachable imported objects")
    group = orphans.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", help="list orphan objects")
    group.add_argument("--remove", action="store_true", help="remove orphan objects")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    ticket = "#25" if args.command == "orphans" else "#15"
    print(f"not implemented yet: see {ticket}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
