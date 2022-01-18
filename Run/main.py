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

    desc = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + \
                                "NDsimu"
    
    map_dic, nodeR_dic = DataStore.simu(desc)

    energy, eff, nd_reec = REEC.chargeByREEC(Constants.NUM_OF_NODES, map_dic, nodeR_dic)
    
    energy, eff, nd_rebe = REBE.chargeByREBE(Constants.NUM_OF_NODES, map_dic, nodeR_dic)

    Visualization.X_ndratio_Y_time(nd_x, nd_reec, nd_rebe, desc)
    


if __name__ == '__main__':
    # NChange()
    NDSimu()
