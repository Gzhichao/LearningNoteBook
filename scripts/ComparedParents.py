#!/usr/bin/python3
import json
import sys
import os
import time
import urllib.request

Script = sys.argv[1] # 执行脚本路径
MinerID = sys.argv[2] # 节点号
DateTime = sys.argv[3] # 查询日期
LotteryNum = sys.argv[4] # 抽奖数量
WinNum = sys.argv[5] # 中奖数量

filename = f'{Script}/HashHeightParentsParentBlockHeight'
with open(filename,mode='r',encoding='utf-8') as rfp:
    content = rfp.readlines()
HeightParents = {}
for item in content:
    line = item.split('\t')
    HashHeightParents = line[0].split(' ')
    ParentBlockHeight = line[1]
    MinedHash = HashHeightParents[0].replace('"','').replace(',','')
    MinedHeight = HashHeightParents[1].replace(',','')
    MinedParents = HashHeightParents[2]
    url = f'https://api.filutils.com/api/v2/block/{MinedHash}'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    req = urllib.request.Request(url=url,headers=headers)
    while True:
        try:
            with urllib.request.urlopen(req) as response:
                content = json.load(response)
        except:
            print(f'{url}访问异常，请耐心等待片刻...')
            time.sleep(5)
            continue
        else:
            break
    data = content['data']
    if str(data) == 'None':
        HeightParents[MinedHeight] = [MinedParents,ParentBlockHeight]

OrphanNum = len(HeightParents) # 孤块数量
BlockNum = int(WinNum) - OrphanNum # 出块数量
print(f'{DateTime} {MinerID} 抽奖数量: {LotteryNum} 中奖数量: {WinNum} 出块数量: {BlockNum} 孤块数量: {OrphanNum}')
if HeightParents:
    for height,parents in HeightParents.items():
        parentsBlock = parents[0]
        parentsHeight = parents[1]
        url = f'https://api.filutils.com/api/v2/tipset/{parentsHeight}'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
        req = urllib.request.Request(url=url, headers=headers)
        while True:
            try:
                with urllib.request.urlopen(req) as response:
                    content = json.load(response)
            except:
                print(f'{url}访问异常，请耐心等待...')
                time.sleep(10)
                continue
            else:
                break
        onChain_parents_lst = []
        blocks_lst = content['data']['blocks']
        if str(blocks_lst) == 'None':
            print(f'请求{url}获取到的数据为{content},请检查')
            continue
        blocks_lst = content['data']['blocks']
        for item in blocks_lst:
            onChain_parents_lst.append(item['miner'])
        winning_parents_lst = list(eval(parentsBlock))
        pubParents = set(winning_parents_lst) & set(onChain_parents_lst)  # 交集
        lackParents = set(onChain_parents_lst) - set(winning_parents_lst)  # 差集(缺少)
        addParents = set(winning_parents_lst) - set(onChain_parents_lst)  # 差集(多了)
        print(f'WinningParents: {winning_parents_lst}')
        print(f'OnChainParents: {onChain_parents_lst}')
        if not pubParents:
            print(f'{MinerID} {height} 父区块同步错误(获取到的父区块高度: {parentsHeight})')
            continue
        if set(winning_parents_lst) == set(onChain_parents_lst):
            print(f'{MinerID} {height} 可能是爬取的页码不够，或是上链超时，或是lotus分叉所致，请检查确认')
        if lackParents:
            lackParents = str(lackParents).replace('\'', '').replace('{', '').replace('}', '')
            print(f'{MinerID} {height} 缺少了父区块{lackParents}')
        if addParents:
            addParents = str(addParents).replace('\'', '').replace('{', '').replace('}', '')
            print(f'{MinerID} {height} 多同步了父区块{addParents}')
