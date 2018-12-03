#!/usr/bin/env python
# -*- coding: utf-8 -*-
# UID取得プログラム
from ctypes import *
defaulrDLLpass = "./SheepSmartCard.dll"
def read_UID(libpass=defaulrDLLpass):
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
        return -1
    # エンディアン変換 + ASCIIコードに変換
    for i in range(8):
        data[i] = val & 0xff
        val >>= 8
        UID_str += chr(data[i])
    return str(UID_str)

if __name__ == "__main__":
    UID = read_UID()
    print("UID:", UID)
