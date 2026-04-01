import numpy as np
import pandas as pd

from FE.base_factor import BaseFactor


class TAKER_BUY_QUOTE_VOLUME_SKEWNESS_COMPOSITE(BaseFactor):
    def __init__(self, name: str = "TAKER_BUY_QUOTE_VOLUME_SKEWNESS_COMPOSITE", window: str = "5D"):
        super().__init__(name=name, window=window)

    def calculate(self, data: pd.DataFrame, interval: str) -> pd.DataFrame:
        required_columns = [
            "quote_asset_volume",
            "taker_buy_quote_asset_volume",
            "number_of_trades",
        ]
        missing = [col for col in required_columns if col not in data.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        result = data.copy().sort_values("date")
        window_size = self._resolve_window_size(self.window, interval)

        taker_buy_ratio = result["taker_buy_quote_asset_volume"] / (result["quote_asset_volume"] + 1e-8)
        avg_trade_size = result["quote_asset_volume"] / (result["number_of_trades"] + 1e-8)

        ratio_mean = taker_buy_ratio.rolling(window_size, min_periods=window_size).mean()
        ratio_q10 = taker_buy_ratio.rolling(window_size, min_periods=window_size).quantile(0.1)
        ratio_q90 = taker_buy_ratio.rolling(window_size, min_periods=window_size).quantile(0.9)

        trade_mean = avg_trade_size.rolling(window_size, min_periods=window_size).mean()
        trade_q10 = avg_trade_size.rolling(window_size, min_periods=window_size).quantile(0.1)
        trade_q90 = avg_trade_size.rolling(window_size, min_periods=window_size).quantile(0.9)

        ratio_mid = (ratio_q10 + ratio_q90) / 2.0
        ratio_half_range = (ratio_q90 - ratio_q10) / 2.0
        trade_mid = (trade_q10 + trade_q90) / 2.0
        trade_half_range = (trade_q90 - trade_q10) / 2.0

        ratio_component = ((ratio_mean - ratio_mid) / (ratio_half_range + 1e-8)).clip(-1.0, 1.0)
        trade_component = ((trade_mean - trade_mid) / (trade_half_range + 1e-8)).clip(-1.0, 1.0)

        result["tbqv_skew_comp"] = ratio_component * trade_component
        return self.format_output(result, "tbqv_skew_comp")
