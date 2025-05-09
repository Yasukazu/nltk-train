#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  9 08:46:07 2025
@author: yasukazu

第2章: UNIXコマンドの基礎

hightemp.txtは，日本の最高気温の記録を「都道府県」「地点」「℃」「日」のタブ区切り形式で格納したファイルである．以下の処理を行うプログラムを作成し，hightemp.txtを入力ファイルとして実行せよ．さらに，同様の処理をUNIXコマンドでも実行し，プログラムの実行結果を確認せよ．


13. col1.txtとcol2.txtをマージ
12で作ったcol1.txtとcol2.txtを結合し，元のファイルの1列目と2列目をタブ区切りで並べたテキストファイルを作成せよ．確認にはpasteコマンドを用いよ．

14. 先頭からN行を出力

自然数Nをコマンドライン引数などの手段で受け取り，入力のうち先頭のN行だけを表示せよ．確認にはheadコマンドを用いよ．

15. 末尾のN行を出力

自然数Nをコマンドライン引数などの手段で受け取り，入力のうち末尾のN行だけを表示せよ．確認にはtailコマンドを用いよ．

16. ファイルをN分割する

自然数Nをコマンドライン引数などの手段で受け取り，入力のファイルを行単位でN分割せよ．同様の処理をsplitコマンドで実現せよ．

17. １列目の文字列の異なり

1列目の文字列の種類（異なる文字列の集合）を求めよ．確認にはsort, uniqコマンドを用いよ．

18. 各行を3コラム目の数値の降順にソート

各行を3コラム目の数値の逆順で整列せよ（注意: 各行の内容は変更せずに並び替えよ）．確認にはsortコマンドを用いよ（この問題はコマンドで実行した時の結果と合わなくてもよい）．

19. 各行の1コラム目の文字列の出現頻度を求め，出現頻度の高い順に並べる

各行の1列目の文字列の出現頻度を求め，その高い順に並べて表示せよ．確認にはcut, uniq, sortコマンドを用いよ．

"""

from subprocess import run
from pathlib import Path

DATA_DIR = Path('DATA')
DATA_FULLPATH = DATA_DIR / 'hightemp.txt'

# 10. 行数のカウント
def count_lines(f: str):
    '''行数をカウントせよ．確認にはwcコマンドを用いよ．
    '''
    pth = Path(f)
    n = 0
    with pth.open() as fi:
        while fi.readline():
            n += 1
    data = run(f"wc {f}", capture_output=True, shell=True, text=True)
    assert n == int(data.stdout.split()[0])
    return n
# 11. タブをスペースに置換

def conv_tab_to_spc(f: str):
    '''タブ1文字につきスペース1文字に置換せよ．確認にはsedコマンド，trコマンド，もしくはexpandコマンドを用いよ．
    '''
    pth = Path(f)
    lines = []
    with pth.open() as fi:
        while (line:=fi.readline()):
            lines.append(line.replace('\t', ' ').strip())
    data = run(f"sed -e 's/\t/ /g' {f}", capture_output=True, shell=True, text=True)
    cmd_lines = [s.strip() for s in data.stdout.split('\n')]
    for n, line in enumerate(lines):
        assert line == cmd_lines[n]
    return lines

def run_cmd(cmd: str):
    return run(cmd, capture_output=True, shell=True, text=True).stdout

# 12. 1列目をcol1.txtに，2列目をcol2.txtに保存
# 各行の1列目だけを抜き出したものをcol1.txtに，2列目だけを抜き出したものをcol2.txtとしてファイルに保存せよ．
# 確認にはcutコマンドを用いよ．
def col_lines(input=DATA_FULLPATH, outputs=['col1.txt', 'col2.txt']):
    """
    Returns
    -------
    as files with names in inputs where the same directory of input
    """
    line_count = 0
    output_lines = ([],[])
    with input.open('r') as inp:
        while line:=inp.readline():
            line_count += 1
            cols = line.split()
            assert len(cols) > 1
            for n in range(2):
                output_lines[n].append(cols[n]) #print(cols[n], file=outs[n])
    # check outputs
    for n in range(2):
        assert len(output_lines[n]) == line_count
    output_fullpath_list = [input.parent / name for name in outputs]
    # write outputs to files
    for n in range(2):
        with output_fullpath_list[n].open('w') as out:
            out.write('\n'.join(output_lines[n]))
    # check output files
    output_lines = [output_fullpath_list[n].open().read().split('\n') for n in range(2)]
    for n in range(2):
        assert len(output_lines[n]) == line_count
    # check by a command
    cmd = "cut -d '\t' -f 1,2 " + str(input)
    cmd_result = run_cmd(cmd)
    assert cmd_result
    cmd_lines = cmd_result.split('\n')
    if cmd_lines[-1] == '':
        cmd_lines = cmd_lines[:-1]
    assert len(cmd_lines) == line_count
    for n in range(line_count):
        cmd_cols = cmd_lines[n].split()
        assert len(cmd_cols) == 2
        for i in range(2):
            assert cmd_cols[i] == output_lines[i][n]
    return output_lines
                
    
    
    
    '''13. col1.txtとcol2.txtをマージ: 12で作ったcol1.txtとcol2.txtを結合し，元のファイルの1列目と2列目をタブ区切りで並べたテキストファイルを作成せよ．確認にはpasteコマンドを用いよ．    '''
    
    