import io
import json
import yaml


def load_yaml(filepath):
    with io.open(filepath, errors="ignore", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(filepath):
    with io.open(filepath, errors="ignore", encoding="utf-8") as f:
        return json.load(f)
