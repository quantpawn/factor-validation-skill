# Factor Result Interpretation

Source: adapted from `commons/docs/factor-measure-skill.md`

## First Distinction

Do not confuse:

- task state
- validation result status

Example:

- task state = `done`
- validation result status = `failed_validation`

That means the service completed normally, but the factor itself did not pass validation.

## Validation Status Values

Common values:

- `passed`
- `failed_validation`
- `failed_execution`

## Failure Stages

### `factor_discovery`

Meaning:

- system could not identify exactly which factor to run

Common causes:

- no valid factor class found
- multiple unexpected factor classes

### `factor_loading`

Meaning:

- factor file or class could not be imported or instantiated

Common causes:

- syntax error
- bad import
- class/file name mismatch
- constructor error

### `factor_generation`

Meaning:

- factor loaded, but `calculate()` failed during FE generation

Common causes:

- missing required columns
- bad rolling logic
- numeric/indexing/runtime errors

### `metric_calculation`

Meaning:

- factor generated, but evaluation metrics could not be computed cleanly

Common causes:

- too many repeated factor values
- missing top/bottom deciles
- undefined tail-bucket correlation

### `unexpected`

Meaning:

- unclassified integration/runtime problem

## Core Metrics

### `rank_ic`

Meaning:

- average daily Spearman rank correlation between factor and forward returns

Heuristic threshold:

- `|rank_ic| > 0.05`

Interpretation:

- positive: higher factor values align with higher forward returns
- negative: factor may need inversion
- near zero: weak or noisy idea

### `rank_ir`

Meaning:

- mean daily rank IC divided by its standard deviation

Heuristic threshold:

- `|rank_ir| > 0.5`

Interpretation:

- stability metric
- decent IC + weak IR usually means unstable signal

### `top_decile_ic` / `bottom_decile_ic`

Meaning:

- signal quality within extreme tails

Use:

- tells whether strongest high-score or low-score assets are informative

### `top_decile_sharpe` / `bottom_decile_sharpe`

Meaning:

- practical return concentration of top/bottom buckets

Heuristic threshold:

- `|sharpe| > 1.0`

Interpretation:

- useful for evaluating economic usefulness of tails
- missing values often mean the output is too discrete for stable deciles

## Decision Heuristics

Use this simple loop:

- weak `rank_ic`: rethink the factor idea
- acceptable `rank_ic` but weak `rank_ir`: improve stability/normalization
- decent overall metrics but weak tails: improve tail separation
- sign opposite expectation: consider inversion
- decile metrics missing: make final output more continuous

## Practical Output

When summarizing a validation result for a user, answer:

1. Did the factor compile/load?
2. Did factor generation succeed?
3. Are `rank_ic` and `rank_ir` promising?
4. Are the tail metrics useful or weak?
5. What should be changed next?
