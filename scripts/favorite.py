# coding: utf-8

import sys
import os
import time
import random
from tempfile import gettempdir

from selenium.common.exceptions import NoSuchElementException

sys.path.append(os.path.join(os.path.dirname(__file__), 'InstaPy'))
from instapy import InstaPy


# Check environment value
try:
    ACCOUNT_USERNAME = os.environ['ACCOUNT_USERNAME']
    ACCOUNT_PASSWORD = os.environ['ACCOUNT_PASSWORD']
    INTERACT_FILEPATH = os.environ['INTERACT_FILEPATH']
    BLACKLIST_FILEPATH = os.environ['BLACKLIST_FILEPATH']
    INTERACT_AMOUNT = int(os.environ['INTERACT_AMOUNT'])
    INTERACT_RATIO = int(os.environ['INTERACT_RATIO'])
except KeyError:
    print("ERROR: No environment value.")
    sys.exit(1)

# Create Blacklist
blacklist = []
with open(BLACKLIST_FILEPATH, 'r') as f:
    for line in f:
      b_username = line.rstrip()
      blacklist.append(b_username)

# Create target tag list
interact_list = []
with open(INTERACT_FILEPATH, 'r') as f:
    for line in f:
      f_tagname = line.rstrip()
      interact_list.append(f_tagname)
random.shuffle(interact_list)

# Do instagram
session = InstaPy(username=ACCOUNT_USERNAME,
                  password=ACCOUNT_PASSWORD,
                  headless_browser=True,
                  multi_logs=True)

try:
    session.login()

    session.set_relationship_bounds(enabled=False)
    session.set_ignore_users(blacklist)
    session.set_do_like(True, percentage=INTERACT_RATIO)

    session.interact_by_users(interact_list, amount=INTERACT_AMOUNT, randomize=False, media='Photo')

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
    sys.exit(0)
