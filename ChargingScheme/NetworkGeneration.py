import itertools
import random
import numpy as np
import math
from Constants import Constants
from random import uniform


# 返回一个大小为n+1的列表，包含基站（0,0）以及随机生成的n个传感器节点坐标
def initSensorNode(n):
    list1 = list(itertools.product(range(-50, 0), range(-50, 51)))
    list2 = list(itertools.product(range(1, 51), range(-50, 51)))
    random_list = random.sample(list1 + list2, n)  # 随机化N个不为（0，0）的节点
    random_list.insert(0, (0, 0))

    return random_list


def countDistance(nodeCoordinatesList, x, y):
    pz = [
        nodeCoordinatesList[x][0] - nodeCoordinatesList[y][0],
        nodeCoordinatesList[x][1] - nodeCoordinatesList[y][1]
    ]
    return math.hypot(pz[0], pz[1])


# 返回一个二维矩阵（n+1,n+1），distanceMatrix[i][j]即为节点i到节点j的物理距离大小
def getDistancematrix(node_list):
    n = len(node_list)
    distanceMatrix = np.ones((n, n))  # 节点间物理距离矩阵

    for i in range(n):
        for j in range(n):
            distanceMatrix[i][j] = countDistance(node_list, i, j)

    return distanceMatrix


# 从BS开始深搜，即在最大通讯距离限制条件下将BS能到达的节点visit值设为1
def dfs(visit, distanceMatrix, maxCommunicateRange, x):
    visit[x] = 1
    n = len(distanceMatrix)
    for i in range(n):
        if i != x and visit[i] == 0 and distanceMatrix[x][i] <= maxCommunicateRange:
            dfs(visit, distanceMatrix, maxCommunicateRange, i)


# 检查生成的节点坐标是否有效，即每个节点是否能在最大通讯距离的限制条件下连接上基站（BS），可以用深搜
def checkMap(distanceMatrix, maxCommunicateRange):
    n = len(distanceMatrix)
    visit = [0 for i in range(n)]
    dfs(visit, distanceMatrix, maxCommunicateRange, 0)
    for i in range(n):
        if visit[i] == 0:
            return False
    return True


# 返回一个大小为N的字典，包含N组节点个数为n+1(加上BS)的网络坐标列表
def initMapDic(N, n, maxCommunicateRange):
    map_dic = {}
    for i in range(N):
        while 1:
            node_list = initSensorNode(n)
            distanceMatrix = getDistancematrix(node_list)
            if checkMap(distanceMatrix, maxCommunicateRange):
                map_dic[i] = node_list
                break
    return map_dic


# 返回一个大小为N的字典，包含N组节点个数为n+1(加上BS)的网络节点信息生成速率在指定范围[rMin, rMax]内的随机值
def initNodeInformationGenerationRateDic(N, n, rMin, rMax):
    temp_r_dic = {}
    for j in range(N):
        r = [uniform(rMin, rMax) for i in range(n + 1)]  # 节点数据产生率，单位：bps
        r[0] = 0
        temp_r_dic[j] = r
    return temp_r_dic


def test():
    map_dic = initMapDic(Constants.NUM_OF_NETWORKS, Constants.NUM_OF_NODES,
                         Constants.MAX_COMMUNICATE_RANGE)
    info_generation_rate_dic = initNodeInformationGenerationRateDic(
        Constants.NUM_OF_NETWORKS, Constants.NUM_OF_NODES, Constants.MIN_INFO_GENERATE_RATE,
        Constants.MAX_INFO_GENERATE_RATE)
    print(map_dic)
    print(info_generation_rate_dic)


if __name__ == '__main__':
    test()
