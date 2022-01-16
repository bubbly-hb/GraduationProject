import numpy as np

import Constants
import NetworkGeneration
import NetworkTopuBuild
import EnergyConsumption
import CommonHelper


def updateEmergencyDegree(nodesNum, residualEnergyList, energyConsumeRateList, distanceMatrix,
                          emergencyDegreeList):
    # TlifeI[i] means the residual life time of the node i
    TlifeI = [0 for i in range(nodesNum + 1)]
    # neighborForNode[i] means the number of sensor nodes within one jump of node i
    neighborForNode = [0 for i in range(nodesNum + 1)]

    for i in range(1, nodesNum + 1):
        if residualEnergyList[i] == 0:
            TlifeI[i] = 0
        else:
            TlifeI[i] = residualEnergyList[i] / energyConsumeRateList[i]

        for j in range(1, nodesNum + 1):
            if distanceMatrix[i][j] <= Constants.MAX_COMMUNICATE_RANGE:
                neighborForNode[i] += 1
        neighborForNode[i] -= 1  # 由于把自身算做了自己的邻居，所以减1

    Tmax = max(TlifeI)
    neighborMax = max(neighborForNode)

    for i in range(1, nodesNum + 1):
        emergencyDegreeList[i] = 1 - TlifeI[i] / Tmax + neighborForNode[i] / (10 * neighborMax)


def chargeByREEC(nodesNum, mapDic, nodeInfoGenerationRateDic):
    AverageEnergy = []
    Rrate = []
    ChargeEfficiency = []
    acdistance = []
    for pos_round in range(Constants.NUM_OF_NETWORKS):
        mcChargingPath = [0]  # MCS充电路径，path[0]为BS，path[1]为第一个待充电的锚点
        topuCostMatrix = np.ones((nodesNum + 1, nodesNum + 1))  # 构造网络拓扑结构时每条通信边的传输代价矩阵

        numOfChildNodesList = [0 for i in range(nodesNum + 1)]  # 存放每个节点的子节点数，在更新两节点间传输代价时会用到,初值设为0

        infoGeneRateList = nodeInfoGenerationRateDic[pos_round]

        # 存放节点到另一节点的信息传输大小，用于计算节点的能量消耗中的信息接收与传输部分
        infoTransRateMatrix = np.zeros((nodesNum + 1, nodesNum + 1))

        energyConsumeRateList = [0 for i in range(nodesNum + 1)]  # 节点能量消耗率
        emergencyDegree = [i for i in range(nodesNum + 1, 0, -1)]  # 紧急指标
        residualEnergy = [Constants.NODE_FULL_ENERGY for i in range(nodesNum + 1)]  # 节点剩余能量

        sortedEmergencyNodeList = [1 for i in range(nodesNum + 1)]  # 已按紧急指标递减排序的节点序号
        sortedEmergencyNodeList[0] = 0  # BS在0号位置，sortedEmergencyNodeList[1]为紧急指标排名第一的节点序号
        emergencyDegree[0] = 0  # 不影响sortByEmergency()的正常运行
        topuMatrix = [[[] * 1 for _ in range(nodesNum + 1)] for _ in range(nodesNum + 1)]

        # to check
        sojournTime = 0

        SumR = 0  # 总的信息收集量

        # MCS进行充电的轮数，每一轮从BS出发，给所有锚点充电后返回BS
        nodeStatus = [1 for i in range(nodesNum + 1)]  # 节点死亡标记为-1，未死亡标记为1
        SumTime = 0

        ACTDistance = 0  # MC实际移动距离
        supplementEnergy = 0  # 输出给节点的总能量

        Round = Constants.ROUND

        nodeDeadTimeList = []

        random_list = mapDic[pos_round]

        distanceMatrix = NetworkGeneration.getDistancematrix(random_list)  # 节点间物理距离矩阵

        NetworkTopuBuild.buildTopu(nodesNum, distanceMatrix, topuCostMatrix, residualEnergy,
                                   nodeStatus, numOfChildNodesList, infoTransRateMatrix,
                                   topuMatrix, infoGeneRateList)

        EnergyConsumption.updateEnergyConsume(nodesNum, nodeStatus, topuMatrix, infoGeneRateList,
                                              energyConsumeRateList)

        for count in range(Round):
            mcChargingPath.clear()  # 每一轮都清空path
            mcChargingPath.append(0)

            updateEmergencyDegree(nodesNum, residualEnergy, energyConsumeRateList, distanceMatrix,
                                  emergencyDegree)
            CommonHelper.sortByEmergency(nodesNum, emergencyDegree, sortedEmergencyNodeList)
            CommonHelper.chooseAnchorAndChargePath(nodesNum, distanceMatrix,
                                                   sortedEmergencyNodeList,
                                                   Constants.MC_MAX_MOVE_DISTANCE, mcChargingPath)
            AnchorAmount = len(mcChargingPath) - 1  # 锚点个数

            mcChargingPath.append(0)

            # print('hhhhhb',path)
            # print('hhb',len(path))

            # print("AnchorAmount:",AnchorAmount)

            for k in range(0, AnchorAmount + 1):

                traverTime = distanceMatrix[mcChargingPath[k]][mcChargingPath[
                    k + 1]] / Constants.MC_SPEED
                ACTDistance += distanceMatrix[mcChargingPath[k]][mcChargingPath[k + 1]]

                SumTime += traverTime

                for i in range(1, nodesNum + 1):

                    if nodeStatus[i] == 1:
                        if residualEnergy[i] < energyConsumeRateList[i] * traverTime:
                            nodeStatus[i] = -1
                            SumR += infoGeneRateList[i] * residualEnergy[
                                i] / energyConsumeRateList[i]  # 在这一跳中忽略子节点信息丢失影响
                            residualEnergy[i] = 0
                            for q in range(1, nodesNum + 1):
                                for nd in topuMatrix[i][q]:
                                    nodeStatus[nd] = -1
                            EnergyConsumption.updateEnergyConsume(nodesNum, nodeStatus, topuMatrix,
                                                                  infoGeneRateList,
                                                                  energyConsumeRateList)
                        else:
                            residualEnergy[i] -= (energyConsumeRateList[i] +
                                                  Constants.PRICE) * traverTime
                            SumR += infoGeneRateList[i] * traverTime
                    elif residualEnergy[i] > 0:
                        if residualEnergy[i] < energyConsumeRateList[i] * traverTime:
                            residualEnergy[i] = 0
                            EnergyConsumption.updateEnergyConsume(nodesNum, nodeStatus, topuMatrix,
                                                                  infoGeneRateList,
                                                                  energyConsumeRateList)
                        else:
                            residualEnergy[i] -= (energyConsumeRateList[i] +
                                                  Constants.PRICE) * traverTime

                CommonHelper.updateND(nodesNum, nodeDeadTimeList, residualEnergy, SumTime)

                # print('MC从节点%d到节点%d信息产生量：%f'%(k,k+1,SumR))               #调试
                # print("各节点信息产生率：",r)                                     #调试

                if k != AnchorAmount:
                    sojournTime = (Constants.NODE_FULL_ENERGY -
                                   residualEnergy[mcChargingPath[k + 1]]) / Constants.CHARINGSPEED
                    supplementEnergy += Constants.NODE_FULL_ENERGY - residualEnergy[mcChargingPath[
                        k + 1]]

                    residualEnergy[mcChargingPath[
                        k + 1]] = Constants.NODE_FULL_ENERGY  # path[k+1]锚点电量被充满
                    nodeStatus[mcChargingPath[k + 1]] = 1
                    for q in range(1, nodesNum + 1):
                        for nd in topuMatrix[mcChargingPath[k + 1]][q]:
                            if residualEnergy[nd] > 0:
                                nodeStatus[nd] = 1
                    EnergyConsumption.updateEnergyConsume(nodesNum, nodeStatus, topuMatrix,
                                                          infoGeneRateList, energyConsumeRateList)

                    for i in range(1, nodesNum + 1):
                        if nodeStatus[i] == 1:
                            if residualEnergy[i] < energyConsumeRateList[i] * sojournTime:
                                nodeStatus[i] = -1
                                SumR += infoGeneRateList[i] * residualEnergy[
                                    i] / energyConsumeRateList[i]  # 在这一跳中忽略子节点信息丢失影响，后面会重新更新拓扑
                                residualEnergy[i] = 0
                                for q in range(1, nodesNum + 1):
                                    for nd in topuMatrix[i][q]:
                                        nodeStatus[nd] = -1
                                EnergyConsumption.updateEnergyConsume(
                                    nodesNum, nodeStatus, topuMatrix, infoGeneRateList,
                                    energyConsumeRateList)
                            else:
                                residualEnergy[i] -= (energyConsumeRateList[i] +
                                                      Constants.PRICE) * sojournTime
                                SumR += infoGeneRateList[i] * sojournTime
                        elif residualEnergy[i] > 0:
                            if residualEnergy[i] < energyConsumeRateList[i] * sojournTime:
                                residualEnergy[i] = 0
                                EnergyConsumption.updateEnergyConsume(
                                    nodesNum, nodeStatus, topuMatrix, infoGeneRateList,
                                    energyConsumeRateList)
                            else:
                                residualEnergy[i] -= (energyConsumeRateList[i] +
                                                      Constants.PRICE) * sojournTime

                    residualEnergy[mcChargingPath[
                        k + 1]] = Constants.NODE_FULL_ENERGY  # path[k+1]锚点电量被充满
                    SumTime += sojournTime

                    CommonHelper.updateND(nodesNum, nodeDeadTimeList, residualEnergy, SumTime)

                    # print('MC停留在节点%d处信息产生量：%f'%(k+1,SumR))
                    # print("各节点信息产生率：", r)                      # 调试

            # print('前', count+1, '轮', '信息产生量：', SumR)
            # print(SumTime)
            # print(EnergyConsume)
            # print(residualEnergy)

            if (count + 1) == Round:
                SumofRestEnergy = 0
                for i in range(1, nodesNum + 1):
                    # print('节点',i,'的剩余能量：',residualEnergy[i])
                    SumofRestEnergy += residualEnergy[i]
                print('第', count + 1, '轮', "网络节点平均能量:", SumofRestEnergy / nodesNum, "  时刻: ",
                      SumTime)

                AverageEnergy.append(SumofRestEnergy / nodesNum)

        # print('总信息产生量：', SumR)
        # print("总共耗时：", SumTime)
        # print("MC移动距离：", ACTDistance)
        # print("网络信息产生速率（信息产生总量/总耗时）：", SumR / SumTime)
        # print("MC为锚点补充能量：", supplementEnergy)
        # print("MC充电效率", supplementEnergy / ACTDistance)
        # print("网络能量消耗速率（总耗能/总耗时）",(B*N-SumofRestEnergy)/SumTime)

        Rrate.append(SumR / SumTime)
        ChargeEfficiency.append(supplementEnergy /
                                (ACTDistance * Constants.MCEV + supplementEnergy))
        acdistance.append(ACTDistance)

    target_E = 0
    target_R = 0
    target_ME = 0

    target_acdistance = 0

    for i in range(Constants.NUM_OF_NETWORKS):
        target_E += AverageEnergy[i]
        target_R += Rrate[i]
        target_ME += ChargeEfficiency[i]

        target_acdistance += acdistance[i]

    print('MC_MAX_MOVE_DISTANCE:', Constants.MC_MAX_MOVE_DISTANCE)
    print('平均能量，MC充电效率:', target_E / Constants.NUM_OF_NETWORKS,
          target_ME / Constants.NUM_OF_NETWORKS)
    # print('FND， 0.3ND',target_FND/posRound, target_tND/posRound)
    print('acdistance: ', target_acdistance / Constants.NUM_OF_NETWORKS)

    # todo
    return target_E / Constants.NUM_OF_NETWORKS, target_ME / Constants.NUM_OF_NETWORKS


def test():
    mapDic = NetworkGeneration.initMapDic(Constants.NUM_OF_NETWORKS, Constants.NUM_OF_NODES,
                                          Constants.MAX_COMMUNICATE_RANGE)
    nodeInfoGenerationRateDic = NetworkGeneration.initNodeInformationGenerationRateDic(
        Constants.NUM_OF_NETWORKS, Constants.NUM_OF_NODES, Constants.MIN_INFO_GENERATE_RATE,
        Constants.MAX_INFO_GENERATE_RATE)
    chargeByREEC(Constants.NUM_OF_NODES, mapDic, nodeInfoGenerationRateDic)


if __name__ == '__main__':
    test()
