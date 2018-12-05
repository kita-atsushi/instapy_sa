# coding: utf-8

import sys
import os
import time
import importlib
from tempfile import gettempdir

from selenium.common.exceptions import NoSuchElementException

sys.path.append(os.path.join(os.path.dirname(__file__), 'InstaPy'))
from instapy import InstaPy


importlib.reload(sys)


# Check environment value
try:
    insta_username = os.environ['ACCOUNT_USERNAME']
    insta_password = os.environ['ACCOUNT_PASSWORD']
    TAGLIST_FILEPATH = os.environ['INTERACT_FILEPATH']
    INTERACT_AMOUNT = int(os.environ['INTERACT_AMOUNT'])
    BLACKLIST_FILEPATH = os.environ['BLACKLIST_FILEPATH']
except KeyError:
    print("ERROR: No environment value.")
    sys.exit(1)

# Create Blacklist
blackwords = []
with open(BLACKLIST_FILEPATH, 'r', encoding="utf-8") as f:
    for line in f:
        b_word = line.rstrip()
        blackwords.append(b_word)

# Create target tag list
tag_list = []
with open(TAGLIST_FILEPATH, 'r', encoding="utf-8") as f:
    for line in f:
      b_tagname = line.rstrip()
      tag_list.append(b_tagname)

# Do instagram
session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True,
                  multi_logs=True)

try:
    session.login()

    session.set_relationship_bounds(
      enabled=True,
      potency_ratio=1.50,
      delimit_by_numbers=True,
      max_followers=15000,
      max_following=300,
      min_followers=100,
      min_following=0
    )
    session.set_delimit_liking(enabled=True, max=30000, min=0)
    session.set_dont_like(blackwords)

    session.like_by_tags(tag_list, amount=INTERACT_AMOUNT, skip_top_posts=True)

except Exception as exc:
    # if changes to IG layout, upload the file to help us locate the change
    if isinstance(exc, NoSuchElementException):
        file_path = os.path.join(gettempdir(), '{}.html'.format(time.strftime('%Y%m%d-%H%M%S')))
        with open(file_path, 'wb') as fp:
            fp.write(session.browser.page_source.encode('utf8'))
        print('{0}\nIf raising an issue, please also upload the file located at:\n{1}\n{0}'.format(
            '*' * 70, file_path))
    # full stacktrace when raising Github issue
    raise

finally:
    # end the bot session
    session.end()

