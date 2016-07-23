#! usr/bin/python
# -*- coding:utf-8 -*-

from time import time
import datetime as datetime_ori
from datetime import datetime
import math


class CalculateScheduling:
    """"""

    SCHEDULING_DAYTIME = 0
    SCHEDULING_NIGHTTIME = 1
    SCHEDULING_GET_OFF_WORK = 2
    SCHEDULING_REST = 3

    _standard_status = None
    _standard_day = None
    _dest_day = None

    def __init__(self):
        self._standard_day = datetime.now().strftime('%Y%m%d')
        self._standard_status = self.SCHEDULING_DAYTIME
        self._dest_day = datetime.now().strftime('%Y%m%d')

    def set_standard(self, day, status):
        self._standard_day = day
        self._standard_status = status

        weekday = datetime.strptime(self._standard_day, '%Y%m%d').weekday()
        print '基准日期: %s     %s     状态: %s \n' % (
            self._standard_day, self.get_weekday_comment(weekday), self.get_result_comment(status))

    def set_dest_day(self, day):
        self._dest_day = day

    def calculate(self):
        day_dest = datetime.strptime(self._dest_day, '%Y%m%d')
        standard_day = datetime.strptime(self._standard_day, '%Y%m%d')
        sub = (day_dest - standard_day).days
        dest = (self._standard_status + sub) % 4
        # if dest > 4:
        #     dest = dest % 4
        return dest

    def get_result_comment(self, status):
        return {
            self.SCHEDULING_DAYTIME: '白班',
            self.SCHEDULING_NIGHTTIME: '夜班',
            self.SCHEDULING_GET_OFF_WORK: '下夜班 *',
            self.SCHEDULING_REST: '休息   *'
        }[status]

    def print_result(self):
        re = self.calculate()
        weekday = datetime.strptime(self._dest_day, '%Y%m%d').weekday()
        print '计算日期: %s     %s     状态: %s' % (
            self._dest_day, self.get_weekday_comment(weekday), self.get_result_comment(re))

    def set_year_month(self, year, month):
        begin_day = datetime.strptime(year + month, '%Y%m')
        end_day = datetime.strptime(year + str(int(month) + 1), '%Y%m')

        sub = (end_day - begin_day).days
        for i in range(1, sub + 1):
            day_str = str(i)
            if i < 10:
                day_str = '0' + str(i)
            self.set_dest_day(year + month + day_str)
            self.print_result()

    def get_weekday_comment(self, weekday):
        return {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六 *',
            6: '星期日 *',
        }[weekday].ljust(15)

    def set_year(self, year):
        begin_day = datetime.strptime(year, '%Y')
        end_day = datetime.strptime(str(int(year) + 1), '%Y')
        sub = (end_day - begin_day).days

        temp_mon = 0
        for i in range(0, sub):
            day = begin_day + datetime_ori.timedelta(days=i)
            day_str = day.strftime('%Y%m%d')
            self.set_dest_day(day_str)

            if day.month != temp_mon:
                print '\n %s 月' % (day.month)
                temp_mon = day.month
            self.print_result()


if __name__ == '__main__':
    cs = CalculateScheduling()
    standard_day = '20160721'
    standard_status = CalculateScheduling.SCHEDULING_GET_OFF_WORK
    re = cs.set_standard(standard_day, standard_status)

    ################################day###############################
    # dest_day = '20160719'
    # cs.set_dest_day(dest_day)
    # cs.print_result()

    ################################month###############################
    # cs.set_year_month('2016', '07')

    ################################year###############################
    cs.set_year('2016')
