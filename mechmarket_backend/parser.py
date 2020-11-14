#! usr/bin/env python3
import praw
import re
from configparser import ConfigParser


# Configuration
personal_key = "fN7PYFUt5Wmicg"
secret_key = "WWzdzOK4afXXgEMcQ7F32VeKzHFsLg"
app_name = "mechmarket parser"

# Reddit and Subreddit instances
reddit = praw.Reddit(client_id=personal_key, \
                     client_secret=secret_key, \
                     user_agent=app_name)

mechmarket = reddit.subreddit("mechmarket")
submissions = mechmarket.new(limit=50)
posts = []

# Compiled regular expressions
buy_or_sell_re = re.compile(r"\[(.*?)\].*?\[(.*?)\](.*)\[(.*?)\](.*)")
first_tag_re = re.compile(r"\[(.*?)\](.*)")

# Methods
def parse_buy_sell_information(post, re_match):
    post["region"] = re_match.group(1)
    if re_match.group(2) == "H":
        post["have"] = re_match.group(3).strip()
        post["want"] = re_match.group(5).strip()
        post["tag"] = "buying"
    else:
        post["want"] = re_match.group(3).strip()
        post["have"] = re_match.group(5).strip()
        post["tag"] = "selling"

def post_title_conform(post):
    if buy_or_sell_re.match(post.title):
        return True
    elif first_tag_re.match(post.title):
        re_match = first_tag_re.match(post.title)
        if first_tag_re.match(re_match.group(1)):
            return False
        else:
            return True
    return False

# Main parser
for submission in submissions:
    if post_title_conform(submission):
        post = {}
        post["post_name"] = submission.title
        post["post_id"] = submission.id
        post["selftext"] = submission.selftext
        post["score"] = submission.score
        post["date"] = submission.created_utc
        post["url"] = submission.url
        re_match = buy_or_sell_re.match(submission.title)
        if re_match:
            parse_buy_sell_information(post, re_match)
        else:
            post["tag"] = first_tag_re.match(submission.title).group(1)
        print(post)
        posts.append(post)


