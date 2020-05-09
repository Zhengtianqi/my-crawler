# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

num_list = [1.5, 0.6, 7.8, 6]
plt.bar(range(len(num_list)), num_list)
plt.show()

# matplotlib中有很多可用的模块，我们使用pyplot模块
from matplotlib import pyplot

month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
number = [20, 40, 60, 100, 12, 123, 13, 1, 12, 1, 3, 66]
# 生成图表
pyplot.plot(month, number)
# 设置横坐标为year，纵坐标为population，标题为Population year correspondence
pyplot.xlabel('month')
pyplot.ylabel('number')
pyplot.title('根据评论展示月销量')
# 设置纵坐标刻度
# pyplot.yticks([0, 25, 50, 75, 90])
# 设置填充选项：参数分别对应横坐标，纵坐标，纵坐标填充起始值，填充颜色（可以有更多选项）
# pyplot.fill_between(month, number, 10, color='green')
pyplot.fill_between(month, number)
# 显示图表
pyplot.show()
