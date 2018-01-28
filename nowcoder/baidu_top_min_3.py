# -*- coding:utf-8 -*-

def answer_top(num, arr):
    top_1 = 0
    top_2 = 0
    top_3 = 0
    for a in arr:
        if a > top_1:
            top_3 = top_2
            top_2 = top_1
            top_1 = a
        elif a == top_1:
            continue
        elif a < top_1 and a > top_2:
            top_3 = top_2
            top_2 = a
        elif a == top_2:
            continue
        elif a < top_2 and a > top_3:
        	top_3 = a
        else:
            continue
    if top_3 >0:
        return top_3
    else:
        return -1

def answer_min(num, arr):
    min_1 = 1001
    min_2 = 1001
    min_3 = 1001
    for a in arr:
        if a < min_1:
            min_3 = min_2
            min_2 = min_1
            min_1 = a
        elif a == min_1:
            continue
        elif a > min_1 and a < min_2:
            min_3 = min_2
            min_2 = a
        elif a == min_2:
            continue
        elif a > min_2 and a < min_3:
        	min_3 = a
        else:
            continue
    if min_3 <1001:
        return min_3
    else:
        return -1

if __name__ == '__main__':
    num = 9
    arr = [10, 40, 50, 20, 70, 80, 30, 90, 60]
    # print answer_top(num, arr)
    print answer_min(num, arr)