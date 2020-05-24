#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time     : 2020/5/24
# @Author   : Peng
# @Desc

class Utils():

    def __init__(self):
        pass

    @staticmethod
    def Format_date(date_str):
        if "-" == date_str or "" == date_str:
            return '1970-01-01'

        arr = []
        arr = date_str.split("-")
        if 1 == len(arr):
            arr.append("01")
            arr.append("01")
        elif 2 == len(arr):
            arr.append("01")

        return "-".join(arr)