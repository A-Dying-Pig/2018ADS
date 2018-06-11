#导入NearestNeighbor包 和 numpy
from sklearn.neighbors import NearestNeighbors
import numpy as np

result_read = []
in_data=[]
val = input('请输入要查询的图片维度信息')
val = val.split(',')
for index, item in enumerate(val):
    in_data.append(int(item))
result_read.append(in_data)

with open('colorhistogram(64).csv', 'r') as f:
    for line in f:
        linelist = line.split('\n')
        linelist = line.split(',')
        data = []
        for index, item in enumerate(linelist):
            data.append(int(item))
        result_read.append(data)

""" 
NearestNeighbors用到的参数解释 
n_neighbors=5,默认值为5，表示查询k个最近邻的数目 
algorithm='auto',指定用于计算最近邻的算法，auto表示试图采用最适合的算法计算最近邻 
fit(X)表示用X来训练算法 
"""
nbrs = NearestNeighbors(n_neighbors=3, algorithm="kd_tree").fit(result_read)
#返回距离每个点k个最近的点和距离指数，indices可以理解为表示点的下标，distances为距离
distances, indices = nbrs.kneighbors(result_read)
print(indices[0,1:])
print(distances[0,1:])

