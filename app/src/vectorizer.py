from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


class Vectorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")

    def create_train_test_data(self, *arrays, test_size):
        outputs = tuple(train_test_split(*arrays, test_size=test_size))
        return (*outputs, )

    def train(self, values_1, values_2):
        str_values1 = [" ".join(samples) for samples in values_1]
        str_values2 = [" ".join(samples) for samples in values_2]
        model = self.vectorizer.fit_transform(str_values1 + str_values2)
        # how to save?
