import os

import requests
import json
import time
import datetime
import logging

"""
NOTE: The Pushshift API was taken down some time in March of 2023, so this script does not work anymore. 
The dataset powering pushshift is still available as a torrent (https://academictorrents.com/details/7c0645c94321311bb05bd879ddee4d0eba08aaee)
"""



API_LINK = "https://api.pushshift.io/reddit/search/comment"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# the subreddit was created on 23-05-2013

"""
Parameters:
    subreddit: Name of subreddit, e.g.: "askreddit"
    before: Unix timestamp, e.g.: 1598918400
    after: Unix timestamp
    size: Number of submissions to return (max 500) default: 25
    sort: Sort by "asc" or "desc" default: "desc"
"""


# Get comments from the subreddit /r/buenzli from 2013-05-23 to 2023-01-01 in 1 week steps
def get_comments_range(subreddit, before, after, size=500):
    # Create URL
    url = API_LINK + "?subreddit=" + subreddit + "&before=" + str(before) + "&after=" + str(after) + "&size=" + str(
        size)
    logger.info(f"URL: {url}")
    # Get response
    response = requests.get(url)
    # Convert response to json
    try:
        response_json = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        logger.error(f"JSONDecodeError: {response.text}")
        return [], after + 7284000

    # Get submissions from response
    submissions = response_json.get("data", None)
    # If submissions is empty, return submissions
    if not submissions:
        logger.info(f"no submissions found between {after} and {before}")
        return []
    # dump submissions to file
    with open(f"json_{datetime.date.today().strftime('%d_%m_%y')}/{subreddit}/comments_{before}_{after}.json", "w") as file:
        json.dump(submissions, file)

    # Return submissions
    return submissions

def get_comments(subreddit, before, after, step, size=500):
    """
    Get comments from a specific subreddit withing a specific time frame. Iterates through time frame in steps of size step.
    :param subreddit: Name of subreddit, e.g.: "askreddit"
    :param before: Unix timestamp, e.g.: 1598918400
    :param after: Unix timestamp
    :param step: Step size in seconds
    :param size: Number of submissions to return (max 500) default: 500
    :return: List of comments
    """
    # create json directory if it does not exist
    date = datetime.date.today().strftime('%d_%m_%y')
    if not os.path.exists(f"json_{date}"):
        os.mkdir(f"json_{date}")
    # create subreddit directory if it does not exist
    if not os.path.exists(f"json_{date}/{subreddit}"):
        os.mkdir(f"json_{date}/{subreddit}")

    if before - after < step:
        logger.error(f"step size {step} is too large for time frame {before} - {after}")
        return []
    comments = []
    lower_bound = after
    upper_bound = after + step
    while upper_bound < before:
        comments += get_comments_range(subreddit, upper_bound, lower_bound, size)
        lower_bound = upper_bound
        upper_bound += step

def main():
    # get comments from subreddit /r/buenzli from 2013-05-23 to 2023-01-01 in 1 week
    # steps and save them to file
    comments = get_comments("schwiiz", 1672531200, 1369267200, 604800)
    # save comments to file
    with open("comments_full.json", "w") as file:
        json.dump(comments, file)




if __name__ == "__main__":
    main()
