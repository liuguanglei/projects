#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver


def test():
    driver = webdriver.Chrome(r"C:\lgl\software\chromedriver_win32\chromedriver.exe")
    driver.get("http://www.so.com")
    # assert "360搜索".decode('utf-8') in driver.title

    driver.find_element_by_id("input").send_keys("python")
    driver.find_element_by_id("search-button").click()

    # print driver.title
    # driver.close()


import thread
import time

global message
global is_stop
message = "hello world"
is_stop = True


def print_fun():
    while True:
        global message
        message = "hello world"
        print message
        # time.sleep(1)


def input_fun():
    global is_stop
    while is_stop:
        input = raw_input()
        if input == "stop":
            is_stop = False
        else:
            print input

        time.sleep(1)


def main():
    thread.start_new_thread(print_fun, ())
    thread.start_new_thread(input_fun, ())


if __name__ == '__main__':
    main()
