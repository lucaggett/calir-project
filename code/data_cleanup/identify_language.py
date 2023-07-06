import random
import xml.etree.ElementTree as ET
import json
import logging
from collections import Counter
from typing import List
import os
import numpy as np


def import_NOAH_sentences(path):
    """
    Imports the NOAH corpus into a list of strings
    This function needs to reconstruct the sentences from the singular words, as the sentences are not stored in the corpus
    """
    # get all files xml files in path
    files = os.listdir(path)
    sentences = []

    # iterate through files
    for file in files:
        if file.endswith(".xml"):
            # parse xml file
            tree = ET.parse(path + file)
            # get root element
            root = tree.getroot()
            # iterate through all text elements
            for article in root.iter("document"):
                for sent in article.iter("s"):
                    # add sentence to list
                    sentence = ""
                    for word in sent.iter("w"):
                        # add word to set
                        sentence += word.text + " "
                    sentences.append(sentence)

    return sentences

def import_buenzli(path) -> list[dict[str, str]]:
    """
    import the buenzli corpus as sentences
    """
    with open(path, "r") as f:
        comments = json.load(f)

    sentences = []
    for comment in comments:
        sentences.append(comment)

    return sentences



def create_swiss_german_dictionary() -> set:
    """
    Creates a set of swiss german words from files contained in NOAHs corpus
    :return: a set of swiss german words
    """
    word_count = 0
    sentence_count = 0
    # files are in NOAH-corpus/ and are as follows: blick.xml, blogs.xml, schobinger.xml, swatch.xml, wiki.xml
    files = ("blick.xml", "blogs.xml", "schobinger.xml", "swatch.xml", "wiki.xml")
    swiss_german_words = set()
    for file in files:
        tree = ET.parse(f"../NOAH-Corpus/{file}")
        root = tree.getroot()
        for article in root:
            for sentence in article:
                sentence_count += 1
                for word in sentence:
                    word_count += 1
                    swiss_german_words.add(word.text)
    return swiss_german_words


class NgramTokenizer:
    def __init__(self, ngram_order: int):
        self.ngram_order = ngram_order

    def __call__(self, text: str) -> List[str]:
        """
        Tokenize text into ngrams, yielding each ngram in turn to reduce memory usage. This assumes the text is already pretokenized and split by spaces
        """

        tokens = text.split(" ")

        for i in range(len(tokens) - self.ngram_order + 1):
            yield " ".join(tokens[i:i + self.ngram_order])


class BigramLanguagePredictor:

    def __init__(self, ngram_order: int = None):

        self.ngram_order = ngram_order

        self.probs = {}

    def create_propabilities(self, text: str):
        """
        Train language model on text, should be able to recognise if a given ngram is in the language it was trained on
        """

        tokenizer = NgramTokenizer(self.ngram_order)

        ngrams = tokenizer(text)
        count = Counter(ngrams)
        total = sum(count.values())
        self.probs = {ngram: np.log(count[ngram] / total) for ngram in count}

    def predict(self, text: str):
        """
        Predict the probability of a given text being in the language the model was trained on
        """
        tokenizer = NgramTokenizer(self.ngram_order)

        ngrams = tokenizer(text)
        ngrams = [ngram for ngram in ngrams]

        # We do not apply any smoothing here, so we simply use a very low probability for unknown ngrams
        return sum(self.probs[ngram] if ngram in self.probs else -100 for ngram in ngrams) / (1 + len(ngrams)/5)


def create_swiss_german_model():
    sentences = import_NOAH_sentences("../NOAH-Corpus/")

    model = BigramLanguagePredictor(ngram_order=2)
    model.create_propabilities(" ".join(sentences))
    return model

def create_english_model():
    with open("../other_data/train.en", "r", encoding="utf-8") as f:
        text = f.readlines()

    model = BigramLanguagePredictor(ngram_order=2)
    model.create_propabilities(" ".join(text))
    return model

def create_german_model():
    with open("../other_data/train.de", "r", encoding="utf-8") as f:
        text = f.readlines()

    model = BigramLanguagePredictor(ngram_order=2)
    model.create_propabilities(" ".join(text))
    return model

def create_dutch_model():
    with open("../other_data/train.nl", "r", encoding="utf-8") as f:
        text = f.readlines()

    model = BigramLanguagePredictor(ngram_order=2)
    model.create_propabilities(" ".join(text))
    return model

def create_italian_model():
    with open("../other_data/train.it", "r", encoding="utf-8") as f:
        text = f.readlines()

    model = BigramLanguagePredictor(ngram_order=2)
    model.create_propabilities(" ".join(text))
    return model

def create_french_model():
    with open("../other_data/clean_train.fr", "r", encoding="utf-8") as f:
        text = f.readlines()

    model = BigramLanguagePredictor(ngram_order=2)
    model.create_propabilities(" ".join(text))
    return model

def main():
    logging.basicConfig(level=logging.INFO)
    models = {
        "GSW": create_swiss_german_model(),
        "EN": create_english_model(),
        "DE": create_german_model(),
        #"NL": create_dutch_model(), Deprecated because of lack of occurrences in the corpus
        "FR": create_french_model(),
        "IT": create_italian_model(),
    }

    buenzli_corpus = import_buenzli("../buenzli-corpus/comments.json")

    for comment in buenzli_corpus:
        comment["language"] = (max(models, key=lambda x: models[x].predict(comment["body"])))

    GSW_comments = []
    other_comments = {lang: [] for lang in models if lang != "GSW"}

    # The code block belows prints some comments from each language. it's not very pretty, but the output is what was important

    for comment in buenzli_corpus:
        if comment["language"] != "GSW":
            other_comments[comment["language"]].append(comment["body"])
        else:
            GSW_comments.append(comment["body"])
    print("\n"*5)
    print("GSW: ", len(GSW_comments))
    for lang in other_comments:
        print(lang, len(other_comments[lang]))

    # print a sample of the each language
    for lang in other_comments:
        print("\n"*5)
        print("*"*10, lang, "*"*10)
        for comment in random.sample(other_comments[lang], 50):
            print(comment)
            print("-"*20)

        print("\n"*5)
        print("*"*10, "GSW", "*"*10)
        for comment in random.sample(GSW_comments, 10):
            print(comment)
            print("-"*20)

    #for each language, print the number of comments
    for lang in other_comments:
        print(lang, len(other_comments[lang]))

    with open("comments.json", "w") as f:
        json.dump(buenzli_corpus, f, indent=2)


    """
    This performs pretty okay overall. 
    The dutch classification mostly catches swiss german sentences, so it could be removed.
    The italian classification is catches some swiss german sentences
    
    GSW: 51853
    non-GSW: 7098
    EN: 1242
    DE: 5583
    NL: 206
    IT: 67
    FR: ?
    """

if __name__ == "__main__":
    main()