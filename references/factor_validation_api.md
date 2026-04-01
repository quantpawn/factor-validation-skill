# Factor Validation API

This service validates one factor immediately inside the upload request.

There is no background queue worker in the current deployment model.

## Hosted Base URL

Current hosted endpoint:

```text
https://factor-verifier-exp-21736345851.asia-southeast1.run.app
```

UI:

```text
https://factor-verifier-exp-21736345851.asia-southeast1.run.app/factor/verify/ui
```

## Default Submission Parameters

Unless the user says otherwise, use:

- `end_date = UTC today - 1 day`
- `lookback = 365d`
- `interval = 1d`
- `symbol_category = low-cap`

## Main Submit Endpoint

```text
POST /factor/verify/tasks
```

Multipart form fields:

- `end_date`
- `lookback`
- `interval`
- `symbol_category`
- `file`

Behavior:

1. check execution capacity
2. create a task folder
3. run FastCheck immediately
4. write logs and result files
5. return the completed task payload

If capacity is full, submission fails immediately with HTTP `503`.

## Task Inspection Endpoints

- `GET /factor/verify/tasks/{task_id}`
- `GET /factor/verify/tasks`
- `GET /factor/verify/tasks/{task_id}/logs/stdout.log`
- `GET /factor/verify/tasks/{task_id}/logs/stderr.log`

Important distinction:

- task state lives under `data.status.status`
- FastCheck result lives under `data.result`

A task may be `done` while `data.result.status` is still `failed_validation`.

## Python Example

```python
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

BASE_URL = "https://factor-verifier-exp-21736345851.asia-southeast1.run.app"
FACTOR_FILE = Path("MY_FACTOR.py")
END_DATE = (datetime.now(timezone.utc) - timedelta(days=1)).date().isoformat()

with FACTOR_FILE.open("rb") as f:
    response = requests.post(
        f"{BASE_URL}/factor/verify/tasks",
        data={
            "end_date": END_DATE,
            "lookback": "365d",
            "interval": "1d",
            "symbol_category": "low-cap",
        },
        files={
            "file": (FACTOR_FILE.name, f, "text/x-python"),
        },
        timeout=3600,
    )

response.raise_for_status()
payload = response.json()
print(json.dumps(payload, indent=2))
```

## curl Example

```bash
END_DATE=$(python - <<'PY'
from datetime import datetime, timedelta, timezone
print((datetime.now(timezone.utc) - timedelta(days=1)).date().isoformat())
PY
)

curl -X POST \
  "https://factor-verifier-exp-21736345851.asia-southeast1.run.app/factor/verify/tasks" \
  -F "end_date=${END_DATE}" \
  -F "lookback=365d" \
  -F "interval=1d" \
  -F "symbol_category=low-cap" \
  -F "file=@MY_FACTOR.py;type=text/x-python"
```

## How To Read The Response

Check these fields first:

- `data.task_id`
- `data.status.status`
- `data.result.status`
- `data.result.stage`
- `data.result.message`
- `data.result.metrics`
- `data.logs`

On failure, fetch:

- `stdout.log`
- `stderr.log`

Use those logs together with `data.result.stage` to decide the next fix.
