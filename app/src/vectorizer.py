from tqdm import tqdm
from src.utils.cosine_sim import cosine_sim
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


class Vectorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    @staticmethod
    def create_train_test_data(*arrays, test_size):
        outputs = train_test_split(*arrays, test_size=test_size, random_state=20)
        return (*outputs, )

    @staticmethod
    def _convert_samples(samples):
        return [" ".join(sentence) for sentence in samples]

    def train(self, samples1, samples2):
        print("Vectorizer - start train")
        str_values1 = Vectorizer._convert_samples(samples1)
        str_values2 = Vectorizer._convert_samples(samples2)
        model = self.vectorizer.fit(str_values1 + str_values2)
        print("Vectorizer - successfully trained")
        return model

    def get_predictions(self, samples1, samples2, threshold):
        str_values1 = Vectorizer._convert_samples(samples1)
        str_values2 = Vectorizer._convert_samples(samples2)
        prediction = []
        for idx in tqdm(range(len(str_values1))):
            tfidf_value1 = list(self.vectorizer.transform([str_values1[idx]]).toarray()[0])
            tfidf_value2 = list(self.vectorizer.transform([str_values2[idx]]).toarray()[0])
            similarity = cosine_sim(tfidf_value1, tfidf_value2)
            if similarity > threshold:
                prediction.append(1)
            else:
                prediction.append(0)
        return prediction
