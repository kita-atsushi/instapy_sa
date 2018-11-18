# coding: utf-8
import sys
from lib.login import login
import time


args = sys.argv
if len(args) != 3:
    print("Usage: %s <username> <password>" % (args[0]))
    sys.exit(0)

args = sys.argv
username = args[1]
password = args[2]


def get_react(browser):
    ACTION_BOTTON = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/a'
    browser.find_element_by_xpath(ACTION_BOTTON).click()
    time.sleep(3)

    # Got action list
    action_user_list = browser.find_elements_by_xpath("//*[@class='nCY9N']/div/div")
    ele = action_user_list[0]

    for i in range(1, len(action_user_list)):
        liked = False
        comment = False
        follow = False

        ACT_EVENT_ELE = ele.find_element_by_xpath('//div[' + str(i) + ']' + '/div[2]/a[@class="FPmhX notranslate yrJyr"]')
        ACT_KIND_ELE = ele.find_element_by_xpath('//div[' + str(i) + ']' + '/div[2]')
        ACT_TIME_ELE = ele.find_element_by_xpath('//div[' + str(i) + ']' + '/div[2]/time')

        action_user_name = ACT_EVENT_ELE.text

        activity_kind = str(ACT_KIND_ELE.text.encode('utf-8'))
        if activity_kind.find('いいね') or activity_kind.find('like'):
            liked = True
        elif activity_kind.find('コメント') or activity_kind.find('comment'):
            comment = True
        elif activity_kind.find('フォロー') or activity_kind.find('follow'):
            follow = True

        activity_time = ACT_TIME_ELE.get_attribute('datetime')

        print('React: username={0} liked={1} follow={2} comment={3} react_timestamp={4}'.format(action_user_name, liked, follow, comment, activity_time))

# Main
browser = login(username, password)
get_react(browser)
