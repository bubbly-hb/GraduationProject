import os
import json
import time
import sys

sys.path.append("e:\\python\\GraduationProject")
sys.path.append("e:\\python\\GraduationProject\\ChargingScheme")
# print('current path:', os.getcwd())
# print('sys path:', sys.path)
import ChargingScheme.Constants as Constants
from ChargingScheme.NetworkGeneration import initMapDic, initNodeInformationGenerationRateDic


def get(mapname, infoname, nodesNum, t):
    # t = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
    targetpwd = os.getcwd() + "\\data\\"
    if os.path.isfile(targetpwd + mapname):
        with open(targetpwd + mapname, "r") as f:
            js = f.read()
            map_dic = json.loads(js)
    else:
        map_dic = initMapDic(Constants.NUM_OF_NETWORKS, nodesNum, Constants.MAX_COMMUNICATE_RANGE)
        js = json.dumps(map_dic)
        try:
            with open(targetpwd + "_MAP_" + t, "w") as f:
                f.write(js)
        except Exception as e:
            print(e)
            os.mkdir("data")
            with open(targetpwd + "_MAP_" + t, "w") as f:
                f.write(js)

    if os.path.isfile(targetpwd + infoname):
        with open(targetpwd + infoname, "r") as f:
            js = f.read()
            nodeR_dic = json.loads(js)
    else:
        nodeR_dic = initNodeInformationGenerationRateDic(Constants.NUM_OF_NETWORKS, nodesNum,
                                                         Constants.MIN_INFO_GENERATE_RATE,
                                                         Constants.MAX_INFO_GENERATE_RATE)
        js = json.dumps(nodeR_dic)
        try:
            with open(targetpwd + "_INFO_" + t, "w") as f:
                f.write(js)
        except Exception as e:
            print(e)
            os.mkdir("data")
            with open(targetpwd + "_INFO_" + t, "w") as f:
                f.write(js)

    return map_dic, nodeR_dic


def test():
    t = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
    map_dic, nodeR_dic = get("_INFO_2022-01-16_15-36-26", "_MAP_2022-01-16_15-36-26", 4, t)
    print(map_dic, nodeR_dic)


if __name__ == '__main__':
    test()
