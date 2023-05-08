# -*- coding: utf-8 -*-
"""
Analysis of the baseline values (moving average when HL index = 0) compared
with an increase in HL index.
Created: 13-04-2023
Python v3.9.5 (base: conda)
Author: M. ter Braak
"""
# %%
# Required modules
import pandas as pd

def analysis(list_par):
    '''
    Function to determine the mean per Heartlogic index
    '''

    # rename the columns of the created list
    list_par = pd.DataFrame(list_par, columns=['index', 'Height index', 'diff_value', 'diff_perc'])

    # Compute the mean per height of the heartlogic index
    mean_par = pd.DataFrame(list_par).groupby(['Height index'], as_index=False).mean().values.tolist()
    mean_par = pd.DataFrame(mean_par, columns=['Height index', 'index', 'diff_value', 'diff_perc'])
    mean_par = pd.DataFrame(mean_par[['Height index', 'diff_value', 'diff_perc']])
    return(mean_par)

    # append the output of the different patients
    # list_par_complete = pd.concat([list_par_complete, mean_par], axis=0)
    # return(list_par_complete)


def visualisation(diff_complete):
    '''
    Function to visualise the difference per parameter compared to baseline (Heartlogic index = 0) 
    with an increasing Heartlogic index.
    '''
    mean_par_complete = pd.DataFrame(diff_complete).groupby(['Height index'], as_index=False).mean().values.tolist()
    par_new = pd.DataFrame(mean_par_complete, columns=['Height index', 'diff_value', 'diff_perc'])
    par_new.plot.scatter(x=['Height index'], y=['diff_value'])
    # print(par_new['diff_perc'][15], par_new['diff_value'][15])  # To get the percentage difference at alarm stage (HL index =16)
    return(par_new)
# %%
