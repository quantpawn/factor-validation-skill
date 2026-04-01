import argparse
from pathlib import Path

import requests


DEFAULT_BASE_URL = "https://factor-verifier-exp-21736345851.asia-southeast1.run.app"


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch factor validation task logs.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--task-id", required=True)
    parser.add_argument(
        "--log-type",
        choices=["stdout", "stderr"],
        default="stderr",
    )
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args()

    log_filename = f"{args.log_type}.log"
    response = requests.get(
        f"{args.base_url.rstrip('/')}/factor/verify/tasks/{args.task_id}/logs/{log_filename}",
        timeout=args.timeout_seconds,
    )
    response.raise_for_status()
    print(response.text)


if __name__ == "__main__":
    main()
