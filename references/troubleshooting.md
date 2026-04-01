# Troubleshooting

Use this reference when validation returns `failed_validation` or when task logs show execution issues.

## Failure Stages

### `factor_discovery`

Meaning:

- the system could not identify exactly one factor

Typical causes:

- no valid public factor class found
- multiple unexpected factor classes found
- filename stem and class name do not line up cleanly

Usual fixes:

- keep exactly one public factor class per file
- make the class name match the filename stem
- remove extra helper classes from the file if they look like factors

### `factor_loading`

Meaning:

- the factor file or class could not be imported or instantiated

Typical causes:

- syntax error
- bad import
- constructor error
- class name mismatch

Usual fixes:

- keep imports to `pandas`, `numpy`, and `FE.base_factor.BaseFactor`
- check for syntax mistakes first
- make sure defaults live in `__init__`
- make sure the file and class names match exactly

### `factor_generation`

Meaning:

- the factor loaded, but `calculate()` failed

Typical causes:

- missing required input columns
- invalid rolling logic
- divide-by-zero or indexing bugs
- wrong assumptions about input shape

Usual fixes:

- validate required columns explicitly
- use `sort_values("date")`
- use `window_size = self._resolve_window_size(self.window, interval)`
- add numeric stabilizers like `1e-8` in denominators

### `metric_calculation`

Meaning:

- the factor generated, but one or more evaluation metrics could not be computed

Typical causes:

- too many repeated factor values
- missing top or bottom deciles
- nearly constant factor output in tail buckets

Usual fixes:

- make the final output more continuous
- avoid very short-window time-series ranks as the final output
- reduce aggressive clipping or bucketization

### `unexpected`

Meaning:

- an unclassified error escaped the normal handling path

Usual fixes:

- inspect both `stdout.log` and `stderr.log`
- separate factor-code bugs from service/integration bugs before revising the factor

## Log-Driven Debugging

When a task fails:

1. read `data.result.stage`
2. read `data.result.message`
3. fetch `stdout.log`
4. fetch `stderr.log`

Use the logs to answer:

- did the file load?
- did `calculate()` start?
- which required column was missing?
- was the failure a code error or just weak metrics?

## Fast Triage Rules

- If import failed: fix file shape or imports before changing factor logic.
- If generation failed: fix required columns and numeric logic.
- If metrics are weak but execution passed: keep the file shape and revise the signal idea.
- If tail metrics are missing but `rank_ic` and `rank_ir` are useful: treat the factor as possibly still valuable.
