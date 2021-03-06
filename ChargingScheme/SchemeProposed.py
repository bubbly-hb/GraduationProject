import numpy as np
import math
from Constants import Constants
import NetworkGeneration
import NetworkTopuBuild
import EnergyConsumption
import CommonHelper


def count_upbound(nodesNum, ev, ls_now, last_send_time, sumT, E_upbound, dis):
    for i in range(1, nodesNum + 1):
        if ls_now[i] > ev[i] * (sumT + dis[i][0] / Constants.MC_SPEED - last_send_time):
            E_upbound[i] = ls_now[i] - ev[i] * (sumT + dis[i][0] / Constants.MC_SPEED -
                                                last_send_time)
        else:
            E_upbound[i] = 0


def count_downbound(nodesNum, ev, ls_now, last_send_time, sumT, E_downbound, T):
    for i in range(1, nodesNum + 1):
        if ls_now[i] > ev[i] * (sumT + T - last_send_time):
            E_downbound[i] = ls_now[i] - ev[i] * (sumT + T - last_send_time)
        else:
            E_downbound[i] = 0


def updateEmergencyDegree(nodesNum, ev, eval_Energy_now, last_send_time, SumTime, E_upbound,
                          E_downbound, T, DistanceMatrix, emergencyDegreeList):
    count_upbound(nodesNum, ev, eval_Energy_now, last_send_time, SumTime, E_upbound,
                  DistanceMatrix)
    count_downbound(nodesNum, ev, eval_Energy_now, last_send_time, SumTime, E_downbound, T)
    tag = True
    for i in range(1, nodesNum + 1):
        if E_downbound[i] <= 0:
            tag = False
            break
    if tag:
        for i in range(1, nodesNum + 1):
            emergencyDegreeList[i] = Constants.NODE_FULL_ENERGY - E_upbound[i]
        return True
    else:
        return False


def countC(nodesNum, C, timedeadline, random_list, DistanceMatrix):
    for i in range(1, nodesNum + 1):
        angle = 0
        if random_list[i][0] > 0 and random_list[i][1] > 0:
            angle = math.asin(random_list[i][1] /
                              math.hypot(random_list[i][0], random_list[i][1])) * 180 / math.pi
        elif random_list[i][0] < 0 and random_list[i][1] > 0:
            angle = 180 - math.asin(random_list[i][1] / math.hypot(
                random_list[i][0], random_list[i][1])) * 180 / math.pi
        elif random_list[i][0] < 0 and random_list[i][1] < 0:
            angle = 180 + math.asin(-random_list[i][1] / math.hypot(
                random_list[i][0], random_list[i][1])) * 180 / math.pi
        elif random_list[i][0] > 0 and random_list[i][1] < 0:
            angle = 360 + math.asin(random_list[i][1] / math.hypot(
                random_list[i][0], random_list[i][1])) * 180 / math.pi
        elif random_list[i][0] == 0 and random_list[i][1] > 0:
            angle = 90
        elif random_list[i][0] == 0 and random_list[i][1] < 0:
            angle = 270
        elif random_list[i][0] > 0 and random_list[i][1] == 0:
            angle = 0
        elif random_list[i][0] < 0 and random_list[i][1] == 0:
            angle = 180
        C[i] = -0.7 * DistanceMatrix[0][i] + 0.1 * timedeadline[i] + 0.3 * (
            (angle / 360) * DistanceMatrix[0][i])


def countTimedeadline(nodesNum, timedeadline, last_send_time, eval_Energy_now, ev):
    for i in range(1, nodesNum + 1):
        timedeadline[i] = last_send_time + eval_Energy_now[i] / ev[i]


def sortCandidate(sort_candidate, candidateSet, ev):
    length = len(candidateSet)
    dic = {}
    for i in range(length):
        dic[candidateSet[i]] = ev[candidateSet[i]]
    for i in range(length):
        max_pos = max(dic, key=dic.get)
        sort_candidate.append(max_pos)
        dic[max_pos] = -1


def check(temp_Path, timedeadline, DistanceMatrix, eval_Energy_now):
    length = len(temp_Path)
    travelDistance = 0
    travelTime = 0
    for i in range(1, length):
        travelDistance += DistanceMatrix[temp_Path[i - 1]][temp_Path[i]]
        if travelDistance > Constants.MC_MAX_MOVE_DISTANCE:
            return Constants.INF
        travelTime += DistanceMatrix[temp_Path[i - 1]][temp_Path[i]] / Constants.MC_SPEED
        if travelTime > timedeadline[temp_Path[i]]:
            return Constants.INF
        travelTime += (Constants.NODE_FULL_ENERGY -
                       eval_Energy_now[temp_Path[i]]) / Constants.CHARINGSPEED
    travelDistance += DistanceMatrix[temp_Path[length - 1]][0]
    if travelDistance > Constants.MC_MAX_MOVE_DISTANCE:
        return Constants.INF
    return travelDistance


def process(temp_Path, min_pos, timedeadline, DistanceMatrix, eval_Energy_now):
    length = len(temp_Path)
    dic = {}
    for i in range(1, length + 1):
        temp_Path.insert(i, min_pos)
        dic[i] = check(temp_Path, timedeadline, DistanceMatrix, eval_Energy_now)
        del temp_Path[i]
    min_p = min(dic, key=dic.get)
    if dic[min_p] != Constants.INF:
        temp_Path.insert(min_p, min_pos)
        return True
    return False


def findPath(sort_candidate, C, timedeadline, path, DistanceMatrix, eval_Energy_now):
    dic = {}
    length = len(sort_candidate)
    for i in range(length):
        dic[sort_candidate[i]] = C[sort_candidate[i]]
    temp_Path = [0]
    for i in range(length):
        min_pos = min(dic, key=dic.get)
        if not process(temp_Path, min_pos, timedeadline, DistanceMatrix, eval_Energy_now):
            return False
        dic[min_pos] = Constants.INF
    for i in range(1, length + 1):
        path.append(temp_Path[i])
    return True


def findPathByVRPTD(nodesNum, E_downbound, path, DistanceMatrix, eval_Energy_now, last_send_time,
                    ev, random_list):
    candidateSet = []
    timedeadline = [0 for i in range(nodesNum + 1)]
    for i in range(1, nodesNum + 1):
        if E_downbound[i] == 0:
            candidateSet.append(i)
    C = [0 for i in range(nodesNum + 1)]
    countTimedeadline(nodesNum, timedeadline, last_send_time, eval_Energy_now, ev)
    countC(nodesNum, C, timedeadline, random_list, DistanceMatrix)
    sort_candidate = []
    sortCandidate(sort_candidate, candidateSet, ev)
    length = len(candidateSet)
    for i in range(length):
        if findPath(sort_candidate, C, timedeadline, path, DistanceMatrix, eval_Energy_now):
            break
        else:
            sort_candidate.pop()
    lengthOfPath = len(path)
    if lengthOfPath == 1 + length:
        dic = {}
        for i in range(1, nodesNum + 1):
            if E_downbound[i] == 0:
                dic[i] = Constants.INF
            else:
                dic[i] = E_downbound[i]
        for i in range(1, nodesNum + 1):
            if E_downbound[i] == 0:
                continue
            min_pos = min(dic, key=dic.get)
            dic[min_pos] = Constants.INF
            process(path, min_pos, timedeadline, DistanceMatrix, eval_Energy_now)
            # if process(path, min_pos, timedeadline):
            #     continue
            # else:
            #     break
    path.append(0)


def chargeByREBE(nodesNum, mapDic, nodeInfoGenerationRateDic):
    AverageEnergy = []
    Rrate = []
    ChargeEfficiency = []
    acdistance = []
    target_nd = [0.0, 0.0, 0.0, 0.0]
    for pos_round in range(Constants.NUM_OF_NETWORKS):
        mcChargingPath = [0]  # MCS???????????????path[0]???BS???path[1]??????????????????????????????
        topuCostMatrix = np.ones((nodesNum + 1, nodesNum + 1))  # ???????????????????????????????????????????????????????????????

        numOfChildNodesList = [0 for i in range(nodesNum + 1)]  # ?????????????????????????????????????????????????????????????????????????????????,????????????0

        infoGeneRateList = nodeInfoGenerationRateDic[pos_round]

        infoTransRateMatrix = np.zeros(
            (nodesNum + 1, nodesNum + 1))  # ?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
        energyConsumeRateList = [0 for i in range(nodesNum + 1)]  # ?????????????????????
        emergencyDegree = [i for i in range(nodesNum + 1, 0, -1)]  # ????????????
        residualEnergy = [Constants.NODE_FULL_ENERGY for i in range(nodesNum + 1)]  # ??????????????????

        sortedEmergencyNodeList = [1 for i in range(nodesNum + 1)]  # ?????????????????????????????????????????????
        sortedEmergencyNodeList[0] = 0  # BS???0????????????sortedEmergencyNodeList[1]??????????????????????????????????????????
        emergencyDegree[0] = 0  # ?????????sortByEmergency()???????????????
        topuMatrix = [[[] * 1 for _ in range(nodesNum + 1)] for _ in range(nodesNum + 1)]

        # to check
        sojournTime = 0

        SumR = 0  # ?????????????????????
        AnchorAmount = 0  # ????????????
        # MCS????????????????????????????????????BS???????????????????????????????????????BS
        nodeStatus = [1 for i in range(nodesNum + 1)]  # ?????????????????????-1?????????????????????1
        SumTime = 0

        ACTDistance = 0  # MC??????????????????
        supplementEnergy = 0

        Round = Constants.ROUND

        nodeDeadTimeList = []

        eval_Energy_last = [Constants.NODE_FULL_ENERGY for i in range(nodesNum + 1)]
        eval_Energy_now = [Constants.NODE_FULL_ENERGY for i in range(nodesNum + 1)]
        last_send_time = 0  # ????????????????????????????????????eval_energy_now
        E_upbound = [Constants.NODE_FULL_ENERGY for i in range(nodesNum + 1)]
        E_downbound = [Constants.NODE_FULL_ENERGY for i in range(nodesNum + 1)]

        ev = [0 for i in range(nodesNum + 1)]

        MCtotalE = Constants.MC_FULL_ENERGY

        nodeDeadTimeList = []

        random_list = mapDic[pos_round]
        distanceMatrix = NetworkGeneration.getDistancematrix(random_list)  # ???????????????????????????

        NetworkTopuBuild.buildTopu(nodesNum, distanceMatrix, topuCostMatrix, residualEnergy,
                                   nodeStatus, numOfChildNodesList, infoTransRateMatrix,
                                   topuMatrix, infoGeneRateList)

        EnergyConsumption.updateEnergyConsume(nodesNum, nodeStatus, topuMatrix, infoGeneRateList,
                                              energyConsumeRateList)

        for i in range(1, nodesNum + 1):
            ev[i] = energyConsumeRateList[i]

        for count in range(Round):
            MCtotalE = Constants.MC_FULL_ENERGY
            mcChargingPath.clear()  # ??????????????????path
            mcChargingPath.append(0)

            if updateEmergencyDegree(nodesNum, ev, eval_Energy_now, last_send_time, SumTime,
                                     E_upbound, E_downbound, Constants.T, distanceMatrix,
                                     emergencyDegree):
                CommonHelper.sortByEmergency(nodesNum, emergencyDegree, sortedEmergencyNodeList)
                CommonHelper.chooseAnchorAndChargePath(nodesNum, distanceMatrix,
                                                       sortedEmergencyNodeList,
                                                       Constants.MC_MAX_MOVE_DISTANCE,
                                                       mcChargingPath)
                AnchorAmount = len(mcChargingPath) - 1  # ????????????

                mcChargingPath.append(0)
            else:
                findPathByVRPTD(nodesNum, E_downbound, mcChargingPath, distanceMatrix,
                                eval_Energy_now, last_send_time, ev, random_list)
                AnchorAmount = len(mcChargingPath) - 2

            # print("AnchorAmount:",AnchorAmount)

            for k in range(0, AnchorAmount + 1):
                if MCtotalE - distanceMatrix[mcChargingPath[k]][mcChargingPath[k + 1]] * Constants.MCEV <= \
                        distanceMatrix[mcChargingPath[k + 1]][0] * Constants.MCEV:
                    traverTime = distanceMatrix[mcChargingPath[k]][0] / Constants.MC_SPEED
                    ACTDistance += distanceMatrix[mcChargingPath[k]][0]

                    buzu = Constants.T_CIRCLE - SumTime % Constants.T_CIRCLE
                    if traverTime > buzu:
                        if traverTime < buzu + Constants.T_CIRCLE:
                            last_send_time = SumTime + buzu
                            for i in range(1, nodesNum + 1):
                                eval_Energy_last[i] = eval_Energy_now[i]
                                if nodeStatus[i] == 1:  # ???????????????????????????????????????????????????????????????????????????
                                    if residualEnergy[i] < energyConsumeRateList[i] * buzu:
                                        eval_Energy_now[i] = 0
                                    else:
                                        eval_Energy_now[i] = residualEnergy[
                                            i] - energyConsumeRateList[i] * buzu
                        else:
                            zz = (SumTime + traverTime) % Constants.T_CIRCLE
                            last_send_time = (SumTime + traverTime) - zz
                            for i in range(1, nodeStatus + 1):
                                if nodeStatus[i] == 1:  # ???????????????????????????????????????????????????????????????????????????
                                    if residualEnergy[i] < energyConsumeRateList[i] * (
                                            last_send_time - SumTime - Constants.T_CIRCLE):
                                        eval_Energy_last[i] = 0
                                        eval_Energy_now[i] = 0
                                    else:
                                        eval_Energy_last[
                                            i] = residualEnergy[i] - energyConsumeRateList[i] * (
                                                last_send_time - SumTime - Constants.T_CIRCLE)

                                        if residualEnergy[i] < energyConsumeRateList[i] * (
                                                last_send_time - SumTime):
                                            eval_Energy_now[i] = 0
                                        else:
                                            eval_Energy_now[i] = residualEnergy[
                                                i] - energyConsumeRateList[i] * (last_send_time -
                                                                                 SumTime)

                        for evi in range(1, nodesNum + 1):
                            zz = (eval_Energy_now[evi] -
                                  eval_Energy_last[evi]) / Constants.T_CIRCLE
                            if zz > 0:
                                ev[evi] = zz

                    SumTime += traverTime

                    for i in range(1, nodesNum + 1):

                        if nodeStatus[i] == 1:
                            if residualEnergy[i] < energyConsumeRateList[i] * traverTime:
                                nodeStatus[i] = -1
                                SumR += infoGeneRateList[i] * residualEnergy[
                                    i] / energyConsumeRateList[i]  # ????????????????????????????????????????????????
                                residualEnergy[i] = 0
                                for q in range(1, nodesNum + 1):
                                    for nd in topuMatrix[i][q]:
                                        nodeStatus[nd] = -1
                                EnergyConsumption.updateEnergyConsume(
                                    nodesNum, nodeStatus, topuMatrix, infoGeneRateList,
                                    energyConsumeRateList)
                            else:
                                residualEnergy[i] -= energyConsumeRateList[i] * traverTime
                                SumR += infoGeneRateList[i] * traverTime
                        elif residualEnergy[i] > 0:
                            if residualEnergy[i] < energyConsumeRateList[i] * traverTime:
                                residualEnergy[i] = 0
                                EnergyConsumption.updateEnergyConsume(
                                    nodesNum, nodeStatus, topuMatrix, infoGeneRateList,
                                    energyConsumeRateList)
                            else:
                                residualEnergy[i] -= energyConsumeRateList[i] * traverTime
                    CommonHelper.updateND(nodesNum, nodeDeadTimeList, residualEnergy, SumTime)
                    break

                traverTime = distanceMatrix[mcChargingPath[k]][mcChargingPath[
                    k + 1]] / Constants.MC_SPEED
                ACTDistance += distanceMatrix[mcChargingPath[k]][mcChargingPath[k + 1]]
                MCtotalE -= Constants.MCEV * distanceMatrix[mcChargingPath[k]][mcChargingPath[
                    k + 1]]  # MC???????????????????????????

                buzu = Constants.T_CIRCLE - SumTime % Constants.T_CIRCLE
                if traverTime > buzu:
                    if traverTime < buzu + Constants.T_CIRCLE:
                        last_send_time = SumTime + buzu
                        for i in range(1, nodesNum + 1):
                            eval_Energy_last[i] = eval_Energy_now[i]
                            if nodeStatus[i] == 1:  # ???????????????????????????????????????????????????????????????????????????
                                if residualEnergy[i] < energyConsumeRateList[i] * buzu:
                                    eval_Energy_now[i] = 0
                                else:
                                    eval_Energy_now[
                                        i] = residualEnergy[i] - energyConsumeRateList[i] * buzu
                    else:
                        zz = (SumTime + traverTime) % Constants.T_CIRCLE
                        last_send_time = (SumTime + traverTime) - zz
                        for i in range(1, nodesNum + 1):
                            if nodeStatus[i] == 1:  # ???????????????????????????????????????????????????????????????????????????
                                if residualEnergy[i] < energyConsumeRateList[i] * (
                                        last_send_time - SumTime - Constants.T_CIRCLE):
                                    eval_Energy_last[i] = 0
                                    eval_Energy_now[i] = 0
                                else:
                                    eval_Energy_last[
                                        i] = residualEnergy[i] - energyConsumeRateList[i] * (
                                            last_send_time - SumTime - Constants.T_CIRCLE)

                                    if residualEnergy[i] < energyConsumeRateList[i] * (
                                            last_send_time - SumTime):
                                        eval_Energy_now[i] = 0
                                    else:
                                        eval_Energy_now[
                                            i] = residualEnergy[i] - energyConsumeRateList[i] * (
                                                last_send_time - SumTime)

                    for evi in range(1, nodesNum + 1):
                        zz = (eval_Energy_now[evi] - eval_Energy_last[evi]) / Constants.T_CIRCLE
                        if zz > 0:
                            ev[evi] = zz

                SumTime += traverTime

                for i in range(1, nodesNum + 1):

                    if nodeStatus[i] == 1:
                        if residualEnergy[i] < energyConsumeRateList[i] * traverTime:
                            nodeStatus[i] = -1
                            SumR += infoGeneRateList[i] * residualEnergy[
                                i] / energyConsumeRateList[i]  # ????????????????????????????????????????????????
                            residualEnergy[i] = 0
                            for q in range(1, nodesNum + 1):
                                for nd in topuMatrix[i][q]:
                                    nodeStatus[nd] = -1
                            EnergyConsumption.updateEnergyConsume(nodesNum, nodeStatus, topuMatrix,
                                                                  infoGeneRateList,
                                                                  energyConsumeRateList)
                        else:
                            residualEnergy[i] -= energyConsumeRateList[i] * traverTime
                            SumR += infoGeneRateList[i] * traverTime
                    elif residualEnergy[i] > 0:
                        if residualEnergy[i] < energyConsumeRateList[i] * traverTime:
                            residualEnergy[i] = 0
                            EnergyConsumption.updateEnergyConsume(nodesNum, nodeStatus, topuMatrix,
                                                                  infoGeneRateList,
                                                                  energyConsumeRateList)
                        else:
                            residualEnergy[i] -= energyConsumeRateList[i] * traverTime
                CommonHelper.updateND(nodesNum, nodeDeadTimeList, residualEnergy, SumTime)

                # print('MC?????????%d?????????%d??????????????????%f'%(k,k+1,SumR))               #??????
                # print("???????????????????????????",r)                                       #??????

                if k != AnchorAmount:
                    if MCtotalE - (Constants.NODE_FULL_ENERGY - residualEnergy[mcChargingPath[k + 1]]) <= \
                            distanceMatrix[mcChargingPath[k + 1]][0] * Constants.MCEV:
                        sojournTime = (MCtotalE - distanceMatrix[mcChargingPath[k + 1]][0] * Constants.MCEV) / \
                                      Constants.CHARINGSPEED

                        buzu = Constants.T_CIRCLE - SumTime % Constants.T_CIRCLE
                        if sojournTime > buzu:
                            if sojournTime < buzu + Constants.T_CIRCLE:
                                last_send_time = SumTime + buzu
                                for i in range(1, nodesNum + 1):
                                    eval_Energy_last[i] = eval_Energy_now[i]
                                    if nodeStatus[i] == 1:  # ???????????????????????????????????????????????????????????????????????????
                                        if residualEnergy[i] < energyConsumeRateList[i] * buzu:
                                            eval_Energy_now[i] = 0
                                        else:
                                            eval_Energy_now[i] = residualEnergy[
                                                i] - energyConsumeRateList[i] * buzu
                            else:
                                zz = (SumTime + sojournTime) % Constants.T_CIRCLE
                                last_send_time = (SumTime + sojournTime) - zz
                                for i in range(1, nodesNum + 1):
                                    if nodeStatus[i] == 1:  # ???????????????????????????????????????????????????????????????????????????
                                        if residualEnergy[i] < energyConsumeRateList[i] * (
                                                last_send_time - SumTime - Constants.T_CIRCLE):
                                            eval_Energy_last[i] = 0
                                            eval_Energy_now[i] = 0
                                        else:
                                            eval_Energy_last[i] = residualEnergy[
                                                i] - energyConsumeRateList[i] * (
                                                    last_send_time - SumTime - Constants.T_CIRCLE)

                                            if residualEnergy[i] < energyConsumeRateList[i] * (
                                                    last_send_time - SumTime):
                                                eval_Energy_now[i] = 0
                                            else:
                                                eval_Energy_now[i] = residualEnergy[
                                                    i] - energyConsumeRateList[i] * (
                                                        last_send_time - SumTime)

                            for evi in range(1, nodesNum + 1):
                                zz = (eval_Energy_now[evi] -
                                      eval_Energy_last[evi]) / Constants.T_CIRCLE
                                if zz > 0:
                                    ev[evi] = zz

                        supplementEnergy += (
                            MCtotalE - distanceMatrix[mcChargingPath[k + 1]][0] * Constants.MCEV)
                        residualEnergy[mcChargingPath[k + 1]] += (
                            MCtotalE - distanceMatrix[mcChargingPath[k + 1]][0] * Constants.MCEV
                        )  # path[k+1]?????????????????????
                        nodeStatus[mcChargingPath[k + 1]] = 1
                        for q in range(1, nodesNum + 1):
                            for nd in topuMatrix[mcChargingPath[k + 1]][q]:
                                if residualEnergy[nd] > 0:
                                    nodeStatus[nd] = 1
                        EnergyConsumption.updateEnergyConsume(nodesNum, nodeStatus, topuMatrix,
                                                              infoGeneRateList,
                                                              energyConsumeRateList)

                        for i in range(1, nodesNum + 1):
                            if nodeStatus[i] == 1:
                                if residualEnergy[i] < energyConsumeRateList[i] * sojournTime:
                                    nodeStatus[i] = -1
                                    SumR += infoGeneRateList[i] * residualEnergy[
                                        i] / energyConsumeRateList[i]  # ??????????????????????????????????????????????????????????????????????????????
                                    residualEnergy[i] = 0
                                    for q in range(1, nodesNum + 1):
                                        for nd in topuMatrix[i][q]:
                                            nodeStatus[nd] = -1
                                    EnergyConsumption.updateEnergyConsume(
                                        nodesNum, nodeStatus, topuMatrix, infoGeneRateList,
                                        energyConsumeRateList)
                                else:
                                    residualEnergy[i] -= energyConsumeRateList[i] * sojournTime
                                    SumR += infoGeneRateList[i] * sojournTime
                            elif residualEnergy[i] > 0:
                                if residualEnergy[i] < energyConsumeRateList[i] * sojournTime:
                                    residualEnergy[i] = 0
                                    EnergyConsumption.updateEnergyConsume(
                                        nodesNum, nodeStatus, topuMatrix, infoGeneRateList,
                                        energyConsumeRateList)
                                else:
                                    residualEnergy[i] -= energyConsumeRateList[i] * sojournTime

                        SumTime += sojournTime
                        CommonHelper.updateND(nodesNum, nodeDeadTimeList, residualEnergy, SumTime)
                        MCtotalE = distanceMatrix[mcChargingPath[k + 1]][0] * Constants.MCEV
                    else:
                        sojournTime = (Constants.NODE_FULL_ENERGY - residualEnergy[mcChargingPath[k + 1]]) / \
                                      Constants.CHARINGSPEED
                        MCtotalE -= (Constants.NODE_FULL_ENERGY -
                                     residualEnergy[mcChargingPath[k + 1]])  # MC????????????????????????????????????

                        buzu = Constants.T_CIRCLE - SumTime % Constants.T_CIRCLE
                        if sojournTime > buzu:
                            if sojournTime < buzu + Constants.T_CIRCLE:
                                last_send_time = SumTime + buzu
                                for i in range(1, nodesNum + 1):
                                    eval_Energy_last[i] = eval_Energy_now[i]
                                    if nodeStatus[i] == 1:  # ???????????????????????????????????????????????????????????????????????????
                                        if residualEnergy[i] < energyConsumeRateList[i] * buzu:
                                            eval_Energy_now[i] = 0
                                        else:
                                            eval_Energy_now[i] = residualEnergy[
                                                i] - energyConsumeRateList[i] * buzu
                            else:
                                zz = (SumTime + sojournTime) % Constants.T_CIRCLE
                                last_send_time = (SumTime + sojournTime) - zz
                                for i in range(1, nodesNum + 1):
                                    if nodeStatus[i] == 1:  # ???????????????????????????????????????????????????????????????????????????
                                        if residualEnergy[i] < energyConsumeRateList[i] * (
                                                last_send_time - SumTime - Constants.T_CIRCLE):
                                            eval_Energy_last[i] = 0
                                            eval_Energy_now[i] = 0
                                        else:
                                            eval_Energy_last[i] = residualEnergy[
                                                i] - energyConsumeRateList[i] * (
                                                    last_send_time - SumTime - Constants.T_CIRCLE)

                                            if residualEnergy[i] < energyConsumeRateList[i] * (
                                                    last_send_time - SumTime):
                                                eval_Energy_now[i] = 0
                                            else:
                                                eval_Energy_now[i] = residualEnergy[
                                                    i] - energyConsumeRateList[i] * (
                                                        last_send_time - SumTime)

                            for evi in range(1, nodesNum + 1):
                                zz = (eval_Energy_now[evi] -
                                      eval_Energy_last[evi]) / Constants.T_CIRCLE
                                if zz > 0:
                                    ev[evi] = zz

                        supplementEnergy += Constants.NODE_FULL_ENERGY - residualEnergy[
                            mcChargingPath[k + 1]]
                        residualEnergy[mcChargingPath[
                            k + 1]] = Constants.NODE_FULL_ENERGY  # path[k+1]?????????????????????
                        nodeStatus[mcChargingPath[k + 1]] = 1
                        for q in range(1, nodesNum + 1):
                            for nd in topuMatrix[mcChargingPath[k + 1]][q]:
                                if residualEnergy[nd] > 0:
                                    nodeStatus[nd] = 1
                        EnergyConsumption.updateEnergyConsume(nodesNum, nodeStatus, topuMatrix,
                                                              infoGeneRateList,
                                                              energyConsumeRateList)

                        for i in range(1, nodesNum + 1):
                            if nodeStatus[i] == 1:
                                if residualEnergy[i] < energyConsumeRateList[i] * sojournTime:
                                    nodeStatus[i] = -1
                                    SumR += infoGeneRateList[i] * residualEnergy[
                                        i] / energyConsumeRateList[i]  # ??????????????????????????????????????????????????????????????????????????????
                                    residualEnergy[i] = 0
                                    for q in range(1, nodesNum + 1):
                                        for nd in topuMatrix[i][q]:
                                            nodeStatus[nd] = -1
                                    EnergyConsumption.updateEnergyConsume(
                                        nodesNum, nodeStatus, topuMatrix, infoGeneRateList,
                                        energyConsumeRateList)
                                else:
                                    residualEnergy[i] -= energyConsumeRateList[i] * sojournTime
                                    SumR += infoGeneRateList[i] * sojournTime
                            elif residualEnergy[i] > 0:
                                if residualEnergy[i] < energyConsumeRateList[i] * sojournTime:
                                    residualEnergy[i] = 0
                                    EnergyConsumption.updateEnergyConsume(
                                        nodesNum, nodeStatus, topuMatrix, infoGeneRateList,
                                        energyConsumeRateList)
                                else:
                                    residualEnergy[i] -= energyConsumeRateList[i] * sojournTime

                        residualEnergy[mcChargingPath[
                            k + 1]] = Constants.NODE_FULL_ENERGY  # path[k+1]?????????????????????

                        SumTime += sojournTime
                        CommonHelper.updateND(nodesNum, nodeDeadTimeList, residualEnergy, SumTime)

                    # print('MC???????????????%d?????????????????????%f'%(k+1,SumR))
                    # print("???????????????????????????", r)                      # ??????

            # print('???', count+1, '???', '??????????????????', SumR)

            if (count + 1) == Round:
                SumofRestEnergy = 0
                for i in range(1, nodesNum + 1):
                    # print('??????',i,'??????????????????',residualEnergy[i])
                    SumofRestEnergy += residualEnergy[i]
                print('???', count + 1, '???', "????????????????????????:", SumofRestEnergy / nodesNum, "  ??????: ",
                      SumTime)

                AverageEnergy.append(SumofRestEnergy / nodesNum)

        # print('?????????????????????', SumR)
        # print("???????????????", SumTime)
        # print("MC???????????????", ACTDistance)
        # print("?????????????????????????????????????????????/???????????????", SumR / SumTime)
        # print("MC????????????????????????", supplementEnergy)
        # print("MC????????????", supplementEnergy / ACTDistance)
        # print("????????????????????????????????????/????????????",(B*N-SumofRestEnergy)/SumTime)

        Rrate.append(SumR / SumTime)
        ChargeEfficiency.append(supplementEnergy /
                                (ACTDistance * Constants.MCEV + supplementEnergy))
        acdistance.append(ACTDistance)

        CommonHelper.fillNDList(nodeDeadTimeList, Constants.STANDARDLIST)
        for i in range(len(target_nd)):
            target_nd[i] += nodeDeadTimeList[i]

    for i in range(len(target_nd)):
        target_nd[i] /= Constants.NUM_OF_NETWORKS

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
    print('???????????????MC????????????:', target_E / Constants.NUM_OF_NETWORKS,
          target_ME / Constants.NUM_OF_NETWORKS)
    # print('FND??? 0.3ND',target_FND/posRound, target_tND/posRound)
    print('acdistance: ', target_acdistance / Constants.NUM_OF_NETWORKS)

    # todo
    return target_E / Constants.NUM_OF_NETWORKS, target_ME / Constants.NUM_OF_NETWORKS, target_nd


def test():
    mapDic = NetworkGeneration.initMapDic(Constants.NUM_OF_NETWORKS, Constants.NUM_OF_NODES,
                                          Constants.MAX_COMMUNICATE_RANGE)
    nodeInfoGenerationRateDic = NetworkGeneration.initNodeInformationGenerationRateDic(
        Constants.NUM_OF_NETWORKS, Constants.NUM_OF_NODES, Constants.MIN_INFO_GENERATE_RATE,
        Constants.MAX_INFO_GENERATE_RATE)
    chargeByREBE(Constants.NUM_OF_NODES, mapDic, nodeInfoGenerationRateDic)


if __name__ == '__main__':
    test()
