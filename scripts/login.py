# coding: utf-8
import time
import random
import os
import sys
import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions


args = sys.argv
if len(args) != 3:
    print("Usage: %s <username> <password>" % (args[0]))
    sys.exit(0)

args = sys.argv
username = args[1]
password = args[2]

LOGINPATH = '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a'
USERNAMEPATH = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[1]/div[1]/div[1]/input'
PASSWORDPATH = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div[1]/div[1]/input'

def login(username, password):
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1280,1024')
    browser = webdriver.Chrome(desired_capabilities=options.to_capabilities())

    browser.get("https://www.instagram.com/")
    time.sleep(3)
    browser.find_element_by_xpath(LOGINPATH).click()
    time.sleep(3)

    usernameField = browser.find_element_by_xpath(USERNAMEPATH)
    usernameField.send_keys(username)
    passwordField = browser.find_element_by_xpath(PASSWORDPATH)
    passwordField.send_keys(password)
    passwordField.send_keys(Keys.RETURN)
    return browser

print("@@@ Login start with %s" % (username))
browser = login(username, password)
browser.close()
print("@@@ Done.")
