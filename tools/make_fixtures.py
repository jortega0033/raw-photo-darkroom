"""Original deterministic fixture generator (spec: Supported DNG profile, Deterministic fixtures)."""

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate the DNG test fixtures and a hash manifest that records the generator revision."
    )
    parser.add_argument("--out", required=True, help="output directory, for example tests/fixtures")
    parser.parse_args(argv)
    print("not implemented yet: see #11", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
