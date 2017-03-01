#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from selenium import webdriver
from selenium import *


def show_all():
    driver = webdriver.Chrome(r"C:\lgl\software\chromedriver_win32\chromedriver.exe")
    # driver.get("http://192.168.20.111/")
    driver.get("http://127.0.0.1:8000/")

    print "please input username"
    # input_name = raw_input()
    input_name = "sysadmin"
    driver.find_element_by_id("login-name").send_keys(input_name)
    time.sleep(2)
    print "please input password"
    # input_pwd = raw_input()
    input_pwd = "admin@1234"
    driver.find_element_by_id("login-pass").send_keys(input_pwd)
    time.sleep(3)

    driver.find_element_by_id("login-button").click()

    time.sleep(3)
    driver.find_element_by_class_name("sidebar-minify-btn").click()
    driver.find_element_by_id("full-screen").click()

    liList = driver.find_elements_by_xpath("//ul[@class='nav m-t-20 active']/li")

    def view():
        for n, li in enumerate(liList):
            if n < 4:
                continue
            ll = li.find_elements_by_xpath("ul/li")
            li.click()
            time.sleep(3)
            if len(ll) > 0:
                for l in ll:
                    l.click()
                    time.sleep(3)

    for i in range(5):
        view()

    time.sleep(60)


if __name__ == '__main__':
    show_all()
