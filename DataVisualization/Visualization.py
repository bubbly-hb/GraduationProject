import os
import time
from matplotlib import pyplot as plt

PWD = os.getcwd() + "\\data\\"


def X_N_Y_energy(x, y_other, y_our, desc):
    plt.xlabel('Network Size (N)')
    plt.ylabel('Average residual energy (mJ)')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(PWD + desc + "\\" + "X_N_Y_energy", bbox_inches='tight')
    plt.show()


def X_N_Y_eff(x, y_other, y_our, desc):
    plt.xlabel('Network Size (N)')
    plt.ylabel('Charging Efficiency')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(PWD + desc + "\\" + "X_N_Y_eff", bbox_inches='tight')
    plt.show()


def X_eff_Y_energy(x, y_other, y_our, desc):
    plt.xlabel('MC maximum travel distance: L (m)')
    plt.ylabel('Average residual energy (mJ)')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(PWD + desc + "\\" + "X_eff_Y_energy", bbox_inches='tight')
    plt.show()


def X_eff_Y_eff(x, y_other, y_our, desc):
    plt.xlabel('MC maximum travel distance: L (m)')
    plt.ylabel('Charging Efficiency')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(PWD + desc + "\\" + "X_eff_Y_eff", bbox_inches='tight')
    plt.show()


def X_B_Y_energy(x, y_other, y_our, desc):
    plt.xlabel('MC maximum travel distance: L (m)')
    plt.ylabel('Average residual energy (mJ)')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(PWD + desc + "\\" + "X_B_Y_energy", bbox_inches='tight')
    plt.show()


def X_B_Y_eff(x, y_other, y_our, desc):
    plt.xlabel('MC maximum travel distance: L (m)')
    plt.ylabel('Charging Efficiency')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(PWD + desc + "\\" + "X_B_Y_eff", bbox_inches='tight')
    plt.show()

def X_ndratio_Y_time(x, y_other, y_our, desc):
    plt.xlabel('node dead ratio (%)')
    plt.ylabel('time')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(PWD + desc + "\\" + "X_ndratio_Y_time", bbox_inches='tight')
    plt.show()

# 对于特定的nd ratio,不同网络大小下对应的出现时间
# 这里的savefig路径有变化，因为在main里已经改变了这个文件的PWD值
def X_N_Y_time(x, y_other, y_our, desc):
    plt.xlabel('Network Size (N)')
    plt.ylabel('time')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(PWD + desc + "X_N_Y_time", bbox_inches='tight')
    plt.show()

# 对于特定的nd ratio,不同L(可对应MC最大携能或者EFF)下对应的出现时间
# 这里的savefig路径有变化，因为在main里已经改变了这个文件的PWD值
def X_L_Y_time(x, y_other, y_our, desc):
    plt.xlabel('MC maximum travel distance: L (m)')
    plt.ylabel('time')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(PWD + desc + "X_L_Y_time", bbox_inches='tight')
    plt.show()



def test():
    x = [30, 50, 70, 100]
    y_other = [1037671.74, 560506.80, 489153.16, 521979.88]
    y_our = [1324049.60, 703185.69, 589055.76, 377469.17]
    t = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
    X_N_Y_energy(x, y_other, y_our, t)


if __name__ == '__main__':
    test()
