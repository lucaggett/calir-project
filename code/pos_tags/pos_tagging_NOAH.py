from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from data import import_NOAH_sentences

model = AutoModelForTokenClassification.from_pretrained("noeminaepli/swiss_german_pos_model")
tokenizer = AutoTokenizer.from_pretrained("noeminaepli/swiss_german_pos_model")

pos_tagger = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")



def pos_tag(text: str) -> list:
    """
    Tags a text with part of speech tags
    :param text: the text to be tagged
    :return: a list of tuples containing the token and its tag
    """
    return pos_tagger(text)


NOAH_corpus = import_NOAH_sentences("../NOAH-Corpus/")
NOAH_corpus_w_pos = []

counter = 0
for sent in NOAH_corpus:
    counter += 1
    if counter % 10 == 0:
        print(f"iteration: {counter}")
    NOAH_corpus_w_pos.append({"text": sent, "pos_tags": pos_tag(sent)})

for elem in NOAH_corpus_w_pos:

    print(elem["text"])
    print(elem["pos_tags"])
    print("\n")