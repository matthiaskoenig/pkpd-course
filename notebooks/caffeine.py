"""
Caffeine PKPD model definition.
"""
from __future__ import print_function, division
import numpy as np


def X0_caffeine():
    """ Returns the initial value array.
    
    :return: array of initial values
    :rtype: 
    """
    # ---------------------
    # Initial values
    # ---------------------
    x = np.empty([20])
    x[0] = 0    # global quantity 'A [mg] amount gut caffeine':ode
    x[1] = 0    # global quantity 'A [mg] amount kidney caffeine':ode
    x[2] = 0    # global quantity 'A [mg] amount liver caffeine':ode
    x[3] = 0    # global quantity 'A [mg] amount lung caffeine':ode
    x[4] = 0    # global quantity 'A [mg] amount spleen caffeine':ode
    x[5] = 0    # global quantity 'A [mg] amount rest caffeine':ode
    x[6] = 0    # global quantity 'A [mg] amount arterial blood caffeine':ode
    x[7] = 0    # global quantity 'A [mg] amount gut paraxanthine':ode
    x[8] = 0    # global quantity 'A [mg] amount kidney paraxanthine':ode
    x[9] = 0    # global quantity 'A [mg] amount liver paraxanthine':ode
    x[10] = 0   # global quantity 'A [mg] amount lung paraxanthine':ode
    x[11] = 0   # global quantity 'A [mg] amount spleen paraxanthine':ode
    x[12] = 0   # global quantity 'A [mg] amount rest paraxanthine':ode
    x[13] = 0   # global quantity 'A [mg] amount arterial blood paraxanthine':ode
    x[14] = 0   # global quantity 'A [mg] amount venous blood caffeine':ode
    x[15] = 100  # global quantity 'oral dose caffeine [mg]':ode
    x[16] = 0   # global quantity 'DCL_caf':ode
    x[17] = 0   # global quantity 'A [mg] amount venous blood paraxanthine':ode
    x[18] = 0   # global quantity 'oral dose paraxanthine [mg]':ode
    x[19] = 0   # global quantity 'DCL_px':ode
    return x


def dxdt_caffeine(x, t):
    """ Differential equation system for caffeine model.

    :param x: state vector
    :param t: time

    :return: differential equation system for odeint
    :rtype:
    """
    # --- Parameters ---
    p = np.empty(47)
    p[0] = 70  # global quantity 'body weight': fixed
    p[1] = 108.33  # global quantity 'cardiac output [ml/s]': fixed
    p[2] = 0.9049  # global quantity 'rest of body fractional tissue volume': fixed
    p[3] = 0.0171  # global quantity 'gut fractional tissue volume': fixed
    p[4] = 0.0044  # global quantity 'kidney fractional tissue volume': fixed
    p[5] = 0.021  # global quantity 'liver fractional tissue volume': fixed
    p[6] = 0.0076  # global quantity 'lung fractional tissue volume': fixed
    p[7] = 0.0026  # global quantity 'spleen fractional tissue volume': fixed
    p[8] = 0.0514  # global quantity 'venous fractional tissue volume': fixed
    p[9] = 0.0257  # global quantity 'arterial fractional tissue volume': fixed
    p[10] = 0.0424  # global quantity 'plasma fractional tissue volume': fixed
    p[11] = 0.146462  # global quantity 'gut fractional tissue blood flow': fixed
    p[12] = 0.19  # global quantity 'kidney fractional tissue blood flow': fixed
    p[13] = 0.215385  # global quantity 'hepatic (venous side) fractional tissue blood flow': fixed
    p[14] = 1  # global quantity 'lung fractional tissue blood flow': fixed
    p[15] = 0.017231  # global quantity 'spleen fractional tissue blood flow': fixed
    p[16] = 0.594615  # global quantity 'rest of body fractional tissue blood flow': fixed
    p[17] = 45  # global quantity 'mg microsomal protein per g liver': fixed
    p[18] = 1  # global quantity 'gut plasma partition coefficient caffeine': fixed
    p[19] = 1  # global quantity 'kidney plasma partition coefficient caffeine': fixed
    p[20] = 1  # global quantity 'liver plasma partition coefficient caffeine': fixed
    p[21] = 1  # global quantity 'lung plasma partition coefficient caffeine': fixed
    p[22] = 1  # global quantity 'spleen plasma partition coefficient caffeine': fixed
    p[23] = 0.5  # global quantity 'rest plasma partition coefficient caffeine': fixed
    p[24] = 1  # global quantity 'gut plasma partition coefficient paraxanthine': fixed
    p[25] = 1  # global quantity 'kidney plasma partition coefficient paraxanthine': fixed
    p[26] = 1  # global quantity 'liver plasma partition coefficient paraxanthine': fixed
    p[27] = 1  # global quantity 'lung plasma partition coefficient paraxanthine': fixed
    p[28] = 1  # global quantity 'spleen plasma partition coefficient paraxanthine': fixed
    p[29] = 0.5  # global quantity 'rest plasma partition coefficient paraxanthine': fixed
    p[30] = 0  # global quantity 'IV bolus dose caffeine [mg]': fixed
    p[31] = 100  # global quantity 'oral bolus dose caffeine [mg]': fixed
    p[32] = 0  # global quantity 'IV bolus dose paraxanthine [mg]': fixed
    p[33] = 0  # global quantity 'oral bolus dose paraxanthine [mg]': fixed
    p[34] = 2.5  # global quantity 'Ka [1/hr] absorption caffeine': fixed
    p[35] = 1  # global quantity 'fraction absorbed caffeine': fixed
    p[36] = 1  # global quantity 'fraction absorbed paraxanthine': fixed
    p[37] = 1  # global quantity 'fraction unbound in plasma caffeine': fixed
    p[38] = 1  # global quantity 'blood to plasma ratio caffeine': fixed
    p[39] = 1  # global quantity 'fraction unbound in microsomes caffeine': fixed
    p[40] = 1  # global quantity 'fraction unbound in plasma paraxanthine': fixed
    p[41] = 1  # global quantity 'blood to plasma ratio paraxanthine': fixed
    p[42] = 1  # global quantity 'fraction unbound in microsomes paraxanthine': fixed
    p[43] = 2  # global quantity 'HLM apparent clearance caffeine by hepatic microsomes [mul/min/mg]': fixed
    p[44] = 1.5  # global quantity 'relative clearance of px to caf': fixed
    p[45] = 0  # global quantity 'renal clearance [L/hr] caffeine': fixed
    p[46] = 0  # global quantity 'renal clearance [L/hr] paraxanthine': fixed

    # --- assignments ---
    y = np.empty(53)
    y[11] = p[1] / 1000.00000000000000000 * 3600.00000000000000000  # model entity 'cardiac output [L/hr]': assignment
    y[12] = p[34]  # model entity 'Ka [1/hr] absorption paraxanthine': assignment
    y[13] = p[44] * p[43]  # model entity 'HLM apparent clearance paraxanthine by hepatic microsomes [mul/min/mg]': assignment
    y[14] = y[11] * p[11]  # model entity 'gut blood flow': assignment
    y[15] = y[11] * p[12]  # model entity 'kidney blood flow': assignment
    y[16] = y[11] * p[13]  # model entity 'hepatic (venous side) blood flow': assignment
    y[17] = y[16] - y[14] - y[19]  # model entity 'hepatic artery blood flow': assignment
    y[18] = y[11] * p[14]  # model entity 'lung blood flow': assignment
    y[19] = y[11] * p[15]  # model entity 'spleen blood flow': assignment
    y[20] = y[11] * p[16]  # model entity 'rest of body blood flow': assignment
    y[21] = x[0] / y[1]  # model entity 'C caffeine [mg/l] gut': assignment
    y[22] = x[1] / y[2]  # model entity 'C caffeine [mg/l] kidney': assignment
    y[23] = x[2] / y[3]  # model entity 'C caffeine [mg/l] liver': assignment
    y[24] = x[3] / y[4]  # model entity 'C caffeine [mg/l] lung': assignment
    y[25] = x[4] / y[5]  # model entity 'C caffeine [mg/l] spleen': assignment
    y[26] = x[5] / y[0]  # model entity 'C caffeine [mg/l] rest of body': assignment
    y[27] = x[14] / y[6]  # model entity 'C caffeine [mg/l] venous blood': assignment
    y[28] = x[6] / y[7]  # model entity 'C caffeine [mg/l] arterial blood': assignment
    y[29] = x[7] / y[1]  # model entity 'C paraxanthine [mg/l] gut': assignment
    y[30] = x[8] / y[2]  # model entity 'C paraxanthine [mg/l] kidney': assignment
    y[31] = x[9] / y[3]  # model entity 'C paraxanthine [mg/l] liver': assignment
    y[32] = x[10] / y[4]  # model entity 'C paraxanthine [mg/l] lung': assignment
    y[33] = x[11] / y[5]  # model entity 'C paraxanthine [mg/l] spleen': assignment
    y[34] = x[12] / y[0]  # model entity 'C paraxanthine [mg/l] rest of body': assignment
    y[35] = x[17] / y[6]  # model entity 'C paraxanthine [mg/l] venous blood': assignment
    y[36] = x[13] / y[7]  # model entity 'C paraxanthine [mg/l] arterial blood': assignment
    y[37] = y[27] / p[38]  # model entity 'venous plasma concentration caffeine': assignment
    y[38] = y[23] * p[37]  # model entity 'free liver concentration caffeine': assignment
    y[39] = y[22] * p[37]  # model entity 'free kidney concentration caffeine': assignment
    y[40] = p[43] / p[39] * p[17] * y[3] * 60.00000000000000000 / 1000.00000000000000000  # model entity 'liver clearance caffeine [l/hr]': assignment
    y[41] = y[38] * y[40]  # model entity 'rate of caffeine change [l/hr]': assignment
    y[42] = y[35] / p[41]  # model entity 'venous plasma concentration paraxanthine': assignment
    y[43] = y[31] * p[40]  # model entity 'free liver concentration paraxanthine': assignment
    y[44] = y[30] * p[40]  # model entity 'free kidney concentration paraxanthine': assignment
    y[45] = y[13] / p[42] * p[17] * y[3] * 60.00000000000000000 / 1000.00000000000000000  # model entity 'liver clearance paraxanthine [l/hr]': assignment
    y[46] = y[43] * y[45]  # model entity 'rate of paraxanthine change [l/hr]': assignment
    y[47] = p[34] * x[15] * p[35]  # model entity 'caffeine absorption': assignment
    y[48] = y[15] * (y[22] / p[19]) * p[38] + y[16] * (y[23] / p[20]) * p[38] + y[20] * (y[26] / p[23]) * p[38]  # model entity 'Venous_caf': assignment
    y[49] = y[12] * x[18] * p[36]  # model entity 'paraxanthine absorption': assignment
    y[50] = y[15] * (y[30] / p[25]) * p[41] + y[16] * (y[31] / p[26]) * p[41] + y[20] * (y[34] / p[29]) * p[41]  # model entity 'Venous_px': assignment
    y[51] = x[6] + x[0] + x[1] + x[2] + x[3] + x[4] + x[5] + x[14]  # model entity 'Abody_caf': assignment
    y[52] = x[13] + x[7] + x[8] + x[9] + x[10] + x[11] + x[12] + x[17]  # model entity 'Abody_px': assignment
    y[0] = p[0] * p[2]  # model entity 'rest of body': assignment
    y[1] = p[0] * p[3]  # model entity 'gut': assignment
    y[2] = p[0] * p[4]  # model entity 'kidney': assignment
    y[3] = p[0] * p[5]  # model entity 'liver': assignment
    y[4] = p[0] * p[6]  # model entity 'lung': assignment
    y[5] = p[0] * p[7]  # model entity 'spleen': assignment
    y[6] = p[0] * p[8]  # model entity 'venous blood': assignment
    y[7] = p[0] * p[9]  # model entity 'arterial blood': assignment
    y[8] = p[0] * p[10]  # model entity 'plasma': assignment
    y[9] = y[8] * y[6] / (y[6] + y[7])  # model entity 'venous plasma': assignment
    y[10] = y[8] * y[7] / (y[6] + y[7])  # model entity 'arterial plasma': assignment

    # --- ode ---
    dx = np.empty(20)
    dx[0] = y[47] + y[14] * (y[28] - y[21] / p[18] * p[38])    # model entity 'A [mg] amount gut caffeine': ode
    dx[1] = y[15] * (y[28] - y[22] / p[19] * p[38]) - p[45] * y[39]    # model entity 'A [mg] amount kidney caffeine': ode
    dx[2] = y[17] * y[28] + y[14] * (y[21] / p[18]) * p[38] + y[19] * (y[25] / p[22]) * p[38] - y[16] * (
    y[23] / p[20]) * p[38] - y[41]    # model entity 'A [mg] amount liver caffeine': ode
    dx[3] = y[18] * y[27] - y[18] * (y[24] / p[21]) * p[38]    # model entity 'A [mg] amount lung caffeine': ode
    dx[4] = y[19] * (y[28] - y[25] / p[22] * p[38])    # model entity 'A [mg] amount spleen caffeine': ode
    dx[5] = y[20] * (y[28] - y[26] / p[23] * p[38])    # model entity 'A [mg] amount rest caffeine': ode
    dx[6] = y[18] * (y[24] / p[21]) * p[38] - y[18] * y[28]    # model entity 'A [mg] amount arterial blood caffeine': ode
    dx[7] = y[49] + y[14] * (y[36] - y[29] / p[24] * p[41])    # model entity 'A [mg] amount gut paraxanthine': ode
    dx[8] = y[15] * (y[36] - y[30] / p[25] * p[41]) - p[46] * y[44]    # model entity 'A [mg] amount kidney paraxanthine': ode
    dx[9] = y[17] * y[36] + y[14] * (y[29] / p[24]) * p[41] + y[19] * (y[33] / p[28]) * p[41] - y[16] * (
    y[31] / p[26]) * p[41] + y[41] - y[46]    # model entity 'A [mg] amount liver paraxanthine': ode
    dx[10] = y[18] * y[35] - y[18] * (y[32] / p[27]) * p[41]    # model entity 'A [mg] amount lung paraxanthine': ode
    dx[11] = y[19] * (y[36] - y[33] / p[28] * p[41])    # model entity 'A [mg] amount spleen paraxanthine': ode
    dx[12] = y[20] * (y[36] - y[34] / p[29] * p[41])    # model entity 'A [mg] amount rest paraxanthine': ode
    dx[13] = y[18] * (y[32] / p[27]) * p[41] - y[18] * y[36]    # model entity 'A [mg] amount arterial blood paraxanthine': ode
    dx[14] = y[48] - y[18] * y[27]    # model entity 'A [mg] amount venous blood caffeine': ode
    dx[15] = (-y[47])    # model entity 'oral dose caffeine [mg]': ode
    dx[16] = p[45] * y[39] + y[38] * y[40]    # model entity 'DCL_caf': ode
    dx[17] = y[50] - y[18] * y[35]    # model entity 'A [mg] amount venous blood paraxanthine': ode
    dx[18] = (-y[49])    # model entity 'oral dose paraxanthine [mg]': ode
    dx[19] = p[46] * y[44] - y[46]    # model entity 'DCL_px': ode

    return dx


def test_caffeine():
    """ Testing the ode integration of the caffeine model.

    Simulation of a 100 [mg] oral caffeine dose.

    :return:
    :rtype:
    """
    from matplotlib import pylab as plt
    from scipy.integrate import odeint
    print('*** test caffeine ***')
    T = np.arange(0, 24, 0.1)
    X0 = X0_caffeine()
    dxdt = dxdt_caffeine
    X = odeint(dxdt_caffeine, X0, T)
    plt.plot(T, X, linewidth=2)
    plt.show()


if __name__ == "__main__":
    test_caffeine()