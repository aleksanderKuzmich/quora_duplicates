from pydantic import BaseModel
from typing import List, Optional
from pathlib import PurePath as Path

from src.utils.data_loaders import load_yaml
from src.configuration.const import path_configuration_app


class ConfigurationApp(BaseModel):
    dir_root: str = str(Path(__file__).parent.parent.parent)
    smtp_host: str
    mail_address: str
    mail_recipient: str


if __name__ == "__main__":
    config_app = ConfigurationApp(**load_yaml(path_configuration_app))
    print(f"dir root: {config_app.smtp_host}")
