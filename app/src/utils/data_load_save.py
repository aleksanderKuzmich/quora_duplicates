import io
import json
import yaml
import pandas as pd
from pathlib import PurePath as Path


def load_yaml(filepath):
    with io.open(filepath, errors="ignore", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(filepath):
    with io.open(filepath, errors="ignore", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path: Path) -> pd.DataFrame:
    raw_data = pd.read_csv(path)
    raw_data = raw_data.dropna(axis=0).reset_index(drop=True)
    return raw_data


def save_parquet(columns, values, path):
    assert len(columns) == len(values), f"Amount of columns ({len(columns)} is not equal to first dimension of " \
                                        f"values shape ({len(values)})"
    data = {key: value for (key, value) in zip(columns, values)}
    df_to_save = pd.DataFrame(data)
    df_to_save.to_parquet(path)
    print(f"Successfully saved to {path}")