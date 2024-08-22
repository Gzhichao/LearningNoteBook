#!/bin/bash
#查看提交上链失败的消息
grep 'Submitting window post' /opt/raid0/lotusminer-window/lotusminer/logs |grep 'failed'|tail -n1|awk '{print $8}'
#查看最新提交上链的消息是否有失败的，如果发现有，时间上如果也来得及抽查，可以重启封装程序，目的是重新提交上链的消息
grep -A1 'Submitted window post' /opt/raid0/lotusminer-window/lotusminer/logs |tail -n1|grep 'failed'
#查看所有消息
lotus mpool pending --local | jq .
#Nonce
lotus mpool pending --local | jq -r .Message.Nonce
#GasFeeCap
lotus mpool pending --local | jq -r .Message.GasFeeCap
#GasPremium
lotus mpool pending --local | jq -r .Message.GasPremium
#GasLimit
lotus mpool pending --local | jq -r .Message.GasLimit
#cid
lotus mpool pending --local --cids
#Method
lotus mpool pending --local | jq -r .Message.Method
#默认情况消息GasFeeCap 大于 ParentBaseFee，如果小于就需要疏通消息
#自动疏通
#--fee-limit 愿意为消息支付的最高费用
lotus mpool replace --auto --fee-limit 0.3 <CID>
#手动疏通
#ParentBaseFee
lotus chain getblock $(lotus chain head | head -1) | jq -r .ParentBaseFee
lotus mpool replace --gas-feecap <参考ParentBaseFee> --gas-premium <原值0.25倍> --gas-limit <参考查看浏览器> <消息CID>
#批量疏通消息
lotus mpool pending --local --cids | wc -l
lotus mpool pending --local --cids | xargs -n 1 lotus mpool replace --auto --fee-limit 0.3
#指定消息的接收方和发送方的钱包地址
lotus mpool pending --local --cids --to f01538000 --from f3rb2as5lyjxu22szdtvorerilr5kkujgf2asnwdykgddachuj4fekgmv7q34ysbtyhirobtmebvipyan7lggq | xargs -n 1 lotus mpool replace --auto --fee-limit 0.3
