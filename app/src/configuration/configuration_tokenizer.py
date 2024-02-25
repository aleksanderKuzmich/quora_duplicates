from pydantic import BaseModel, validator

from src.utils.data_load_save import load_yaml
from src.configuration.const import path_configuration_tokenizer


class ConfigurationTokenizer(BaseModel):
    min_token_len: int
    remove_stopwords: bool
    case_mode: str
    lemmatize: bool
    ngrams_size: int

    class Config:
        validate_assignment = True

    @validator("min_token_len")
    def set_min_token_len(cls, value):
        return value or 2

    @validator("remove_stopwords")
    def set_remove_stopwords(cls, value):
        return value or False

    @validator("case_mode")
    def set_case_mode(cls, value):
        if value in ["first_only", "all"]:
            return value
        elif value is None:
            return "all"
        else:
            print("Wrong parameter was given for \"case_mode\" variable. Value \"all\" will be set")
            return "all"

    @validator("lemmatize")
    def set_lemmatize(cls, value):
        return value or True

    @validator("ngrams_size")
    def set_ngrams_size(cls, value):
        return value or 1


if __name__ == "__main__":
    config = ConfigurationTokenizer(**load_yaml(path_configuration_tokenizer))
    print(config)
