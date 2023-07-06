import json
from dataclasses import dataclass
import os
from identify_language import create_swiss_german_dictionary

import unicodedata

def replace_unicode_chars(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
        unicode_chars_dict = {
            '\u2018': "'",
            '\u00fc': "ü",
            '\u00e4': "ä",
            '\u00f6': "ö",
            '\u00e9': "é",
            '\u00e8': "è",
            '\u00e0': "à",
            '\u00e2': "â",
            '\u00e7': "ç",
            '\u00ea': "ê"
        }
        for key, value in unicode_chars_dict.items():
            text = text.replace(key, value)
        with open(output_file, 'w', encoding='utf-8') as output:
            output.write(text)

@dataclass
class Comment:
    """
    Dataclass for a simplified reddit comment
    """
    score: int
    id: str
    created_utc: int
    body: str

    def __hash__(self):
        return hash(self.id)

comments = []
deleted_count = 0

# Read all json files in ../json/raw_json_weeks and create a list of comments
for jsonfile in os.listdir("../json/raw_json_weeks"):
    with open(f"../json/raw_json_weeks/{jsonfile}", "r") as f:
        data = json.load(f)
    for comment in data:
        # Add all comments that are not deleted to the list
        if comment["body"] != "[deleted]":
            comments.append(Comment(comment["score"], comment["id"], comment["created_utc"], comment["body"]))
        else:
            deleted_count += 1

print(f"Removed {deleted_count} deleted comments")

# remove duplicates and print the amount of comments removed
comments_unique = list(set(comments))
print(f"Removed {len(comments) - len(comments_unique)} duplicate comments")

old_length = len(comments_unique)
# remove comments that contain no swiss german words
swiss_german_words = create_swiss_german_dictionary()
comments_unique = [comment for comment in comments_unique if any(word in swiss_german_words for word in comment.body.split())]

print(f"Removed {old_length - len(comments_unique)} comments that contain no swiss german words")
# approximate the total wordcount of the comments
total_wordcount = 0
for comment in comments_unique:
    total_wordcount += len(comment.body.split())
print(f"Total wordcount: {total_wordcount}")


print(f"Total comments: {len(comments_unique)}")
# create a new json file with the unique comments
with open("comments.json", "w") as f:
    # convert dataclass to dict
    comments_dict = [comment.__dict__ for comment in comments_unique]
    json.dump(comments_dict, f, indent=4)

# replace unicode characters
replace_unicode_chars("comments.json", "comments.json")