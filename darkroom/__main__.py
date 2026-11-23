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
    parser.add_argument("--data-dir", help="application-owned data root")
    parser.add_argument("--port", type=int, default=8765, help="port on 127.0.0.1")
    return parser


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    print("not implemented yet: see #15", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
