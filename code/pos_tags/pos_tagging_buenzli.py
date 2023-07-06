from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from data import import_buenzli, import_NOAH_sentences
import json
import tqdm
import threading

model = AutoModelForTokenClassification.from_pretrained("noeminaepli/swiss_german_pos_model")
tokenizer = AutoTokenizer.from_pretrained("noeminaepli/swiss_german_pos_model")

pos_tagger = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")



def pos_tag(text: str) -> list[dict]:
    """
    Tags a text with part of speech tags
    :param text: the text to be tagged
    :return: a list of tuples containing the token and its tag
    """
    return pos_tagger(text)

def tag_buenzli():
    # import the comments
    comments = import_buenzli("comments.json")
    # iterate over the comments and tag them
    for comment in tqdm.tqdm(comments):
        pos_tags = []
        for word in comment["body"].split():
            word.lower().strip(".,!?;:()[]{}")
            pos_tags.append(pos_tag(word))

        comment["POS"] = pos_tags

        for word in pos_tags:
            for tag_dict in word:
                for attr in tag_dict:
                    if not isinstance(tag_dict[attr], str):
                        tag_dict[attr] = str(tag_dict[attr])

    # write the comments to a new json file
    with open("comments_pos.json", "w") as f:
        json.dump(comments, f, indent=4)


if __name__ == "__main__":
    tag_buenzli()