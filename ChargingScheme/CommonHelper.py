import Constants
import NetworkGeneration


# nodesNum：网络节点数量
# emergencyDegreeList：存放节点的紧急指标值
# sortedEmergencyNodeList：存放节点索引，按照紧急指标值降序排列
def sortByEmergency(nodesNum, emergencyDegreeList, sortedEmergencyNodeList):
    ls = emergencyDegreeList[1:]
    for i in range(1, nodesNum + 1):
        sortedEmergencyNodeList[i] = ls.index(max(ls)) + 1  # 已将BS的紧急指标设置为0，所以不会选到BS，其实BS已经在列表首位
        ls[sortedEmergencyNodeList[i] - 1] = -Constants.INF
    # sortedEmergencyNodeList[0]是BS，sortedEmergencyNodeList[1]是紧急指标排名第一的节点在node_list中的索引，以此类推


# 计算最短闭环距离，由于是NP难，所以采用近似解，即确定环时每次都取最近的节点(the nearest neighbor)作为下一个节点
# sortedEmergencyNodeList：已经按照充电紧急度降序排列的节点索引列表，第一个元素对应为BS，即0
# n：选取前n个非BS节点（充电紧急度最高的n个节点）
# path：MC充电路径
# tag：tag为False时，不更新path，tag为True时，更新path
def countCircle(distanceMatrix, sortedEmergencyNodeList, n, path, tag):
    circleL = 0
    pre = 0  # start from BS

    ls = sortedEmergencyNodeList[1:n + 1]
    for j in range(n - 1):
        mindex = ls[0]
        for i in ls:
            if distanceMatrix[pre][mindex] > distanceMatrix[pre][i]:
                mindex = i
        ls.remove(mindex)
        if tag:
            path.append(mindex)
        circleL += distanceMatrix[pre][mindex]
        pre = mindex
    if tag:
        path.append(ls[0])
    circleL += (distanceMatrix[pre][ls[0]] + distanceMatrix[ls[0]][0])
    # print("本次尝试路径长度： ", circleL)
    return circleL


# mcMaxMoveDistance：单轮充电中MC最大移动距离
def chooseAnchorAndChargePath(nodesNum, distanceMatrix, sortedEmergencyNodeList, mcMaxMoveDistance,
                              path):
    # clear path
    del path[:]
    path.append(0)
    left = 1
    right = nodesNum
    while True:
        # 防止mid与left与right三个相等时且circleL>mcMaxMoveDistance，程序之前会执行right=mid-1,那么这里left大于right成立
        # 但是circleL>mcMaxMoveDistance
        if left > right:
            mid = right
            break
        mid = (left + right) // 2
        circleL = countCircle(distanceMatrix, sortedEmergencyNodeList, mid, path, False)
        if circleL < mcMaxMoveDistance:
            left = mid + 1
        elif circleL == mcMaxMoveDistance:
            break
        else:
            right = mid - 1
    countCircle(distanceMatrix, sortedEmergencyNodeList, mid, path, True)


# 计算死亡节点占节点总数的比例
# residualEnergyList：存储节点的剩余能量
def ND(nodesNum, residualEnergyList):
    count = 0
    for i in range(1, nodesNum + 1):
        if residualEnergyList[i] == 0:
            count += 1
    return count / nodesNum


def updateND(nodesNum, nodeDeadTimeList, residualEnergyList, currentTime):
    if len(nodeDeadTimeList) == 0 and ND(nodesNum, residualEnergyList) >= 0:
        nodeDeadTimeList.append(currentTime)
    if len(nodeDeadTimeList) == 1 and ND(nodesNum, residualEnergyList) >= 0.3:
        nodeDeadTimeList.append(currentTime)
    if len(nodeDeadTimeList) == 2 and ND(nodesNum, residualEnergyList) >= 0.5:
        nodeDeadTimeList.append(currentTime)
    if len(nodeDeadTimeList) == 3 and ND(nodesNum, residualEnergyList) >= 0.7:
        nodeDeadTimeList.append(currentTime)


def test_chooseAnchorAndChargePath():
    nodesNum = 3
    emergencyDegreeList = [0, 1, -2, 5]
    sortedEmergencyNodeList = [0, 0, 0, 0]
    sortByEmergency(nodesNum, emergencyDegreeList, sortedEmergencyNodeList)
    print("节点充电紧急度列表")
    print(emergencyDegreeList)
    print("按照充电紧急度降序排列的节点列表")
    print(sortedEmergencyNodeList)

    nodeList = NetworkGeneration.initSensorNode(3)
    disMatrix = NetworkGeneration.getDistancematrix(nodeList)
    mcMaxMoveDistance = 150
    path = []
    chooseAnchorAndChargePath(nodesNum, disMatrix, sortedEmergencyNodeList, mcMaxMoveDistance,
                              path)
    print("节点物理距离矩阵")
    print(disMatrix)
    print("充电路径")
    print(path)


def test():
    test_chooseAnchorAndChargePath()


if __name__ == '__main__':
    test()
