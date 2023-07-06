import json
import xml.etree.ElementTree as ET
import os
def import_NOAH(path):
    """
    Imports the NOAH corpus into a list of strings
    :param path: path to NOAH corpus
    :return: list of strings
    """
    # get all files in path
    files = os.listdir(path)
    # create set of words used in corpus
    words = set()
    words_frequencies = {}
    sentences = []

    # iterate through files
    for file in files:
        # parse xml file
        tree = ET.parse(path + file)
        # get root element
        root = tree.getroot()
        # iterate through all text elements
        for article in root.iter("document"):
            for sent in article.iter("s"):
                # add sentence to list
                sentence = []
                for word in sent.iter("w"):
                    # add word to set
                    words.add(word.text)
                    sentence.append(word.text)
                    if word.text in words_frequencies:
                        words_frequencies[word.text] += 1
                    else:
                        words_frequencies[word.text] = 1
                sentences.append(sentence)

    # return set of words
    return words, words_frequencies, sentences


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

# remove punctuation
def remove_punct(corpus):
    corpus.pop(".", None)
    corpus.pop(",", None)
    corpus.pop(":", None)
    corpus.pop(";", None)
    corpus.pop("!", None)
    corpus.pop("?", None)
    corpus.pop("(", None)
    corpus.pop(")", None)
    corpus.pop("'", None)
    corpus.pop('"', None)
    corpus.pop("–", None)
    corpus.pop("..", None)
    corpus.pop("...", None)
    corpus.pop("«", None)
    corpus.pop("»", None)
    corpus.pop(" ", None)

NOAH_frequencies = import_NOAH("C:/Users/Dominic-Asus/Documents/UZH/Semester_4/CALiR/NOAH-Corpus-master/")[1]
remove_punct(NOAH_frequencies)


NOAH_frequencies_sorted = sorted(NOAH_frequencies.items(), key=lambda x: x[1], reverse=True)
# calculate the avg word length in the noahs corpus




# for each word length, count the number of words with that length
word_length_count = {}
for word in NOAH_frequencies_sorted:
    if len(word[0]) in word_length_count:
        word_length_count[len(word[0])] += word[1]
    else:
        word_length_count[len(word[0])] = 1

sum_length = sum([key * value for key, value in word_length_count.items()])
avg_NOAH = sum_length/sum(dict(NOAH_frequencies_sorted).values())
#print(avg_NOAH)

# plot the word length distribution
import matplotlib.pyplot as plt
from buenzli_frequencies import sorted_buenzli

# calculate the avg word length in the buenzli corpus


# for each word length, count the number of words with that length
word_length_count_buenzli = {}
for word in sorted_buenzli:
    if len(word[0]) in word_length_count_buenzli:
        word_length_count_buenzli[len(word[0])] += word[1]
    else:
        word_length_count_buenzli[len(word[0])] = 1

sum_length_buenzli = sum([key * value for key, value in word_length_count_buenzli.items()])
avg_buenzli = sum_length_buenzli/sum(dict(sorted_buenzli).values())
#print(avg_buenzli)

# as y-axis, use the percentage of words with that length
# set bars as see-through
NOAH_word_count = sum(word_length_count.values())
buenzli_word_count = sum(word_length_count_buenzli.values())

plt.bar(word_length_count.keys(), [x * 100 / NOAH_word_count for x in word_length_count.values()], alpha=0.5, color='orange', label='NOAH')
plt.bar(word_length_count_buenzli.keys(), [x * 100 / buenzli_word_count for x in word_length_count_buenzli.values()], alpha=0.5, color='grey', label='Buenzli')
# limit the x-axis to 20 and keep the labels as integers
plt.xlim(0, 25)
plt.xticks(range(0, 26, 1))
plt.legend()

# add title
plt.title("Word length distribution")

plt.xlabel("Word length")
plt.ylabel("Percentage")
plt.show()