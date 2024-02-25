import nltk
from tqdm import tqdm
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
from nltk.util import ngrams
from typing import List

from src.configuration.configuration_tokenizer import ConfigurationTokenizer


class Tokenizer:
    punctuation = "!\"#$%&'()*+, -./:;<=>?@[\]^_`{|}~"
    eng_ascii = list(range(65, 91)) + list(range(97, 123))
    usual_encodings = list(range(33, 126))
    contractions = {
        "'m": "am",
        "'s": "is",
        "'n": "and",
        "'re": "are",
        "n't": "not",
        "'d": "would",
        "'ll": "will",
        "'ve": "have",
        "'em": "them",
        "e'en": "even",
        "e'er": "ever",
        "cuz": "because",
        "cap'n": "captain",
        "a'ight": "alright",
        "'cause": "because",
        "'gainst": "against",
    }

    def __init__(self, configuration: ConfigurationTokenizer):
        """
        Options for some variables:
            remove_stopwords: bool - True or False
            case_mode: str - "all" or "first_only"
            lemmatize: bool - True ot False

        :param configuration:
        """
        self.stopwords = nltk.corpus.stopwords.words("english")
        self.tokenizer = TreebankWordTokenizer()
        self.lemmatizer = WordNetLemmatizer()
        self.min_token_len: int = configuration.min_token_len
        self.remove_stopwords: bool = configuration.remove_stopwords
        self.case_mode: str = configuration.case_mode
        self.lemmatize: bool = configuration.lemmatize
        self.ngrams_size: int = configuration.ngrams_size

    def preprocess_sentences(self, sentences: List[str]) -> List[List[str]]:
        """
        Data processing entrypoint
        # consider one for loop with tqdm
        """
        sentence = None
        processed: List[List[str]] = []
        try:
            for idx, sentence in tqdm(enumerate(sentences)):
                # cleaning
                sentence = self._tokenize_treebank(sentence, self.min_token_len)
                sentence = self._resolve_contractions(sentence)
                sentence = self._remove_stopwords(sentence, self.remove_stopwords)  # True | False
                # normalization
                sentence = self._case_folding(sentence, self.case_mode)  # all | first_only
                sentence = self._lemmatize(sentence, self.lemmatize)  # True | False

                sentence_ngrammed = self._create_ngrams(sentence, self.ngrams_size)

                processed.append(sentence_ngrammed)
        except Exception:
            print(sentence)

        return processed

    @staticmethod
    def get_empty_ids(sentences: List[List[str]], threshold: int = 1):
        """
        Get indexes of sentences of len < that provided as threshold variable
        """
        empty_ids = []
        print(f"Tokenizer - looking for sentences of len < {threshold}")
        for idx, el in tqdm(enumerate(sentences)):
            if len(el) < threshold:
                empty_ids.append(idx)
        print(f"Tokenizer - there are {len(empty_ids)} sentences of len < {threshold}")
        return empty_ids

    @staticmethod
    def remove_empty_sentences(sentences: List[List[str]], empty_ids: List[int]):
        """
        Delete sentences which indexes are on empty_ids list
        """
        print(f"Tokenizer - deleting sentences")
        for idx in tqdm(sorted(empty_ids, reverse=True)):
            del sentences[idx]

    def _tokenize_treebank(self, sentence: str, min_token_len: int = 2) -> List[str]:
        """
        1a, 1b
        Tokenizes one sentence, is used by _tokenize_sentences
        """
        sentence = self.tokenizer.tokenize(sentence)
        # remove punctuation tokens
        sentence = [word for word in sentence if word not in self.punctuation]
        # remove trailing punctuation chars from the tokens
        sentence = [word[:-1] if word.endswith(tuple(self.punctuation)) else word for word in sentence]
        # remove fully not alphanumeric words
        sentence = [token for token in sentence if any([ch.isalnum() for ch in token])]
        for idx, token in enumerate(sentence):
            if any([True for ch in token if ord(ch) in self.eng_ascii]):
                token = "".join([ch for ch in token if ord(ch) in self.eng_ascii])
            sentence[idx] = token
        # as last - remove tokens of len==1
        sentence = [token for token in sentence if len(token) >= min_token_len]
        return sentence

    def _resolve_contractions(self, sentence: List[str]) -> List[str]:
        """
        1c
        """
        contr_keys = list(self.contractions.keys())
        sentence = [self.contractions[el] if el in contr_keys else el for el in sentence]
        return sentence

    def _remove_stopwords(self, sentence: List[str], run_job: bool = True) -> List[str]:
        """
        1d
        Delete stopwords from given tokenized sentence
        """
        if run_job:
            sentence = [token for token in sentence if token.lower() not in self.stopwords]
        return sentence

    def _case_folding(self, sentence: List[str], param: str = "all") -> List[str]:
        """
        1e
        some information is often communicated by capitalization of a word —
            for example, 'doctor' and 'Doctor' often have different meanings.
        hint: better approach for case normalization is to lowercase only the first
            word of a sentence and allow all other words to retain their capitalization
        """
        if param == "first_only":
            # lowercase first token in sentence if token is not an abbreviation
            sentence[0] = sentence[0].lower() if not sentence[0].isupper() else sentence[0]
        elif param == "all":
            # lowercase all tokens
            sentence = [token.lower() for token in sentence]

        return sentence

    def _lemmatize(self, sentence: List[str], run_job: bool = True) -> List[str]:
        """
        1f
        """
        if run_job:
            sentence = [self.lemmatizer.lemmatize(token) for token in sentence]
        return sentence

    def _create_ngrams(self, sentence: List[str], ngrams_size=1) -> List[str]:
        """
        2a
        """
        sentence_ngrams = list(ngrams(sentence, ngrams_size))
        sentence_ngrams = [" ".join(x) for x in sentence_ngrams]
        return sentence_ngrams
