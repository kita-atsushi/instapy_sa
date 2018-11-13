# coding: utf-8
import os
import re
import time
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


args = sys.argv
target_account = args[1]
content_amount = 10
OPEN_URL = "https://www.instagram.com/%s" % (target_account)

def _print_relation_log(pics_id, mention_users):
    for mention_user in mention_users:
        try:
            print("id=%s user=%s mention=%s" % (pics_id, target_account, mention_user))
            sys.stdout.flush()
        except UnicodeEncodeError:
            pass

def _is_private():
    try:
        private_string = '//*[@id="react-root"]/section/main/div/div/article/div[1]/div/h2'
        private_msg = browser.find_element_by_xpath(private_string).text
        _print_relation_log("PRIVATE_ACCOUNT", ["PRIVATE_ACCOUNT"])
    except NoSuchElementException:
        return False

    return True


def _get_pics_id():
    ret_id = None
    # Expect: https://www.instagram.com/p/Bpb2IYol9CB/
    current_url = browser.current_url
    ret_id = current_url.split("/p/")[-1].strip("/")
    return ret_id

def _get_mention_users_by_web_element(users_list):
    comment_xpath = '/html/body/div[3]/div[1]/div[2]/div[1]/article/div[2]/div[1]/ul/li'
    comment_ele_list = browser.find_elements_by_xpath(comment_xpath)
    count = 1
    for comment_ele in comment_ele_list:
        if count >= 3:
            commenter = comment_ele.find_element_by_xpath('div[1]/div[1]/div[1]/h3/a').text
            if commenter == target_account:
                contents = comment_ele.find_element_by_xpath('div[1]/div[1]/div[1]/span').text
                mention_user = contents.split(' ')[0]
                if '@' in mention_user:
                    users_list.append(mention_user.lstrip('@'))
        count+=1

def _get_mention_users():
    ret_users = []
    RETRY_MAX = 5
    for i in range(RETRY_MAX):
        try:
            _get_mention_users_by_web_element(ret_users)
        except StaleElementReferenceException:
            # Browser is not still reload
            time.sleep(1)

    return ret_users

def _click_media_list():
    mediaList = None
    try:
        # No story account
        mediaSelector = '//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div[1]/div[1]/div[1]'
        mediaList = browser.find_element_by_xpath(mediaSelector)
    except NoSuchElementException:
        pass

    if mediaList is None:
        mediaSelector = '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div[1]/div[1]/div[1]'
        mediaList = browser.find_element_by_xpath(mediaSelector)

    mediaList.click()

    time.sleep(2)

def _next_bottun(index):
    if index == 1:
        next = '/html/body/div[3]/div[1]/div[1]/div[1]/div[1]/a[1]'
    else:
        next = '/html/body/div[3]/div[1]/div[1]/div[1]/div[1]/a[2]'

    next_bottun = browser.find_element_by_xpath(next)
    next_bottun.click()

    time.sleep(2)


### Main
options = ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1280,1024')
browser = webdriver.Chrome(
    desired_capabilities=options.to_capabilities()
)
time.sleep(1)
browser.get(OPEN_URL)
time.sleep(5)

if _is_private():
    browser.close()
    sys.exit(0)

_click_media_list()

for pics_index in range(1, content_amount):
    _next_bottun(pics_index)
    pics_id = _get_pics_id()
    mention_users = _get_mention_users()
    _print_relation_log(pics_id, mention_users)
    time.sleep(5)

browser.close()
