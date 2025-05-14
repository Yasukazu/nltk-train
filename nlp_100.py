#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  8 15:42:27 2025

@author: yasukazu
"""
import sys, os
import pandas as pd
from subprocess import run
from pathlib import Path


DATA_DIR = Path('DATA')
DATA_FILE = 'hightemp.txt'
DATA_FULLPATH = DATA_DIR / DATA_FILE

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

'''09. Typoglycemia
スペースで区切られた単語列に対して，各単語の先頭と末尾の文字は残し，それ以外の文字の順序をランダムに並び替えるプログラムを作成せよ．
ただし，長さが４以下の単語は並び替えないこととする．適当な英語の文（例えば
"I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
）を与え，その実行結果を確認せよ．
'''
import random
def rand_str(s: str):
    rr = []
    random.seed()
    ss = [c for c in s]
    while len(rr) < len(s):
        n = random.randrange(len(s))
        if (c:=ss[n]) != '\0':
            rr.append(c)
            ss[n] = '\0'
    return ''.join(rr)
def rand_splits(s: str):
    ss = s.split()
    out = []
    for s in ss:
        if len(s) <= 4:
            out.append(s)
        else:
            hd = s[0]
            tl = s[-1]
            md = s[1:-1]
            rnd_md = rand_str(md)
            out.append(hd + rnd_md + tl)
    return ' '.join(out)
