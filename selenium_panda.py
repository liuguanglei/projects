#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
import sys

from selenium import webdriver
from selenium import *


def main():
    # driver = webdriver.Safari()
    # driver = webdriver.Firefox(r'/Users/liuguanglei/Downloads/geckodriver')
    driver = webdriver.Chrome(r'/Users/liuguanglei/Downloads/chromedriver')
    driver.get("http://www.panda.tv/2009")
    # driver.get("http://www.baidu.com")
    time.sleep(2)

    driver.find_element_by_xpath("//div[@class='room-task room-task-not-login']").click()

    user_name = "xxx"
    pwd = "xxx"
    driver.find_element_by_xpath("//input[@class='ruc-input-name ruc-input-login-name']").send_keys(user_name)
    driver.find_element_by_xpath("//input[@class='ruc-input-login-passport']").send_keys(pwd)
    driver.find_element_by_xpath("//div[@class='ruc-form-item button-container login-button-container']").click()

    time.sleep(3)
    _num = 100
    _text = u"666666 z"
    for i in range(_num):
        driver.find_element_by_xpath("//textarea[@class='room-chat-texta']").send_keys(_text)
        driver.find_element_by_xpath("//div[@class='room-chat-send']").click()
        time.sleep(5)

    time.sleep(1000)


if __name__ == '__main__':
    main()
