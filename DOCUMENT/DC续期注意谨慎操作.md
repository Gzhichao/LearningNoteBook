#查询DC是不是2022年 11月 30 日 之后跑的
awk '$5 >= 2383920{print}' DC.txt   #备注：高度2383920对应的时间2022-12-01 00:00:00，是可以续期的
#查询DC是不是2022年 11月 30 日 之前跑的
awk '$5 < 2383920{print}' DC.txt #备注：在此高度之前的是不要续期的,否则十倍质押一倍算力！！！！！！！！！！！！！！！！！！！！！

#查看有效扇区的信息
lotus-miner sectors check-expire --cutoff=2880000000 > 1.txt
#查看过期的高度为4305400的有效扇区
awk '$11 == 4305400{print}' 1.txt
#查找满足两个高度之间的扇区信息
awk '$15 >= 3962160 && $15 < 4137840' /root/.guozhichao/ExportSector/f01656666/All/3998096/AllSectorInfo-41313
#查看有效扇区过期高度的扇区数量，$11是过期高度
awk 'NR>1{sum[$11]++}END{for(i in sum)print i,sum[i]}' 1.txt
#查询DataCap的剩余额度
lotus filplus check-client-datacap f01940441 |awk '{print $1/1024/1024/1024"GB"}'
#回收额度
lotus filplus remove-expired-allocations f1gk7n4ckn23ix2bu7q6qtas6eayambn57ass2zfq
#查看节点的LDN
lotus filplus list-claims f0503420
