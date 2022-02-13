class Constants:
    INF = 99999999
    NUM_OF_NETWORKS = 30  # 网络个数
    NUM_OF_NODES = 150  # 单个网络节点数
    MAX_COMMUNICATE_RANGE = 20  # 最大信息传输距离 m
    MAX_INFO_GENERATE_RATE = 2000  # 节点最大信息生成速率 bps
    MIN_INFO_GENERATE_RATE = 1200  # 节点最小信息生成速率 bps
    NODE_FULL_ENERGY = 2000000  # mJ, 即20kJ, which is the maximum capacity of the battery of each sensor node
    MC_FULL_ENERGY = 50000000  # mJ, 即50kJ, which is the maximum capacity of the battery of MC
    MC_MAX_MOVE_DISTANCE = 300  # m, 单轮充电中MC最大移动距离
    ROUND = 1000  # 对网络的充电轮数
    MC_SPEED = 3  # m/s
    PRICE = 0  # REEC额外信息传输代价
    CHARINGSPEED = 500000  # mj/s, 决定MC在锚点处停留时间长短，与锚点剩余能量多少有关,即MC充电速率
    MCEV = 100000  # 0.6kJ/m ,MC移动单位距离耗能
    T = 200  # expected waiting time of the last charged sensor in the current charging cycle before it be charged
    T_CIRCLE = 100  # 信息传输周期 s

    # forwarding cost value 的三个权重，它们和为1
    AERF = 0.1
    BETA = 0.3
    GAMA = 0.6

    # energy consumption model 的三个权重
    EIR = 0.3  # mj/bit, energy consumed by node i to receive one bit data
    EIS = 0.3  # mj/bit, energy consumed by node i to transmit one bit data
    EIG = 0.002  # mj/bit, energy consumed by node i to generate one bit data

    STANDARDLIST = [10000, 50000, 70000, 90000]

    def getDic():
        dic = {}
        dic["INF"] = Constants.INF
        dic["NUM_OF_NETWORKS"] = Constants.NUM_OF_NETWORKS
        dic["NUM_OF_NODES"] = Constants.NUM_OF_NODES
        dic["MAX_COMMUNICATE_RANGE"] = Constants.MAX_COMMUNICATE_RANGE
        dic["MAX_INFO_GENERATE_RATE"] = Constants.MAX_INFO_GENERATE_RATE
        dic["MIN_INFO_GENERATE_RATE"] = Constants.MIN_INFO_GENERATE_RATE
        dic["NODE_FULL_ENERGY"] = Constants.NODE_FULL_ENERGY
        dic["MC_FULL_ENERGY"] = Constants.MC_FULL_ENERGY
        dic["MC_MAX_MOVE_DISTANCE"] = Constants.MC_MAX_MOVE_DISTANCE
        dic["ROUND"] = Constants.ROUND
        dic["MC_SPEED"] = Constants.MC_SPEED
        dic["PRICE"] = Constants.PRICE
        dic["CHARINGSPEED"] = Constants.CHARINGSPEED
        dic["MCEV"] = Constants.MCEV
        dic["T"] = Constants.T
        dic["T_CIRCLE"] = Constants.T_CIRCLE
        dic["AERF"] = Constants.AERF
        dic["BETA"] = Constants.BETA
        dic["GAMA"] = Constants.GAMA
        dic["EIR"] = Constants.EIR
        dic["EIS"] = Constants.EIS
        dic["EIG"] = Constants.EIG
        dic["STANDARDLIST"] = Constants.STANDARDLIST
        return dic

    def setByDic(dic):
        Constants.INF = dic["INF"]
        Constants.NUM_OF_NETWORKS = dic["NUM_OF_NETWORKS"]
        Constants.NUM_OF_NODES = dic["NUM_OF_NODES"]
        Constants.MAX_COMMUNICATE_RANGE = dic["MAX_COMMUNICATE_RANGE"]
        Constants.MAX_INFO_GENERATE_RATE = dic["MAX_INFO_GENERATE_RATE"]
        Constants.MIN_INFO_GENERATE_RATE = dic["MIN_INFO_GENERATE_RATE"]
        Constants.NODE_FULL_ENERGY = dic["NODE_FULL_ENERGY"]
        Constants.MC_FULL_ENERGY = dic["MC_FULL_ENERGY"]
        Constants.MC_MAX_MOVE_DISTANCE = dic["MC_MAX_MOVE_DISTANCE"]
        Constants.ROUND = dic["ROUND"]
        Constants.MC_SPEED = dic["MC_SPEED"]
        Constants.PRICE = dic["PRICE"]
        Constants.CHARINGSPEED = dic["CHARINGSPEED"]
        Constants.MCEV = dic["MCEV"]
        Constants.T = dic["T"]
        Constants.T_CIRCLE = dic["T_CIRCLE"]
        Constants.AERF = dic["AERF"]
        Constants.BETA = dic["BETA"]
        Constants.GAMA = dic["GAMA"]
        Constants.EIR = dic["EIR"]
        Constants.EIS = dic["EIS"]
        Constants.EIG = dic["EIG"]
        Constants.STANDARDLIST = dic["STANDARDLIST"]
