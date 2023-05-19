from src.utils.data_load_save import load_yaml, load_csv, save_parquet
from src.configuration.const import path_configuration_app, path_configuration_tokenizer, path_processed_dataset
from src.configuration.configuration_app import ConfigurationApp
from src.configuration.configuration_tokenizer import ConfigurationTokenizer
from src.tokenizer import Tokenizer
from src.vectorizer import Vectorizer


class App:
    def __init__(self):
        self.config_app = ConfigurationApp(**load_yaml(path_configuration_app))
        self.config_tokenizer: ConfigurationTokenizer = ConfigurationTokenizer(**load_yaml(path_configuration_tokenizer))
        self.raw_data = None
        self.labels = None
        self.tokenizer = None
        self.tokenized_question_1 = None
        self.tokenized_question_2 = None

    def load_dataset(self):
        self.raw_data = load_csv(self.config_app.dataset_path)
        self.raw_data = self.raw_data.dropna(axis=0).reset_index(drop=True)
        self.labels = self.raw_data.is_duplicate.tolist()

    def process_dataset(self):
        self.tokenizer = Tokenizer(self.config_tokenizer)
        raw_question_1 = self.raw_data.question1.tolist()
        raw_question_2 = self.raw_data.question2.tolist()
        self.tokenized_question_1 = self.tokenizer.preprocess_sentences(raw_question_1)
        self.tokenized_question_2 = self.tokenizer.preprocess_sentences(raw_question_2)

    def remove_short_samples(self):
        empty_ids = []
        empty_ids.extend(Tokenizer.get_empty_ids(self.tokenized_question_1, threshold=self.config_app.tokens_threshold))
        empty_ids.extend(Tokenizer.get_empty_ids(self.tokenized_question_2, threshold=self.config_app.tokens_threshold))
        empty_ids = list(set(empty_ids))
        print(f"Amount of pairs where len of sample < {self.config_app.tokens_threshold} is {empty_ids}")

        Tokenizer.remove_empty_sentences(self.tokenized_question_1, empty_ids)
        Tokenizer.remove_empty_sentences(self.tokenized_question_2, empty_ids)
        # run additional check
        empty_ids = []
        empty_ids.extend(Tokenizer.get_empty_ids(self.tokenized_question_1, threshold=self.config_app.tokens_threshold))
        empty_ids.extend(Tokenizer.get_empty_ids(self.tokenized_question_2, threshold=self.config_app.tokens_threshold))
        assert len(empty_ids) == 0, f"Empty ids list after removal is not empty, len: {len(empty_ids)}"

    def save_processed_dataset(self):
        columns = ["question1", "question2", "is_duplicate"]
        values = [self.tokenized_question_1, self.tokenized_question_2, self.labels]
        save_parquet(columns, values, path_processed_dataset)

    def train_vectorizer(self):
        vectorizer = Vectorizer()
        x1_train, x1_test, x2_train, x2_test, y_train, y_test = vectorizer.create_train_test_data(
            self.tokenized_question_1,
            self.tokenized_question_2,
            self.labels,
            test_size=self.config_app.test_size
        )
        vectorizer.train(x1_train, x2_train)
        # TODO: save model
        # TODO: implement prediction + metrics
