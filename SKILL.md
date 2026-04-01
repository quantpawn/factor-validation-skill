---
name: factor-validation
description: Use this skill when you need to design, write, submit, debug, or interpret a third-party factor for the xgboost-exp-canary factor validation service. It covers the full loop: author a valid factor file, run validation against the hosted API, inspect task results and logs, and decide how to revise the factor based on FastCheck stages and metrics.
---

# Factor Validation

Use this skill for the complete factor iteration loop:

1. write one valid factor file
2. submit it to the factor validation service
3. inspect the result and task logs
4. decide whether to keep, invert, or revise the factor

## Start Here

- If the task is to write or repair factor code, read [references/factor_authoring.md](references/factor_authoring.md).
- If the task is to submit a factor or explain the service API, read [references/factor_validation_api.md](references/factor_validation_api.md).
- If the task is to judge whether a factor result is good or bad, read [references/factor_result_interpretation.md](references/factor_result_interpretation.md).
- If the task failed and you need to debug it, read [references/troubleshooting.md](references/troubleshooting.md).

## Default Operating Rules

- Produce exactly one public factor class per file.
- Keep the factor self-contained. Do not depend on local helper modules, config files, file I/O, or network calls.
- Use only `pandas`, `numpy`, and `FE.base_factor.BaseFactor` unless the user explicitly says otherwise.
- Prefer continuous outputs over very coarse bucketed outputs. FastCheck's cross-sectional and decile metrics are more informative when the signal varies smoothly across assets.
- Treat task state and validation result as different things. A task can be `done` while the factor result is still `failed_validation`.

## Validation Workflow

When asked to validate a factor:

1. make sure the class name matches the filename stem
2. submit the `.py` file to `POST /factor/verify/tasks`
3. inspect:
   - `data.result`
   - `stdout.log`
   - `stderr.log`
4. if validation failed, classify the failure by `stage`
5. revise the factor based on the failure mode or weak metrics

## Output Expectations

When helping a user, prefer this structure:

1. the factor file content or the exact change needed
2. the submission result summary
3. the key metrics or failure stage
4. the next revision advice

## Bundled Resources

- [references/factor_authoring.md](references/factor_authoring.md): required code shape, allowed imports, output contract, and authoring rules
- [references/factor_validation_api.md](references/factor_validation_api.md): API usage, task model, log endpoints, and Python/curl examples
- [references/factor_result_interpretation.md](references/factor_result_interpretation.md): how to read FastCheck metrics and decide whether a factor is promising
- [references/troubleshooting.md](references/troubleshooting.md): common failure stages and the usual fixes
- [scripts/submit_factor.py](scripts/submit_factor.py): small helper to submit one factor file to the hosted service
- [scripts/fetch_logs.py](scripts/fetch_logs.py): small helper to fetch `stdout.log` or `stderr.log` for one task
- [examples/sample_factor.py](examples/sample_factor.py): a valid example factor file
- [examples/sample_success_response.json](examples/sample_success_response.json): a compact successful validation response
- [examples/sample_failed_validation_response.json](examples/sample_failed_validation_response.json): a compact failure response
