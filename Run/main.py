import sys
import time
import os

sys.path.append(os.getcwd())
sys.path.append(os.getcwd() + "\\DataVisualization")
import DataVisualization.DataStore as DataStore
import DataVisualization.Visualization as Visualization
from ChargingScheme.Constants import Constants
import ChargingScheme.SchemeComparative as REEC
import ChargingScheme.SchemeProposed as REBE


def NChange():
    currentTime = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
    N_ls = [30, 50, 70, 100]
    energy_ls_reec = []
    energy_ls_rebe = []
    eff_ls_reec = []
    eff_ls_rebe = []
    for i in N_ls:
        Constants.NUM_OF_NODES = i
        map_dic, nodeR_dic = DataStore.get("", "", Constants.NUM_OF_NODES, currentTime)

        # 根据历史数据跑时，避免当前网络数与历史数据网络数不一致
        key_count = 0
        for r_dic_key in map_dic:
            key_count += 1
        Constants.NUM_OF_NETWORKS = key_count

        energy, eff = REEC.chargeByREEC(Constants.NUM_OF_NODES, map_dic, nodeR_dic)
        energy_ls_reec.append(energy)
        eff_ls_reec.append(eff)

        energy, eff = REBE.chargeByREBE(Constants.NUM_OF_NODES, map_dic, nodeR_dic)
        energy_ls_rebe.append(energy)
        eff_ls_rebe.append(eff)

    Visualization.X_N_Y_energy(N_ls, energy_ls_reec, energy_ls_rebe, currentTime)
    Visualization.X_N_Y_eff(N_ls, eff_ls_reec, eff_ls_rebe, currentTime)


def NDSimu():
    nd_x = [1, 30, 50, 70]

    desc = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + "NDsimu"

    map_dic, nodeR_dic = DataStore.simu(desc)

    energy, eff, nd_reec = REEC.chargeByREEC(Constants.NUM_OF_NODES, map_dic, nodeR_dic)

    energy, eff, nd_rebe = REBE.chargeByREBE(Constants.NUM_OF_NODES, map_dic, nodeR_dic)

    Visualization.X_ndratio_Y_time(nd_x, nd_reec, nd_rebe, desc)


def NChangeNDSimu():
    nd_x = [1, 30, 50, 70]
    N_ls = [30, 50, 70, 100]
    nd_ls_reec = [[], [], [], []]
    nd_ls_rebe = [[], [], [], []]
    desc = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + "NChangeNDSimu"
    DataStore.createNewFile(desc)
    DataStore.PWD = DataStore.PWD + desc + "\\"
    Visualization.PWD = Visualization.PWD + desc + "\\"
    for i in range(4):
        Constants.NUM_OF_NODES = N_ls[i]

        desc = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + "NChangeNDSimu"

        map_dic, nodeR_dic = DataStore.simu(desc)

        energy, eff, nd_reec = REEC.chargeByREEC(Constants.NUM_OF_NODES, map_dic, nodeR_dic)

        energy, eff, nd_rebe = REBE.chargeByREBE(Constants.NUM_OF_NODES, map_dic, nodeR_dic)

        for j in range(4):
            nd_ls_reec[j].append(nd_reec[j])
            nd_ls_rebe[j].append(nd_rebe[j])

    for i in range(4):
        Visualization.X_N_Y_time(N_ls, nd_ls_reec[i], nd_ls_rebe[i], "percent" + str(nd_x[i]))


def MCFullEnergyChangeNDSimu():
    nd_x = [1, 30, 50, 70]
    mc_full_energy_ls = [300000000, 500000000, 700000000, 900000000]
    L_ls = []
    Constants.NUM_OF_NODES = 70
    Constants.MCEV = 500000
    nd_ls_reec = [[], [], [], []]
    nd_ls_rebe = [[], [], [], []]
    desc = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + "MCFullEnergyChangeNDSimu"
    DataStore.createNewFile(desc)
    DataStore.PWD = DataStore.PWD + desc + "\\"
    Visualization.PWD = Visualization.PWD + desc + "\\"
    for i in range(4):
        Constants.MC_FULL_ENERGY = mc_full_energy_ls[i]
        Constants.MC_MAX_MOVE_DISTANCE = (
            1 - Constants.EFF) * Constants.MC_FULL_ENERGY / Constants.MCEV
        L_ls.append(Constants.MC_MAX_MOVE_DISTANCE)
        desc = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + "MCFullEnergyChangeNDSimu"

        map_dic, nodeR_dic = DataStore.simu(desc)

        energy, eff, nd_reec = REEC.chargeByREEC(Constants.NUM_OF_NODES, map_dic, nodeR_dic)

        energy, eff, nd_rebe = REBE.chargeByREBE(Constants.NUM_OF_NODES, map_dic, nodeR_dic)

        for j in range(4):
            nd_ls_reec[j].append(nd_reec[j])
            nd_ls_rebe[j].append(nd_rebe[j])

    for i in range(4):
        Visualization.X_L_Y_time(L_ls, nd_ls_reec[i], nd_ls_rebe[i], "percent" + str(nd_x[i]))


def EFFChangeNDSimu():
    nd_x = [1, 30, 50, 70]
    eff_ls = [0.6, 0.5, 0.4, 0.3]
    L_ls = []
    Constants.NUM_OF_NODES = 70
    Constants.MCEV = 100000
    Constants.MC_FULL_ENERGY = 50000000
    nd_ls_reec = [[], [], [], []]
    nd_ls_rebe = [[], [], [], []]
    desc = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + "EFFChangeNDSimu"
    DataStore.createNewFile(desc)
    DataStore.PWD = DataStore.PWD + desc + "\\"
    Visualization.PWD = Visualization.PWD + desc + "\\"
    for i in range(4):
        Constants.EFF = eff_ls[i]
        Constants.MC_MAX_MOVE_DISTANCE = (
            1 - Constants.EFF) * Constants.MC_FULL_ENERGY / Constants.MCEV
        L_ls.append(Constants.MC_MAX_MOVE_DISTANCE)
        desc = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + "EFFChangeNDSimu"

        map_dic, nodeR_dic = DataStore.simu(desc)

        energy, eff, nd_reec = REEC.chargeByREEC(Constants.NUM_OF_NODES, map_dic, nodeR_dic)

        energy, eff, nd_rebe = REBE.chargeByREBE(Constants.NUM_OF_NODES, map_dic, nodeR_dic)

        for j in range(4):
            nd_ls_reec[j].append(nd_reec[j])
            nd_ls_rebe[j].append(nd_rebe[j])

    for i in range(4):
        Visualization.X_L_Y_time(L_ls, nd_ls_reec[i], nd_ls_rebe[i], "percent" + str(nd_x[i]))


if __name__ == '__main__':
    # NChange()
    # NDSimu()
    # NChangeNDSimu()
    MCFullEnergyChangeNDSimu()
    # EFFChangeNDSimu()
