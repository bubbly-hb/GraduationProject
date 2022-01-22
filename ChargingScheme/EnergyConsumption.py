from Constants import Constants


# nodesNum：网络节点数量
# nodeStatus：标识节点存活状态
# topuMatrix：拓扑关系矩阵，topuMatrix[i][j]的值是一个列表，里面存储节点索引，这些节点是节点i的孩子节点，并且通过i->j路径由i转发给j
# infoGeneRateList：节点信息产生速率列表
# energyConsumeRateList：节点实际能耗速率列表
def updateEnergyConsume(nodesNum, nodeStatus, topuMatrix, infoGeneRateList, energyConsumeRateList):
    for i in range(1, nodesNum + 1):
        if nodeStatus[i] == 1:
            fji = 0
            fij = 0
            for j in range(1, nodesNum + 1):
                for q in topuMatrix[j][i]:
                    if nodeStatus[q] == 1:
                        fji += infoGeneRateList[q]
                for w in topuMatrix[i][j]:
                    if nodeStatus[w] == 1:
                        fij += infoGeneRateList[w]

            # 单位为mj/s
            energyConsumeRateList[
                i] = fji * Constants.EIR + fij * Constants.EIS + infoGeneRateList[i] * Constants.EIG
