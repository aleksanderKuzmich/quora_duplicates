import nltk
import argparse

from src.utils.data_load_save import load_yaml, load_csv, save_parquet, load_parquet, save_pickle
from src.utils.get_general_metrics import get_general_metrics
from src.configuration.const import \
    path_configuration_app, \
    path_configuration_tokenizer, \
    path_processed_dataset, \
    path_trained_model, \
    message_template
from src.utils.dotenv import load_env_variables
from src.configuration.configuration_app import ConfigurationApp
from src.configuration.configuration_tokenizer import ConfigurationTokenizer
from src.tokenizer import Tokenizer
from src.vectorizer import Vectorizer
from src.mailing import send_mail

nltk.download("stopwords")
nltk.download("wordnet")


class App:
    def __init__(self):
        self.config_app = ConfigurationApp(**load_yaml(path_configuration_app))
        self.config_app.set_env_data(load_env_variables())
        self.config_tokenizer: ConfigurationTokenizer = ConfigurationTokenizer(**load_yaml(path_configuration_tokenizer))
        self.raw_data = None
        self.labels = None
        self.tokenizer = None
        self.tokenized_question_1 = None
        self.tokenized_question_2 = None
        self.test_data = None
        self.vectorizer = None
        self.model = None
        self.accuracy = None

    def load_dataset(self):
        self.raw_data = load_csv(self.config_app.dataset_path)
        self.raw_data = self.raw_data.dropna(axis=0).reset_index(drop=True)
        self.labels = self.raw_data.is_duplicate.tolist()

    def load_processed_dataset(self):
        processed_dataset = load_parquet(path_processed_dataset)
        self.tokenized_question_1 = processed_dataset.question1.tolist()
        self.tokenized_question_2 = processed_dataset.question2.tolist()
        self.labels = processed_dataset.is_duplicate.tolist()

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
        print(f"Amount of pairs where len of tokens < {self.config_app.tokens_threshold} is {len(empty_ids)}")

        Tokenizer.remove_empty_sentences(self.tokenized_question_1, empty_ids)
        Tokenizer.remove_empty_sentences(self.tokenized_question_2, empty_ids)
        Tokenizer.remove_empty_sentences(self.labels, empty_ids)
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
        self.vectorizer = Vectorizer()
        x1_train, x1_test, x2_train, x2_test, y_train, y_test = Vectorizer.create_train_test_data(
            self.tokenized_question_1,
            self.tokenized_question_2,
            self.labels,
            test_size=self.config_app.test_size
        )
        self.test_data = {"x1": x1_test, "x2": x2_test, "labels": y_test}
        self.model = self.vectorizer.train(self.tokenized_question_1, self.tokenized_question_2)

    def save_vectorizer(self):
        save_pickle(self.model, path_trained_model)

    def get_prediction(self):
        predictions = self.vectorizer.get_predictions(
            samples1=self.test_data["x1"],
            samples2=self.test_data["x2"],
            threshold=self.config_app.similarity_threshold
        )
        tn, fp, fn, tp = get_general_metrics(y_true=self.test_data["labels"], y_pred=predictions)
        print(f"correctly predicted not duplicates: {tn}")
        print(f"incorrectly predicted not duplicates: {fp}")
        print(f"incorrectly predicted duplicates: {fn}")
        print(f"correctly predicted duplicates: {tp}")
        self.accuracy = f"{round((tn+tp)/(tn+fp+fn+tp), 4)*100}%"

    def send_results_mail(self):
        subject = "Pipeline results"
        message = message_template.format(items_no=len(self.tokenized_question_1), accuracy=self.accuracy)
        send_mail(
            sender=self.config_app.mail_address,
            recipient=self.config_app.mail_recipient,
            password=self.config_app.mail_password,
            subject=subject,
            body=message
        )
        print(f"Mail has been sent to {self.config_app.mail_recipient}")

    def run(self, processed=None):
        if processed:
            self.load_processed_dataset()
        else:
            self.load_dataset()
            self.process_dataset()
            self.remove_short_samples()
            self.save_processed_dataset()

        self.train_vectorizer()
        self.save_vectorizer()
        self.get_prediction()
        self.send_results_mail()

    def run_with_processed_dataset(self):
        self.load_processed_dataset()
        self.train_vectorizer()
        self.save_vectorizer()
        self.get_prediction()
        self.send_results_mail()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pd", action="store_true")
    args = parser.parse_args()
    app = App()
    if args.pd:
        print("App - will run with processed dataset")
        app.run(processed=True)
    else:
        print("App - will process dataset")
        app.run()
