import os
import time
from matplotlib import pyplot as plt

targetpwd = os.getcwd() + "\\pic\\"
if not os.path.isdir(targetpwd):
    os.mkdir(targetpwd)


def X_N_Y_energy(x, y_other, y_our, t):
    plt.xlabel('Network Size (N)')
    plt.ylabel('Average residual energy (mJ)')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(targetpwd + t + "X_N_Y_energy", bbox_inches='tight')
    plt.show()


def X_N_Y_eff(x, y_other, y_our, t):
    plt.xlabel('Network Size (N)')
    plt.ylabel('Charging Efficiency')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(targetpwd + t + "X_N_Y_eff", bbox_inches='tight')
    plt.show()


def X_eff_Y_energy(x, y_other, y_our, t):
    plt.xlabel('MC maximum travel distance: L (m)')
    plt.ylabel('Average residual energy (mJ)')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(targetpwd + t + "X_eff_Y_energy", bbox_inches='tight')
    plt.show()


def X_eff_Y_eff(x, y_other, y_our, t):
    plt.xlabel('MC maximum travel distance: L (m)')
    plt.ylabel('Charging Efficiency')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(targetpwd + t + "X_eff_Y_eff", bbox_inches='tight')
    plt.show()


def X_B_Y_energy(x, y_other, y_our, t):
    plt.xlabel('MC maximum travel distance: L (m)')
    plt.ylabel('Average residual energy (mJ)')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(targetpwd + t + "X_B_Y_energy", bbox_inches='tight')
    plt.show()


def X_B_Y_eff(x, y_other, y_our, t):
    plt.xlabel('MC maximum travel distance: L (m)')
    plt.ylabel('Charging Efficiency')

    plt.plot(x, y_other, label='REEC', color='black', marker='D')
    plt.plot(x, y_our, label='REBE', color='black', marker='s')
    plt.legend()
    plt.savefig(targetpwd + t + "X_B_Y_eff", bbox_inches='tight')
    plt.show()


def test():
    x = [30, 50, 70, 100]
    y_other = [1037671.74, 560506.80, 489153.16, 521979.88]
    y_our = [1324049.60, 703185.69, 589055.76, 377469.17]
    t = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
    X_N_Y_energy(x, y_other, y_our, t)


if __name__ == '__main__':
    test()
