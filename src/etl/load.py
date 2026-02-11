"""Load cleaned datasets to processed storage."""
from __future__ import annotations

import pandas as pd

from src.config import PipelineConfig


def load_processed_data(clean_df: pd.DataFrame, config: PipelineConfig) -> None:
    clean_df.to_csv(config.data_processed_dir / "clean_events.csv", index=False)
