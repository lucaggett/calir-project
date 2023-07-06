# Cleaning up the acquired data

After initially running the script, we were left with 408 individual .json files that each contained a sample of reddit comments from one specific week. 
The files ranged from 20 kilobytes in 2013 to about 1mb in 2020 and after.

## Combining and cleaning up the data
We combined the file into one large file (supplied here as `all_comments.json`) and then ran the script `create_dataset.py`, which removes a lot of identifiable/unnecessary metadata from the comments, as well as doing some simple preprocessing by removing duplicate and empty comments.

## Identifying comment languages
We tried a lot of different approaches to identifying the language of comments. these attempts can be found in the script `language_identification.py` and `identify_language.py`. We've added a language tag to the comments in comment.json.