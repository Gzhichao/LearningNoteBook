#!/bin/bash
#与冒泡排序相比，直接选择排序的交换次数更少，所以速度会快些
#基本思想：
#将指定排序位置与其它数组元素分别对比，如果满足条件就交换元素值，注意这里区别冒泡排序，不是交换相邻元素，而是把满足条件的元素与指定的排序位置交换(如从最后一个元素开始排序) ，这样排序好的位置逐渐扩大，最后整个数组都成为已排序好的格式
abc=(63 4 24 1 3 15)    #定义一个数组
echo "原数组的排列顺序为${abc[*]}" 
length=${#abc[*]}    #定义原数组的长度，这里原数组的长度为6
for ((i=1;i<$length;i++))   #这里是定义比较的轮数，比较5次
do
  index=0    #表示从索引0开始比较
  last=$[$length-$i]    #获取在比较的范围中的最后一个元素的索引
  for ((k=1;k<=$length-i;k++))   #这里是确定用于比较的第一个元素的索引范围，比如已经定义了从索引0开始了，所以和0进行比较的范围就是从索引1-5了
  do
     first=${abc[$k]}   #定义与index相比较的索引的取值为first
     if [ $first -gt ${abc[$index]} ];then   #通过将index所在的索引的值与k所在的索引的值进行比较，获取最大元素的索引位置
        index=$k    #通过比较将较大的数定义到index中，进行下一轮的比较
     fi
     temp=${abc[$last]}   #将上一步获取到的最后一个元素的索引的值保存到临时变量temp中
     abc[$last]=${abc[$index]}  #把最大上面for循环比较出来的最大元素的值赋值给最后一个元素
     abc[$index]=$temp    #把原来最后一个元素的值赋给原来最大值的位置的元素
     echo "$i $k: ${abc[*]}"
  done
  echo "$i $k: ${abc[*]}"
done
echo "排序后数组的排列顺序为${abc[*]}"   #输出排序后的数组
