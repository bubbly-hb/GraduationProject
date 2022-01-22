from Constants import Constants
import NetworkGeneration
import numpy as np


# nodesNum：网络节点数量
# distanceMatrix：节点间物理距离矩阵
# topuCostMatrix：拓扑代价矩阵
# residualEnergyList：存储节点的剩余能量
# nodeStatus：标识节点存活状态
# numOfChildNodesList：节点的孩子节点数量列表，numOfChildNodesList[i]表示节点i的下游节点数量
def updateTopuCostMatrix(nodesNum, distanceMatrix, topuCostMatrix, residualEnergyList, nodeStatus,
                         numOfChildNodesList):
    aerf = Constants.AERF
    beta = Constants.BETA
    gama = Constants.GAMA
    for i in range(nodesNum + 1):
        for j in range(nodesNum + 1):
            if nodeStatus[i] == -1 or nodeStatus[j] == -1:
                topuCostMatrix[i][j] = Constants.INF
                topuCostMatrix[j][i] = Constants.INF
                continue
            if distanceMatrix[i][j] > Constants.MAX_COMMUNICATE_RANGE:
                topuCostMatrix[i][j] = Constants.INF  # forwarding cost value will be infinite
            else:
                topuCostMatrix[i][j] = aerf * (1 - residualEnergyList[j] / Constants.NODE_FULL_ENERGY)\
                                       + beta * (distanceMatrix[i][j] / Constants.MAX_COMMUNICATE_RANGE)\
                                       + gama * numOfChildNodesList[j] / 10


# 给定拓扑代价矩阵，求source到target的最小代价值
# tag为True时，进行infoTransRateMatrix与numOfChildNodesList的更新，tag为False时，不进行相关更新，只是计算最小代价值
# infoGeneRateList：节点信息产生速率列表
# topuCostMatrix：拓扑代价矩阵
# infoTransRateMatrix：信息传输速率矩阵，infoTransRateMatrix[i][j]表示节点i向节点j信息传输速率
# topuMatrix：拓扑关系矩阵，topuMatrix[i][j]的值是一个列表，里面存储节点索引，这些节点是节点i的孩子节点，并且通过i->j路径由i转发给j
# numOfChildNodesList：节点的孩子节点数量列表，numOfChildNodesList[i]表示节点i的下游节点数量
# nodesNum：网络节点数量
def dijkstra(infoGeneRateList, topuCostMatrix, infoTransRateMatrix, topuMatrix,
             numOfChildNodesList, nodesNum, source, target, tag):

    visit = [0 for i in range(nodesNum + 1)]  # 标记节点是否被访问过
    visit[source] = 1
    costToi = [0 for i in range(nodesNum + 1)]
    pre = [0 for i in range(nodesNum + 1)]
    for i in range(nodesNum + 1):
        costToi[i] = topuCostMatrix[source][i]
        pre[i] = source
    for k in range(nodesNum):
        minNodeIndex = 1
        minCost = Constants.INF
        for i in range(nodesNum + 1):
            if costToi[i] < minCost and visit[i] == 0:
                minNodeIndex = i
                minCost = costToi[i]
        visit[minNodeIndex] = 1
        for j in range(nodesNum + 1):
            if visit[j] == 0 and costToi[
                    j] > costToi[minNodeIndex] + topuCostMatrix[minNodeIndex][j]:
                costToi[j] = costToi[minNodeIndex] + topuCostMatrix[minNodeIndex][j]
                pre[j] = minNodeIndex

    if tag and costToi[target] < Constants.INF:
        preN = pre[target]
        laterN = target
        while preN != source:
            numOfChildNodesList[preN] += 1  # 对应论文中"The w of each node on the path plus one"
            infoTransRateMatrix[preN][laterN] += infoGeneRateList[source]  # 更新数据传输矩阵
            topuMatrix[preN][laterN].append(source)  # 记录topuMatrix[preN][laterN]里包含source
            laterN = preN
            preN = pre[preN]
        infoTransRateMatrix[preN][laterN] += infoGeneRateList[source]  # 此时preN == source
        topuMatrix[preN][laterN].append(source)
    return costToi[target]


def buildTopu(nodesNum, distanceMatrix, topuCostMatrix, residualEnergy, nodeStatus,
              numOfChildNodesList, infoTransRateMatrix, topuMatrix, infoGeneRateList):
    for i in range(nodesNum + 1):
        numOfChildNodesList[i] = 0
        for j in range(nodesNum + 1):
            infoTransRateMatrix[i][j] = 0
            del topuMatrix[i][j][:]
    for i in range(1, nodesNum + 1):
        updateTopuCostMatrix(nodesNum, distanceMatrix, topuCostMatrix, residualEnergy, nodeStatus,
                             numOfChildNodesList)
        dijkstra(infoGeneRateList, topuCostMatrix, infoTransRateMatrix, topuMatrix,
                 numOfChildNodesList, nodesNum, i, 0, True)


def test():
    map_dic = NetworkGeneration.initMapDic(Constants.NUM_OF_NETWORKS, Constants.NUM_OF_NODES,
                                           Constants.MAX_COMMUNICATE_RANGE)
    info_generation_rate_dic = NetworkGeneration.initNodeInformationGenerationRateDic(
        Constants.NUM_OF_NETWORKS, Constants.NUM_OF_NODES, Constants.MIN_INFO_GENERATE_RATE,
        Constants.MAX_INFO_GENERATE_RATE)
    node_coordinate_ls = map_dic[0]
    distanceMatrix = NetworkGeneration.getDistancematrix(node_coordinate_ls)
    info_generation_rate_ls = info_generation_rate_dic[0]
    print("节点坐标列表")
    print(node_coordinate_ls)
    print("节点信息产生速率列表")
    print(info_generation_rate_ls)
    N = Constants.NUM_OF_NODES
    topuCostMatrix = np.ones((N + 1, N + 1))  # 构造网络拓扑结构时每条通信边的传输代价矩阵
    infoTransRateMatrix = np.zeros((N + 1, N + 1))  # 存放节点到另一节点的信息传输大小，用于计算节点的能量消耗中的信息接收与传输部分
    topuMatrix = [[[] * 1 for _ in range(N + 1)] for _ in range(N + 1)]
    numOfChildNodesList = [0 for i in range(N + 1)]  # 存放每个节点的子节点数，在更新两节点间传输代价时会用到,初值设为0
    nodeStatus = [1 for i in range(N + 1)]  # 节点死亡标记为-1，未死亡标记为1
    residualEnergy = [Constants.NODE_FULL_ENERGY for i in range(N + 1)]  # 节点剩余能量

    buildTopu(N, distanceMatrix, topuCostMatrix, residualEnergy, nodeStatus, numOfChildNodesList,
              infoTransRateMatrix, topuMatrix, info_generation_rate_ls)

    print("节点物理距离矩阵")
    print(distanceMatrix)
    print("节点topu代价矩阵")
    print(topuCostMatrix)
    print("信息传输速率矩阵，infoTransRateMatrix[i][j]表示节点i向节点j信息传输速率")
    print(infoTransRateMatrix)
    print("拓扑关系矩阵，topuMatrix[i][j]的值是一个列表，里面存储节点索引，这些节点是节点i的孩子节点，并且通过i->j路径由i转发给j")
    print(topuMatrix)


if __name__ == '__main__':
    test()
