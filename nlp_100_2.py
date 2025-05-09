#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  9 08:46:07 2025
@author: yasukazu

第2章: UNIXコマンドの基礎

hightemp.txtは，日本の最高気温の記録を「都道府県」「地点」「℃」「日」のタブ区切り形式で格納したファイルである．以下の処理を行うプログラムを作成し，hightemp.txtを入力ファイルとして実行せよ．さらに，同様の処理をUNIXコマンドでも実行し，プログラムの実行結果を確認せよ．



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
import sys, os
from subprocess import run
from pathlib import Path

DATA_DIR = Path('DATA')
DATA_FILE = 'hightemp.txt'
DATA_FULLPATH = DATA_DIR / DATA_FILE

def run_cmd(cmd: str, cwd=DATA_DIR):
    """Execute a command in a terminal
    

    Parameters
    ----------
    cmd : str
        command line text

    Returns
    -------
    string
        stdout of the result of the executed command

    """
    return run(cmd, capture_output=True, shell=True, text=True, check=True, cwd=cwd).stdout

# 10. 行数のカウント
def count_lines(f: str, encoding='utf8'):
    '''Count lines.  Check with `wc`.
    '''
    pth = Path(f)
    n = 0
    with pth.open(encoding=encoding) as fi:
        while fi.readline():
            n += 1
    cmd_result = run_cmd(f"wc {f}")
    assert n == int(cmd_result.split()[0])
    return n
# 11. タブをスペースに置換
def conv_tab_to_spc(f: str, encoding='utf8'):
    '''タブ1文字につきスペース1文字に置換せよ．確認にはsedコマンド，trコマンド，もしくはexpandコマンドを用いよ．
    '''
    pth = Path(f)
    lines = []
    with pth.open(encoding=encoding) as fi:
        while (line:=fi.readline()):
            lines.append(line.replace('\t', ' ').strip())
    cmd_result = run_cmd(f"sed -e 's/\t/ /g' {f}")
    cmd_lines = [s.strip() for s in cmd_result.split('\n')]
    for n, line in enumerate(lines):
        assert line == cmd_lines[n]
    return lines

# 12.
def col_lines(input_=DATA_FULLPATH, outputs=('col1.txt', 'col2.txt'), encoding='utf8'):
    """Extract 1st and 2nd columns in every line
    
    Saves the first column and the second column of every line into files named 'col1.txt' and 'col2.txt', respectively.
    Uses `cut` command to check this function.
    
    Returns
    -------
    a list of output lines
     * Files with names in inputs where the same directory of inputs are also generated.
    """
    line_count = 0
    output_lines = ([],[])
    with input_.open(encoding=encoding) as inp:
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
        with output_fullpath_list[n].open('w', encoding=encoding) as out:
            out.write('\n'.join(output_lines[n]))
    # check output files
    output_lines = [output_fullpath_list[n].open(encoding=encoding).read().split('\n') for n in range(2)]
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

# 13.
def merge_files(input_=DATA_FULLPATH, inputs=('col1.txt', 'col2.txt'), output='col1-2.txt', encoding='utf8'):
    '''Merge `col1.txt` and `col2.txt` every line alternately spacing with a tab character:
        12で作ったcol1.txtとcol2.txtを結合し，元のファイルの1列目と2列目をタブ区切りで並べたテキストファイルを作成
    Check using `paste` command
    
    Returns
    -------
    None.
    '''
    def fullpath(f: str):
        return input_.parent / f
    input_lines = [[r.strip('\n') for r in fullpath(input).open(encoding=encoding).readlines()] for input in inputs]
    assert len(input_lines[0]) == len(input_lines[1])
    output_fullpath = fullpath(output)
    with output_fullpath.open('w', encoding=encoding) as wf:
        for c1, c2 in zip(*input_lines):
            print(f"{c1}\t{c2}", file=wf)
    cmd = f"paste {inputs[0]} {inputs[1]}"
    run_result = run_cmd(cmd)
    run_lines = [r for r in run_result.split('\n') if r.replace('\n', '')]
    rf_lines = [r.strip('\n') for r in output_fullpath.open(encoding=encoding).readlines() if r.replace('\n', '')]
    assert len(run_lines) == len(rf_lines)
    breakpoint()
    for n in range(len(run_lines)):
        assert run_lines[n] == rf_lines[n]

# 14. Output n lines from the head
def print_head(n: int, input_fullpath=DATA_FULLPATH, encoding='utf8', output=sys.stdout):
    '''Get a natural number N using command-line argument, then print heading N lines
        - Check with `head` command
        Parameters
        ----------
        n : int
            count of lines heading in the file
        Returns
        -------
        None.
    '''
    with input_fullpath.open(encoding=encoding) as fi:
        while n and (input_line:=fi.readline()):
            print(input_line, file=output, end='')
            n -= 1
from io import StringIO
def check_print_head(n: int):#, input_fullpath=DATA_FULLPATH, input_file=sys.stdin, encoding='utf8'):
    sio = StringIO()
    print_head(n, output=sio)
    cmd = f"head -n {n} {DATA_FILE}"
    cmd_result = run_cmd(cmd)
    sio.seek(0)
    cmd_lines = cmd_result.split('\n')
    for i in range(n):
        s_line = sio.readline().strip('\n')
        assert cmd_lines[i] == s_line
