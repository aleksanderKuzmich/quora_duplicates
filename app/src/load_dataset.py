import pandas as pd
from pathlib import PurePath as Path


def load_csv(path: Path) -> pd.DataFrame:
    raw_data = pd.read_csv(path)
    raw_data = raw_data.dropna(axis=0).reset_index(drop=True)
    return raw_data
