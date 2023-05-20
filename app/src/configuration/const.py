from pathlib import PurePath as Path

FILE_CONFIGURATION_APP = "configuration_app.yaml"
FILE_CONFIGURATION_TOKENIZER = "configuration_tokenizer.yaml"
FILE_PROCESSED_DATASET = "dataset.parquet"
FILE_TRAINED_MODEL = "model.pickle"

dir_root = str(Path(__file__).parent.parent.parent)
dir_input = str(Path(dir_root + "/input"))
dir_output = str(Path(dir_root + "/output"))
dir_input_configuration = str(Path(dir_input + "/configuration"))

path_configuration_app = str(Path(dir_input_configuration + "/" + FILE_CONFIGURATION_APP))
path_configuration_tokenizer = str(Path(dir_input_configuration + "/" + FILE_CONFIGURATION_TOKENIZER))
path_processed_dataset = str(Path(dir_output + "/" + FILE_PROCESSED_DATASET))
path_trained_model = str(Path(dir_output + "/" + FILE_TRAINED_MODEL))

message_template = (
    "Model has been successfully trained on {items_no} pairs and it's accuracy is {accuracy}.\n\nBest regards,\n"
    "Quora duplicates project!"
)
