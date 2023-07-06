
import langid
from py3langid.langid import LanguageIdentifier, MODEL_FILE
import langdetect
import spacy
from textblob import TextBlob as tb
import os
import xml.etree.ElementTree as ET

#load the file "dictionary"
from DOMINIC_import_dict import fr_word_ls, it_word_ls, en_word_ls

def import_NOAH(path):
    """
    Imports the NOAH corpus into a list of strings
    :param path: path to NOAH corpus
    :return: list of strings
    """
    # get all files in path
    files = os.listdir(path)
    # create set of words used in corpus
    articles = []

    # iterate through files
    for file in files:
        # parse xml file
        tree = ET.parse(path + file)
        # get root element
        root = tree.getroot()
        # iterate through all text elements
        for article in root.iter("document"):
            articles_ls = []
            articles.append(articles_ls)
            for sent in article.iter("s"):
                sent_ls = []
                articles_ls.append(sent_ls)
                for word in sent.iter("w"):
                    sent_ls.append(word.text)

    # return set of words
    return articles


identifier = LanguageIdentifier.from_pickled_model(MODEL_FILE, norm_probs=True)
identifier.set_languages(['de', 'en', 'fr', 'it'])

def identify_language(text):
    pass

NOAH_path = "C:/Users/Dominic-Asus/Documents/UZH/Semester_4/CALiR/NOAH-Corpus-master/"
NOAH = import_NOAH(NOAH_path)

count_supposed_foreign = 0
count_foreign = 0
count_words = 0

def swiss_german_check(word):
    #catch swiss german verbs in 2nd person plural that look like english participles
    if len(word) >= 4 and word[-2:] == "ed" and word[-4] == "e":
        return True
    elif word.lower() == "also":
        return True
    else:
        return False


for article in NOAH:
    for sentence in article:
        for word in sentence:
            count_in_sentence = 0
            count_words += 1
            word_analysis = identifier.classify(word)
            if word_analysis[1] > 0.95 and word_analysis[0] != 'de':
                count_supposed_foreign += 1
                if (word_analysis[0] == 'fr' and word in fr_word_ls) or (word_analysis[0] == 'it' and word in it_word_ls) or (word_analysis[0] == 'en' and word in en_word_ls) and swiss_german_check is False:
                    count_in_sentence += 1
                    #print(word)
                    #print(word_analysis)
                    count_foreign += 1
        if count_in_sentence >= len(sentence) > 2:
            print(f"Supposed foreign sentence: {sentence}")

            count_words += 1

print(count_supposed_foreign)
print(count_foreign)
print(count_words)