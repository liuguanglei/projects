#! usr/bin/python
# -*- coding:utf-8 -*-
import random
import copy
from datetime import datetime


def fun_execute_time(func):
    """A decorator that can print execution microseconds of a function"""

    def _fun_execute_time(*args, **kwargs):
        begin_time = datetime.now()
        re = func(*args, **kwargs)
        end_time = datetime.now()
        sub_time = (end_time - begin_time)
        sub_microseconds = sub_time.seconds * 1000000 + sub_time.microseconds
        print func.func_name + ' execute time is:' + str(sub_microseconds) + ' microseconds'
        return re

    return _fun_execute_time


class Sort:
    _number_array = None
    _result_array = None

    _total_compare_number = 0

    # _array_result = None

    def set_number_array(self, array):
        self._number_array = array

    @fun_execute_time
    def bubble_sort(self):
        self._result_array = copy.deepcopy(self._number_array)
        array = self._result_array
        last_pos = len(array)
        for index_i, i in enumerate(array):

            max = 0
            for index_j, j in enumerate(array):

                if index_j >= last_pos:
                    break

                if index_j + 1 >= len(array) - index_i:
                    break

                self._total_compare_number += 1
                k = array[index_j + 1]
                if j < k:
                    array[index_j] = k
                    array[index_j + 1] = j
                    max = index_j

            last_pos = max

    def reset(self):
        self._result_array = None
        self._total_compare_number = 0

    def bubble_sort_1(self):
        self._result_array = copy.deepcopy(self._number_array)
        r = self._result_array
        n = len(array)
        i = n - 1  # 初始时, 最后位置保持不变

        while i > 0:
            pos = 0  # 每趟开始时, 无记录交换
            for j, j_value in enumerate(array):

                if j >= i:
                    break

                self._total_compare_number += 1

                if r[j] < r[j + 1]:
                    pos = j  # 记录交换的位置
                    tmp = r[j]
                    r[j] = r[j + 1]
                    r[j + 1] = tmp

            i = pos  # 为下一趟排序作准备

    def quick_sort_inside(self, array):
        array = copy.deepcopy(array)
        base_ele = 0

        n = len(array)
        k = 0

        i = 0
        j = n - 1

        while k < n - 1:
            self._total_compare_number += 1

            if base_ele == i:

                if array[j] >= array[base_ele]:

                    j = j - 1
                else:
                    temp = array[j]
                    array[j] = array[base_ele]
                    array[base_ele] = temp
                    base_ele = j
                    i = i + 1

            elif base_ele == j:

                if array[i] <= array[base_ele]:

                    i = i + 1
                else:
                    temp = array[i]
                    array[i] = array[base_ele]
                    array[base_ele] = temp
                    base_ele = i
                    j = j - 1

            k = k + 1

        return (array, base_ele)

    def quick_sort(self,array):
        re = self.quick_sort_inside(array)
        re_array = re[0]

        re_n = len(re)[0]
        base_ele = re[1]

        if re_n > 2:
            self.quick_sort(array)
        else:
            return re_array


    def print_result(self):
        print '排序前数组: \r'
        re = ', '.join(str(i) for i in self._number_array)
        print re

        print '排序结果: \r'
        re = ', '.join(str(i) for i in self._result_array)
        print re

        print '总循环次数： %d' % (self._total_compare_number,)

    def gen_random_array(self, number):
        re = []
        for i in range(0, number):
            r = random.randint(0, number)
            re.append(r)
        return re


if __name__ == '__main__':
    array = Sort().gen_random_array(10)
    # array = [8, 3, 2, 9, 0, 8, 10, 9, 7, 2]
    sort = Sort()
    sort.set_number_array(array)
    # sort.bubble_sort()
    # sort.print_result()
    #
    # sort.reset()
    # sort.bubble_sort_1()
    # sort.print_result()

    sort.quick_sort()
    sort.print_result()
