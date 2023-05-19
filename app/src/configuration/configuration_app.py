from pydantic import BaseModel
from typing import List, Optional
from pathlib import PurePath as Path

from src.utils.data_load_save import load_yaml
from src.configuration.const import dir_input, path_configuration_app


class ConfigurationApp(BaseModel):
    smtp_host: str
    mail_address: str
    mail_recipient: str
    dataset_filename: str
    tokens_threshold: int
    test_size: float
    dir_root: str = str(Path(__file__).parent.parent.parent)

    @property
    def dataset_path(self):
        return str(Path(dir_input + "/" + self.dataset_filename))


if __name__ == "__main__":
    config_app = ConfigurationApp(**load_yaml(path_configuration_app))
    print(f"{config_app}")
    print(config_app.dataset_path)
