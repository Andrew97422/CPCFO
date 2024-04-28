from sentence_transformers import SentenceTransformer
from .utils import singleton
import pandas as pd
import nltk

@singleton
class Encoder:
    def __init__(self) -> None:
        self.model = SentenceTransformer("cointegrated/LaBSE-en-ru")
        self.stemmer = nltk.stem.snowball.SnowballStemmer("russian", True)

    def __call__(self, input, stem=False):
        input = pd.Series(input).astype(str)
        return self.model.encode(
            (input.apply(self.stemmer.stem) if stem else input).values,
            convert_to_tensor=True
        )