# -*- coding: utf-8 -*-
"""
Polynomial fit on the different parameters for the Heartlogic index
Created: 13-04-2023
Python v3.9.5 (base: conda)
Author: M. ter Braak
"""
# %%
# Required modules
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
from matplotlib.ticker import MaxNLocator


def pol_fit(list_par):
    '''
    Function to fit different degrees (1,2,3) polynomials on
    the parameters associated with the Heartlogic index

    Input:
    List of the parameter with the height of the heartlogic index and the
    corresponding difference in value compared to baseline (Heartlogic index = 0).
    Cannot contain any Nan.

    '''
    y_actual = list_par['diff_value'][0:21]
    list_par = list_par.dropna()
    x = list_par['Height index'][0:21]  # Heartlogic index is set to 21, since higher indeces have a big influence on the fit
    y = list_par['diff_value'][0:21]

    # first order - linear function
    coeffs = np.polyfit(x, y, deg=1)
    a = coeffs[0]
    b = coeffs[1]
    fit_equation_1 = a*x + b
    print(f'coefficients first deg a ={a}, b={b}')
    # Computing residuals
    pol_fun_1 = np.poly1d(coeffs)
    y_pred_1 = pol_fun_1(x)
    residuals_1 = y - y_pred_1
    ## Alarm value (HL index = 16)
    # y_pred = pol_fun_1(16)
    # print(f'actual value = {y_actual[15]}, predicted = {y_pred}')

    # second order - quadratic function
    coeffs = np.polyfit(x, y, deg=2)
    a = coeffs[0]
    b = coeffs[1]
    c = coeffs[2]
    fit_equation_2 = a*np.square(x) + b*x + c
    print(f'coefficients second deg a={a}, b={b}, c={c}')
    # Computing residuals
    pol_fun_2 = np.poly1d(coeffs)
    y_pred_2 = pol_fun_2(x)
    residuals_2 = y - y_pred_2
    ## Alarm value (HL index = 16)
    # y_pred = pol_fun_2(16)
    # print(f'actual value = {y_actual[15]}, predicted = {y_pred}')

    # third order - cubic function
    coeffs = np.polyfit(x, y, deg=3)
    a = coeffs[0]
    b = coeffs[1]
    c = coeffs[2]
    d = coeffs[3]
    fit_equation_3 = a * x**3 + b * x**2 + c * x + d
    print(f'coefficients third deg a={a}, b={b}, c={c}, d={d}')
    # Computing residuals
    pol_fun_3 = np.poly1d(coeffs)
    y_pred_3 = pol_fun_3(x)
    residuals_3 = y - y_pred_3
    # # Alarm value (HL index = 16)
    # y_pred = pol_fun_3(16)
    # print(f'actual value = {y_actual[15]}, predicted = {y_pred}')

    # Plot with the three different orders polynomial
    fig1 = plt.figure()
    ax1 = fig1.subplots()
    ax1.plot(x, fit_equation_1, label='1st deg')
    ax1.plot(x, fit_equation_2, label='2nd deg')
    ax1.plot(x, fit_equation_3, label='3rd deg')
    ax1.scatter(x, y, s=5, label='Data points')
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel('Heartlogic index')
    plt.legend()
    plt.show()

    # Plot with the residuals of the three different orders
    fig2 = plt.figure()
    ax2 = fig2.subplots()
    ax2.scatter(x, residuals_1, marker='.', label='1st deg')
    ax2.scatter(x, residuals_2, marker='.', label='2nd deg')
    ax2.scatter(x, residuals_3, marker='.', label='3rd deg')
    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel('Heartlogic index')
    plt.legend()
    plt.show()

    corr_coef_1 = pearsonr(y, fit_equation_1)
    corr_coef_2 = pearsonr(y, fit_equation_2)
    corr_coef_3 = pearsonr(y, fit_equation_3)
    print(corr_coef_1, corr_coef_2, corr_coef_3)
    return corr_coef_1, corr_coef_2, corr_coef_3
# %%
