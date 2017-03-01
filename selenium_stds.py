#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
import sys

from selenium import webdriver
from selenium import *

is_run = True


def show_all():
    global is_run

    def input_watching():
        global is_run
        while True:
            input_name = raw_input()
            print input_name
            if input_name == 'pause' or input_name == 'p':
                is_run = False
            if input_name == 'start' or input_name == 's':
                is_run = True
            if input_name == 'quit' or input_name == 'q':
                driver.close()
                driver.quit()
                sys.exit(0)

    t = threading.Thread(target=input_watching, args=())
    t.start()

    sleep_time = 5

    driver = webdriver.Chrome(r"C:\lgl\software\chromedriver_win32\chromedriver.exe")
    driver.get("http://192.168.20.111/")
    # driver.get("http://127.0.0.1:8000/")

    print "please input username"
    # input_name = raw_input()
    input_name = "sysadmin"
    driver.find_element_by_id("login-name").send_keys(input_name)
    time.sleep(2)
    print "please input password"
    # input_pwd = raw_input()
    input_pwd = "admin@1234"
    driver.find_element_by_id("login-pass").send_keys(input_pwd)
    time.sleep(sleep_time)

    driver.find_element_by_id("login-button").click()

    time.sleep(sleep_time)
    driver.find_element_by_class_name("sidebar-minify-btn").click()
    driver.find_element_by_id("full-screen").click()

    liList = driver.find_elements_by_xpath("//ul[@class='nav m-t-20 active']/li")

    def view():

        for n, li in enumerate(liList):
            while not is_run:
                time.sleep(1)
            # if n < 4:
            #     continue
            ll = li.find_elements_by_xpath("ul/li")
            li.click()
            time.sleep(sleep_time)
            if len(ll) > 0:
                for l in ll:
                    while not is_run:
                        time.sleep(1)
                    l.click()
                    time.sleep(sleep_time)

    for_times = 500
    for i in range(for_times):
        view()

    time.sleep(60)


if __name__ == '__main__':
    show_all()
