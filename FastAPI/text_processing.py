import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

import string

from sklearn.feature_extraction.text import CountVectorizer

nltk.download("stopwords")
stemmer = PorterStemmer()
stopwords_set = set(stopwords.words("english"))
vectorizer = CountVectorizer()


def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )  # Remove punctuation
    words = text.split()  # Split into words
    words = [
        stemmer.stem(word) for word in words if word not in stopwords_set
    ]  # Stem and remove stopwords
    return " ".join(words)


raw_text = "Participate in a lottery and win car for free!"
processed_text = preprocess_text(raw_text)

print("processed_text: ", processed_text)
