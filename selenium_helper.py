#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver


def test():
    # driver = webdriver.Chrome(r"C:\lgl\software\chromedriver_win32\chromedriver.exe")
    driver = webdriver.Chrome(r"/Users/liuguanglei/Downloads/chromedriver")
    driver.get("http://www.so.com")
    # assert "360搜索".decode('utf-8') in driver.title

    driver.find_element_by_id("input").send_keys("python")
    driver.find_element_by_id("search-button").click()

    driver.get("http://www.baidu.com")
    # print driver.title
    # driver.close()
    time.sleep(100)


def jdLogin():
    # driver = webdriver.Chrome(r"C:\lgl\software\chromedriver_win32\chromedriver.exe")
    driver = webdriver.Chrome(r"/Users/liuguanglei/Downloads/chromedriver")
    # driver.set_window_size(200, 200)

    driver.get("https://passport.jd.com/new/login.aspx")
    driver.find_element_by_class_name("login-tab-r").click()
    print "please input username"
    # input_name = raw_input()
    input_name = "xxx"
    driver.find_element_by_id("loginname").send_keys(input_name)
    print "please input password"
    # input_pwd = raw_input()
    input_pwd = "xxx"
    driver.find_element_by_id("nloginpwd").send_keys(input_pwd)
    driver.find_element_by_id("loginsubmit").click()
    time.sleep(2)

    driver.get("https://miaosha.jd.com")
    time.sleep(2)

    driver.find_element_by_xpath(
        "//ul[@class='seckill_mod_goodslist clearfix']/li[1]/div[@class='seckill_mod_goods_info']/a").click()
    time.sleep(2)

    for handle in driver.window_handles:
        driver.switch_to_window(handle)
    try:
        driver.find_elements_by_id("InitCartUrl")[0].click()
        time.sleep(2)
    except:
        pass
    driver.get("https://cart.jd.com/cart.action")
    time.sleep(2)
    driver.find_elements_by_class_name("submit-btn")[0].click()

    time.sleep(2)
    driver.find_element_by_id("order-submit").click()

    time.sleep(100)


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
    # main()
    # test()
    jdLogin()
