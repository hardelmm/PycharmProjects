# -*- coding: utf-8 -*-
# @Time    : 2023/2/27 11:12
# @Author  : huangyl
# @FileName: Sorting.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com

'''
list = [4, 5, 8, 3, 5, 6, 1, 2, 9, 7, 0]

for i in range(len(list)):
    j = i + 1
    for j in range(len(list)):
        if list[i] < list[j]:
            tmp = list[i]
            list[i] = list[j]
            list[j] = tmp
        #print("i = " + str(i) + "----- j = " + str(j))

print(list)
'''

n = [1, 2, 3, 4]
s = ['one', 'two', 'three']
r = zip(n, s)
print(set(r))