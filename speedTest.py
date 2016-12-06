from __future__ import division
import time
import random

data = []
data_length = 100000    # 总数据量
ma_length = 500         # 移动均线的窗口
test_times = 10         # 测试次数

for i in range(data_length):
    data.append(random.randint(1, 100))


def ma_basic(data, ma_length):

    # 用于保存均线输出结果的列表
    ma = []

    # 计算均线用的数据窗口
    data_window = data[:ma_length]

    # 测试用数据（去除了之前初始化用的部分）
    test_data = data[ma_length:]

    # 模拟实盘不断收到新数据推送的情景，遍历历史数据计算均线
    for new_tick in test_data:
        # 移除最老的数据点并增加最新的数据点
        data_window.pop(0)
        data_window.append(new_tick)

        # 遍历求均线
        sum_tick = 0
        for tick in data_window:
            sum_tick += tick
        ma.append(sum_tick/ma_length)

    # 返回数据
    return ma

import numpy as np

def ma_numpy_wrong(data, ma_length):
    ma = []
    data_window = data[:ma_length]
    test_data = data[ma_length:]

    for new_tick in test_data:
        data_window.pop(0)
        data_window.append(new_tick)

        # 使用numpy求均线，注意这里本质上每次循环
        # 都在创建一个新的numpy数组对象，开销很大
        data_array = np.array(data_window)
        ma.append(data_array.mean())

    return ma


# numpy的正确用法
def ma_numpy_right(data, ma_length):
    ma = []

    # 用numpy数组来缓存计算窗口内的数据
    data_window = np.array(data[:ma_length])

    test_data = data[ma_length:]

    for new_tick in test_data:
        # 使用numpy数组的底层数据偏移来实现数据更新
        data_window[0:ma_length-1] = data_window[1:ma_length]
        data_window[-1] = new_tick
        ma.append(data_window.mean())

    return ma

import numba
@numba.jit
def ma_numba(data, ma_length):
	ma = []
	data_window = data[:ma_length]
	test_data = data[ma_length:]

	for new_tick in test_data:
		data_window.pop(0)
		data_window.append(new_tick)
		sum_tick = 0
		for tick in data_window:
			sum_tick += tick
		ma.append(sum_tick/ma_length)

	return ma




# 将均线计算改写为高速算法
@numba.jit
def ma_online(data, ma_length):
    ma = []
    data_window = data[:ma_length]
    test_data = data[ma_length:]

    # 缓存的窗口内数据求和结果
    sum_buffer = 0

    for new_tick in test_data:
        old_tick = data_window.pop(0)
        data_window.append(new_tick)

        # 如果缓存结果为空，则先通过遍历求第一次结果
        if not sum_buffer:
            sum_tick = 0
            for tick in data_window:
                sum_tick += tick
            ma.append(sum_tick/ma_length)

            # 将求和结果缓存下来
            sum_buffer = sum_tick
        else:
            # 这里的算法将计算复杂度从O(n)降低到了O(1)
            sum_buffer = sum_buffer - old_tick + new_tick
            ma.append(sum_buffer/ma_length)

    return ma


# 基础的cython加速
# cython和高速算法
import helloworld


# 运行测试
start = time.time()

for i in range(test_times):
    result = ma_numba(data, ma_length)

time_per_test = (time.time()-start)/test_times
time_per_point = time_per_test/(data_length - ma_length)

print (u'单次耗时：%s秒' %time_per_test)
print (u'单个数据点耗时：%s微秒' %(time_per_point*1000000))
print (u'最后10个移动平均值：', result[-10:])