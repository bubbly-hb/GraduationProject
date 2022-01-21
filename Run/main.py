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
    
def NChangeNDSimu():
    nd_x = [1, 30, 50, 70]
    N_ls = [30, 50, 70, 100]
    nd_ls_reec = [[], [], [], []]
    nd_ls_rebe = [[], [], [], []]
    desc = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + \
                                    "NChangeNDSimu"
    DataStore.createNewFile(desc)
    DataStore.PWD = DataStore.PWD + desc + "\\"
    Visualization.PWD = Visualization.PWD + desc + "\\"
    for i in range(4):
        Constants.NUM_OF_NODES = N_ls[i]

        desc = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())) + \
                                    "NChangeNDSimu"
        
        map_dic, nodeR_dic = DataStore.simu(desc)

        energy, eff, nd_reec = REEC.chargeByREEC(Constants.NUM_OF_NODES, map_dic, nodeR_dic)
        
        energy, eff, nd_rebe = REBE.chargeByREBE(Constants.NUM_OF_NODES, map_dic, nodeR_dic)

        for j in range(4):
            nd_ls_reec[j].append(nd_reec[j])
            nd_ls_rebe[j].append(nd_rebe[j])

   
    for i in range(4):
        Visualization.X_N_Y_time(N_ls, nd_ls_reec[i], nd_ls_rebe[i], "percent" + str(nd_x[i]))

if __name__ == '__main__':
    # NChange()
    # NDSimu()
    NChangeNDSimu()
