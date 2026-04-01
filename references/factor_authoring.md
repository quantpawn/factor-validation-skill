# Factor Authoring

This reference defines the writing contract for a third-party factor.

## Goal

Produce one self-contained Python file that defines one factor class.

The file should be portable:

- no dependency on local helper modules
- no dependency on config JSON
- no file I/O
- no network calls
- no dependence on local runtime state outside the input DataFrame

The only repo-level dependency the factor may assume is a `BaseFactor` class with:

- `__init__(name, window=None)`
- `_resolve_window_size(window, interval)`
- `format_output(df, value_column)`

Allowed imports:

- `pandas`
- `numpy`
- `FE.base_factor.BaseFactor`

## Required Code Shape

1. One `.py` file per factor.
2. One public factor class per file.
3. Class name must equal the factor name.
4. The class must inherit from `BaseFactor`.
5. Required defaults belong in `__init__`, especially `window`.
6. The full factor logic must be implemented inside the file itself.
7. Do not import project-specific helper utilities.

## Input Schema

`calculate(self, data: pd.DataFrame, interval: str)` receives a DataFrame for one symbol.

Expected columns may include:

- `date`
- `coin_name`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `quote_asset_volume`
- `number_of_trades`
- `taker_buy_base_asset_volume`
- `taker_buy_quote_asset_volume`

Validate the columns you need and raise a clear `ValueError` if they are missing.

## Output Schema

`calculate()` must return a pandas DataFrame with these semantic columns:

- `factor`
- `date`
- `coin_name`

Preferred pattern:

```python
result = data.copy().sort_values("date")
result["my_factor_value"] = ...
return self.format_output(result, "my_factor_value")
```

Output rules:

- keep one output row per input row
- do not drop rows inside `calculate()`
- allow early rows to be `NaN` when the rolling window is unavailable
- ensure the factor value column is numeric before calling `format_output`

## Minimal Template

```python
import pandas as pd

from FE.base_factor import BaseFactor


class MY_FACTOR(BaseFactor):
    def __init__(self, name: str = "MY_FACTOR", window: str = "20D"):
        super().__init__(name=name, window=window)

    def calculate(self, data: pd.DataFrame, interval: str) -> pd.DataFrame:
        required_columns = ["close"]
        missing = [col for col in required_columns if col not in data.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        result = data.copy().sort_values("date")
        window_size = self._resolve_window_size(self.window, interval)
        result["my_factor_value"] = (
            result["close"] / result["close"].rolling(window_size).mean() - 1.0
        )
        return self.format_output(result, "my_factor_value")
```

## FastCheck-Friendly Design

Preferred output behavior:

- produce a continuous numeric signal when possible
- keep enough cross-sectional variation across assets on the same date
- allow warmup `NaN` instead of forcing unstable early values
- prefer ratios, deviations, z-scores, or scaled spreads

Avoid these final-output patterns when possible:

- very short-window percentile ranks like `TS_RANK(..., 3D)` or `TS_RANK(..., 5D)`
- outputs with only a few repeated buckets
- hard clipping into a tiny number of discrete levels
- `min_periods=1` on long-window statistics when it creates unstable early rows

Why this matters:

- decile metrics split the universe into quantiles per date
- too many tied values can make top or bottom deciles undefined
- coarse outputs often weaken tail metrics even when the code itself is valid

## Delivery Checklist

Before submitting a factor, check:

- filename stem equals class name
- class inherits from `BaseFactor`
- factor code is self-contained
- required columns are validated
- `calculate()` returns `format_output(...)`
- output is numeric and reasonably continuous
