#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  8 15:42:27 2025

@author: yasukazu
"""

#07. テンプレートによる文生成
def zino(x: int, y: str, z: float):
    '''引数x, y, zを受け取り「x時のyはz」という文字列を返す
    x=12, y="気温", z=22.4
    '''
    return f"{x}時の{y}は{z}"
'''08. 暗号文

与えられた文字列の各文字を，以下の仕様で変換する関数cipherを実装せよ．

    英小文字ならば(219 - 文字コード)の文字に置換
    その他の文字はそのまま出力

この関数を用い，英語のメッセージを暗号化・復号化せよ．
'''
def ciconv(c: str):
    return chr(219 - ord(c[0])) if c[0].islower() else c[0]
def cipher(src: str):
    return ''.join([ciconv(c) for c in src])
