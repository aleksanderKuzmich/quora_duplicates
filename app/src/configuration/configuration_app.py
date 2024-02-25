from pydantic import BaseModel
from typing import List, Optional
from pathlib import PurePath as Path

from src.utils.data_load_save import load_yaml
from src.configuration.const import dir_input, path_configuration_app


class ConfigurationApp(BaseModel):
    smtp_host: str
    mail_address: str
    dataset_filename: str
    tokens_threshold: int
    similarity_threshold: float
    test_size: float
    dir_root: str = str(Path(__file__).parent.parent.parent)
    mail_recipient: str = ""
    mail_password: str = ""

    @property
    def dataset_path(self):
        return str(Path(dir_input + "/" + self.dataset_filename))

    def set_env_data(self, env_data):
        self.mail_recipient = env_data["mail_recipient"]
        self.mail_password = env_data["mail_password"]


if __name__ == "__main__":
    config_app = ConfigurationApp(**load_yaml(path_configuration_app))
    print(f"{config_app}")
    print(config_app.dataset_path)
