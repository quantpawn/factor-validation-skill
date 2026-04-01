#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests


DEFAULT_BASE_URL = "https://factor-verifier-exp-21736345851.asia-southeast1.run.app"


def default_end_date() -> str:
    return (datetime.now(timezone.utc) - timedelta(days=1)).date().isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Submit one factor file for validation.")
    parser.add_argument("factor_file", type=Path, help="Path to the factor .py file")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--end-date", default=default_end_date())
    parser.add_argument("--lookback", default="365d")
    parser.add_argument("--interval", default="1d")
    parser.add_argument("--symbol-category", default="low-cap")
    parser.add_argument("--timeout-seconds", type=int, default=3600)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    with args.factor_file.open("rb") as f:
        response = requests.post(
            f"{args.base_url.rstrip('/')}/factor/verify/tasks",
            data={
                "end_date": args.end_date,
                "lookback": args.lookback,
                "interval": args.interval,
                "symbol_category": args.symbol_category,
            },
            files={
                "file": (args.factor_file.name, f, "text/x-python"),
            },
            timeout=args.timeout_seconds,
        )

    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
