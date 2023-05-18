from pathlib import PurePath as Path

FILE_CONFIGURATION_APP = "configuration_app.yaml"

dir_root: str = str(Path(__file__).parent.parent.parent)
dir_configuration = str(Path(dir_root + "/input/configuration/"))

path_configuration_app: str = str(Path(dir_configuration + "/" + FILE_CONFIGURATION_APP))
