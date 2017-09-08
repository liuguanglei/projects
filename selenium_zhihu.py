#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
import sys
import traceback
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium import *


def main():
    options = webdriver.ChromeOptions()
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"')

    driver = webdriver.Chrome(r"C:\lgl\software\chromedriver_win32\chromedriver.exe", chrome_options=options)
    driver.get("https://www.zhihu.com/#signin")

    user_name = "18600958348"
    pwd = "lglcomcn"
    driver.find_element_by_xpath("//span[@class='signin-switch-password']").click()
    driver.find_element_by_xpath("//input[@name='account']").send_keys(user_name)
    driver.find_element_by_xpath("//input[@name='password']").send_keys(pwd)
    time.sleep(6)
    driver.find_element_by_xpath("//button[@class='sign-button submit']").click()
    # driver.get("https://www.zhihu.com/topic#滑雪")
    # driver.find_element_by_xpath("//a[@class='AppHeader-navItem'][2]").click()

    # for i in range(5):
    #     js = "window.scrollTo(0, document.body.scrollHeight)"
    #     driver.execute_script(js)
    #     time.sleep(3)

    time.sleep(3)
    doms = driver.find_elements_by_xpath("//div[@class='Card TopstoryItem']")
    for d in doms:
        try:
            # upButton = d.find_element_by_xpath(".//button[@class='Button VoteButton VoteButton--up']")
            # upButton.click()
            # time.sleep(5)
            upComment = d.find_element_by_xpath(".//button[@class='Button ContentItem-action Button--plain']")
            upComment.click()
            comment =u"哈哈,到此一游!"
            dom1 = d.find_element_by_xpath(".//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']")
            dom2 = d.find_element_by_xpath(".//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']/span")
            # action = ActionChains(driver).move_to_element(dom1).click(dom2).perform()
            actions = ActionChains(driver)
            actions.move_to_element(dom1)
            actions.click(dom2)
            actions.send_keys(comment)
            actions.perform()
            time.sleep(1)
            d.find_element_by_xpath(".//button[@class='Button CommentEditor-singleButton Button--primary Button--blue']").click()
            # time.sleep(2)
            # upComment.click()
            time.sleep(10)
        except Exception,e:
            print traceback.format_exc()
    i = 0

if __name__ == '__main__':
    main()
