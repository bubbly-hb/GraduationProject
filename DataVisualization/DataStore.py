import os
import json
import time
import sys

sys.path.append(os.getcwd())
sys.path.append(os.getcwd() + "\\ChargingScheme")
# print('current path:', os.getcwd())
# print('sys path:', sys.path)
from ChargingScheme.Constants import Constants
from ChargingScheme.NetworkGeneration import initMapDic, initNodeInformationGenerationRateDic

PWD = os.getcwd() + "\\data\\"
if not os.path.isdir(PWD):
    os.mkdir(PWD)


# write Constans info
def writeConstants(targetpwd):
    dic = Constants.getDic()
    js = json.dumps(dic)

    with open(targetpwd + "_Constants", "w") as f:
        f.write(js)


# get Constans info
def setConstants(targetpwd):
    with open(targetpwd + "_Constants", "r") as f:
        js = f.read()
        dic = json.loads(js)
    Constants.setByDic(dic)


def createNewFile(desc):
    os.mkdir(PWD + desc + "\\")


# 即时生成数据进行仿真
def simu(desc):
    createNewFile(desc)  # 先在data文件夹下面建一个子文件夹
    targetpwd = PWD + desc + "\\"
    writeConstants(targetpwd)

    map_dic = initMapDic(Constants.NUM_OF_NETWORKS, Constants.NUM_OF_NODES,
                         Constants.MAX_COMMUNICATE_RANGE)
    js = json.dumps(map_dic)

    with open(targetpwd + "_MAP", "w") as f:
        f.write(js)

    nodeR_dic = initNodeInformationGenerationRateDic(Constants.NUM_OF_NETWORKS,
                                                     Constants.NUM_OF_NODES,
                                                     Constants.MIN_INFO_GENERATE_RATE,
                                                     Constants.MAX_INFO_GENERATE_RATE)
    js = json.dumps(nodeR_dic)
    with open(targetpwd + "_INFO", "w") as f:
        f.write(js)

    return map_dic, nodeR_dic


# 重现仿真
# desc:对数据的描述，包含时间信息和概述字符串
def resimu(filename):
    targetpwd = PWD + filename + "\\"
    setConstants(targetpwd)

    with open(targetpwd + "_MAP", "r") as f:
        js = f.read()
        map_dic = json.loads(js)

    with open(targetpwd + "_INFO", "r") as f:
        js = f.read()
        nodeR_dic = json.loads(js)

    return map_dic, nodeR_dic


def test():
    t = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
    map_dic, nodeR_dic = simu(t)
    print(map_dic, nodeR_dic)


if __name__ == '__main__':
    test()
