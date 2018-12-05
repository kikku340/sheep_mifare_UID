#!/usr/bin/env python
# -*- coding: utf-8 -*-
# UID取得プログラム
from ctypes import *
import os
from glob import glob
import csv
import linecache
from datetime import datetime

defaultDLLpass = "./SheepSmartCard.dll"
logfilerlink = "./esddata"
target_place = [3, 5]
def read_UID(libpass=defaultDLLpass):
    # DLLファイルをロード
    dll = windll.LoadLibrary(libpass)
    # 返り値の型を指定
    dll.GetSmartCardUID.restypes = c_long
    # 引数の型を指定
    # dll.GetSmartCardUID.argtypes = [c_longlong()]
    # 参照渡しする変数の型を初期化
    UID = c_longlong()
    # UIDをDLLファイル経由で取得
    ret = dll.GetSmartCardUID(byref(UID))

    # 値は10進数で返るので文字列に変換する
    val = UID.value
    data = [0] * 8
    UID_str = ''
    if(ret != 0):
        print("読み取りエラー")
        return 0
    # エンディアン変換 + ASCIIコードに変換
    for i in range(8):
        data[i] = val & 0xff
        val >>= 8
        UID_str += chr(data[i])
    return str(UID_str)

def get_latestfile(dirname):
    target = os.path.join(dirname, '*')
    files = [(f, os.path.getmtime(f)) for f in glob(target)]
    latest_modified_file_path = sorted(files, key=lambda files: files[1])[-1]
    return latest_modified_file_path[0]

def get_result_latestESD(filename):
    with open(filename, 'r') as input:
        spamreader = csv.reader(input, delimiter=',', quotechar='|')
        data = list(spamreader)
        data_len = len(data)
        target = data[data_len - 1]
        # print("右足の測定値", target[target_place[0] + 1], "Ω", "左足の測定値", target[target_place[1] + 1], "[Ω]")
        print(target)
        if (target[target_place[0]] == "OK" and target[target_place[1]] == "OK"):
            return 0
    return -1

if __name__ == "__main__":
    # UID = read_UID()
    # res = get_result_latestESD()
    while (1):
        UID = read_UID()
        if (UID != 0):
            time = datetime.now()
            break
        sleep(0.1)
    while (time > datetime.datetime.fromtimestamp(os.stat(get_latestfile(logfirelink)).st_mtime)):
        continue
    res = get_result_latestESD(get_latestfile(logfirelink))
    if (res == 0):
        print("success!!!")
    else:
        print("failed...")
