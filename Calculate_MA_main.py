# -*- coding: utf-8 -*-
"""
Moving average of the parameters used for computing of Heartlogic index
Created: 29-03-2023
Python v3.9.5 (base: conda)
Author: M. ter Braak
"""
# %%
# Required modules
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import Counter

# Required functions
from pol_fit import pol_fit
import MA_analysis

# Create empty dataframe to store output of all parameters
diff_S3_complete = pd.DataFrame()
diff_S1_complete = pd.DataFrame()
diff_impedance_complete = pd.DataFrame()
diff_RR_complete = pd.DataFrame()
diff_NHR_complete = pd.DataFrame()
diff_sleep_inc_complete = pd.DataFrame()
diff_weight_complete = pd.DataFrame()
diff_SBP_complete = pd.DataFrame()
diff_DBP_complete = pd.DataFrame()
diff_mean_HR_complete = pd.DataFrame()
diff_HRV_complete = pd.DataFrame()
diff_act_lev_complete = pd.DataFrame()

# bas_S3_complete = pd.DataFrame()
# bas_S1_complete = pd.DataFrame()
# bas_impedance_complete = pd.DataFrame()
# bas_RR_complete = pd.DataFrame()
# bas_NHR_complete = pd.DataFrame()
# bas_sleep_inc_complete = pd.DataFrame()
# bas_weight_complete = pd.DataFrame()
# bas_SBP_complete = pd.DataFrame()
# bas_DBP_complete = pd.DataFrame()
# bas_mean_HR_complete = pd.DataFrame()
# bas_HRV_complete = pd.DataFrame()
# bas_act_lev_complete = pd.DataFrame()

# %%
# Current directory should be changed to the folder with your patient (xlsx) files.
os.chdir("C:/Users/milou/Documents/Master/TM2 - Stage 3/Heartlogic_patienten/Patienten")  # change your current directory
for files in os.listdir("C:/Users/milou/Documents/Master/TM2 - Stage 3/Heartlogic_patienten/Patienten"):  # folder with the xlsx files
    hl_parameters = pd.read_excel(files)
    # print(files)
    # rename parameter headings for further use
    hl_parameters.rename(columns={'HeartLogic Heart Failure Index': 'hl_index', 'HeartLogic-index voor hartfalen': 'hl_index',
                                  'Date': 'date',
                                  'S3 (mG)': 'S3',
                                  'S1 (mG)': 'S1',
                                  'Thoracic Impedance (Ω)': 'impedance', 'Thoracale impedantie (Ω)': 'impedance',
                                  'Respiratory Rate (min⁻¹)': 'RR', 'Respiratiefreq. (min⁻¹)': 'RR',
                                  'Night Heart Rate (min⁻¹)': 'NHR', 'Hartfrequentie ´s nachts (min⁻¹)': 'NHR',
                                  'Sleep Incline (degrees)': 'sleep_inc', 'Stijging tijdens slaap (graden)': 'sleep_inc',
                                  'Weight (kg)': 'weight', 'Gewicht (kg)': 'weight',
                                  'Systolic': 'SBP', 'Systolische bloeddruk': 'SBP',
                                  'Diastolic': 'DBP', 'Diastolische bloeddruk': 'DBP',
                                  'Mean Heart Rate (min⁻¹)': 'mean_HR', 'Gemiddelde hartfrequentie (min⁻¹)': 'mean_HR',
                                  'Heart Rate Variability (SDANN) (ms)': 'HRV', 'Heart Rate Variability (SDANN) (ms)': 'HRV',
                                  'Activ.niveau (uur (uren))': 'act_lev',
                                  'Activity Level (hour(s))': 'act_lev'}, inplace=True)

    hl_parameters = hl_parameters.set_index('date')
 
    # Changing all N/R (not reported), N.G./N.G (niet geraporteerd) to Nan
    hl_parameters.replace('N/R', np.nan, inplace=True)
    hl_parameters.replace('N.G.', np.nan, inplace=True)
    hl_parameters.replace('N.G', np.nan, inplace=True)

    # visualising the HL index over time
    # plt.style.use('seaborn')
    # hl_parameters.plot(y='hl_index')
    # plt.ylim([-0.5, 30])
    # plt.title('Heartlogic index of a patient')

    # Rolling average per parameter
    # Is only calculated when the index is 0. Window size is set to 5 periods (days). Minimum of 3 windows (days) is needed.
    cols = ['S3', 'S1', 'impedance', 'RR', 'NHR', 'sleep_inc', 'weight', 'SBP', 'DBP', 'mean_HR', 'HRV', 'act_lev']
    not_na_values = pd.DataFrame()
    for col in cols:
        hl_parameters[f'{col}'] = hl_parameters[f'{col}'].astype(float)
        hl_parameters[f'MA_{col}_5'] = np.where(hl_parameters['hl_index'] == 0, hl_parameters[col].rolling(5, min_periods=1).mean(), np.nan)

    hl_parameters['ratio_S3S1'] = hl_parameters['S3']/hl_parameters['S1']
    hl_parameters['MA_ratio_S3S1_5'] = np.where(hl_parameters['hl_index'] == 0, hl_parameters['ratio_S3S1'].rolling(5, min_periods=3).mean(), np.nan)

    # Find the differences with baseline
    bas_S3, bas_S1, bas_impedance, bas_RR, bas_NHR, bas_sleep_inc, bas_weight, bas_SBP, bas_DBP, bas_mean_HR, bas_HRV, bas_act_lev  = [], [], [], [], [], [], [], [], [], [], [], []
    diff_S3, diff_S1, diff_impedance, diff_RR, diff_NHR, diff_sleep_inc, diff_weight, diff_SBP, diff_DBP, diff_mean_HR, diff_HRV, diff_act_lev = [], [], [], [], [], [], [], [], [], [], [], []
    prev_value = 0

    # To determine what the average value is when the HL index is 0
    '''
    This part is only used to determine what the overall baseline value is taken into account all value when HL index = 0.
    '''
    # for idx, value in enumerate(hl_parameters['hl_index']):
    #     if value == 0:
    #         bas_S3_val = hl_parameters['S3'][idx]
    #         bas_S3.append(bas_S3_val)
    #         bas_S1_val = hl_parameters['S1'][idx]
    #         bas_S1.append(bas_S1_val)
    #         bas_impedance_val = hl_parameters['impedance'][idx]
    #         bas_impedance.append(bas_impedance_val)
    #         bas_RR_val = hl_parameters['RR'][idx]
    #         bas_RR.append(bas_RR_val)
    #         bas_NHR_val = hl_parameters['NHR'][idx]
    #         bas_NHR.append(bas_NHR_val)
    #         bas_sleep_inc_val = hl_parameters['sleep_inc'][idx]
    #         bas_sleep_inc.append(bas_sleep_inc_val)
    #         bas_SBP_val = hl_parameters['SBP'][idx]
    #         bas_SBP.append(bas_SBP_val)
    #         bas_DBP_val = hl_parameters['DBP'][idx]
    #         bas_DBP.append(bas_DBP_val)
    #         bas_mean_HR_val = hl_parameters['mean_HR'][idx]
    #         bas_mean_HR.append(bas_mean_HR_val)
    #         bas_HRV_val = hl_parameters['HRV'][idx]
    #         bas_HRV.append(bas_HRV_val)
    #         bas_act_lev_val = hl_parameters['act_lev'][idx]
    #         bas_act_lev.append(bas_act_lev_val)

    # bas_S3_complete = pd.concat([bas_S3_complete, pd.Series(np.mean(bas_S3)).to_frame()], ignore_index=True)
    # mean_bas_S3 = np.mean(bas_S3_complete)
    # bas_S1_complete = pd.concat([bas_S1_complete, pd.Series(np.mean(bas_S1)).to_frame()], ignore_index=True)
    # mean_bas_S1 = np.mean(bas_S1_complete)
    # bas_impedance_complete = pd.concat([bas_impedance_complete, pd.Series(np.mean(bas_impedance)).to_frame()], ignore_index=True)
    # mean_bas_impedance = np.mean(bas_impedance_complete)
    # bas_RR_complete = pd.concat([bas_RR_complete, pd.Series(np.mean(bas_RR)).to_frame()], ignore_index=True)
    # mean_bas_RR = np.mean(bas_RR_complete)
    # bas_NHR_complete = pd.concat([bas_NHR_complete, pd.Series(np.mean(bas_NHR)).to_frame()], ignore_index=True)
    # mean_bas_NHR = np.mean(bas_NHR_complete)
    # bas_sleep_inc_complete = pd.concat([bas_sleep_inc_complete, pd.Series(np.mean(bas_sleep_inc)).to_frame()], ignore_index=True)
    # mean_bas_sleep_inc = np.mean(bas_sleep_inc_complete)
    # bas_weight_complete = pd.concat([bas_weight_complete, pd.Series(np.mean(bas_weight)).to_frame()], ignore_index=True)
    # mean_bas_weight = np.mean(bas_weight_complete)
    # bas_SBP_complete = pd.concat([bas_SBP_complete, pd.Series(np.mean(bas_SBP)).to_frame()], ignore_index=True)
    # mean_bas_SBP = np.mean(bas_SBP_complete)
    # bas_DBP_complete = pd.concat([bas_DBP_complete, pd.Series(np.mean(bas_DBP)).to_frame()], ignore_index=True)
    # mean_bas_DBP = np.mean(bas_DBP_complete)
    # bas_mean_HR_complete = pd.concat([bas_mean_HR_complete, pd.Series(np.mean(bas_mean_HR)).to_frame()], ignore_index=True)
    # mean_bas_mean_HR = np.mean(bas_mean_HR_complete)
    # bas_HRV_complete = pd.concat([bas_HRV_complete, pd.Series(np.mean(bas_HRV)).to_frame()], ignore_index=True)
    # mean_bas_HRV = np.mean(bas_HRV_complete)
    # bas_act_lev_complete = pd.concat([bas_act_lev_complete, pd.Series(np.mean(bas_act_lev)).to_frame()], ignore_index=True)
    # mean_bas_act_lev = np.mean(bas_act_lev_complete)

    '''
    The next part is used to determine the difference with baseline.
    It uses the last moving average (when HL index = 0) to compare with.
    Each index higher than 0 is analysed. 
    '''

    for idx, value in enumerate(hl_parameters['hl_index']):
        if (value > prev_value) or ((prev_value > 0 and value > 0)):  # first statement for increasing HL index, second for HL index > 0
            if prev_value == 0:  # When the previous hl_index = 0, save the index as baseline value
                bas = idx-1
            diff_S3_val = hl_parameters['S3'][idx] - hl_parameters['MA_S3_5'][bas]
            perc_S3 = (diff_S3_val / hl_parameters['MA_S3_5'][bas]) * 100
            diff_S3.append((idx, value, diff_S3_val, perc_S3))
            diff_S1_val = hl_parameters['ratio_S3S1'][idx] - hl_parameters['MA_ratio_S3S1_5'][bas]
            perc_S1 = (diff_S1_val / hl_parameters['MA_S1_5'][bas]) * 100
            diff_S1.append((idx, value, diff_S1_val, perc_S1))
            diff_impedance_val = hl_parameters['impedance'][idx] - hl_parameters['MA_impedance_5'][bas]
            perc_impedance = (diff_impedance_val / hl_parameters['MA_impedance_5'][bas]) * 100
            diff_impedance.append((idx, value, diff_impedance_val, perc_impedance))
            diff_RR_val = hl_parameters['RR'][idx] - hl_parameters['MA_RR_5'][bas]
            perc_RR = (diff_RR_val / hl_parameters['MA_RR_5'][bas]) * 100
            diff_RR.append((idx, value, diff_RR_val, perc_RR))
            diff_NHR_val = hl_parameters['NHR'][idx] - hl_parameters['MA_NHR_5'][bas]
            perc_NHR = (diff_NHR_val / hl_parameters['MA_NHR_5'][bas]) * 100
            diff_NHR.append((idx, value, diff_NHR_val, perc_NHR))
            diff_sleep_inc_val = hl_parameters['sleep_inc'][idx] - hl_parameters['MA_sleep_inc_5'][bas]
            perc_sleep_inc = (diff_sleep_inc_val / hl_parameters['MA_sleep_inc_5'][bas]) * 100
            diff_sleep_inc.append((idx, value, diff_sleep_inc_val, perc_sleep_inc))
            diff_weight_val = hl_parameters['weight'][idx] - hl_parameters['MA_weight_5'][bas]
            perc_weight = (diff_weight_val / hl_parameters['MA_weight_5'][bas]) * 100
            diff_weight.append((idx, value, diff_weight_val, perc_weight))
            diff_SBP_val = hl_parameters['SBP'][idx] - hl_parameters['MA_SBP_5'][bas]
            perc_SBP = (diff_SBP_val / hl_parameters['MA_SBP_5'][bas]) * 100
            diff_SBP.append((idx, value, diff_SBP_val, perc_SBP))
            diff_DBP_val = hl_parameters['DBP'][idx] - hl_parameters['MA_DBP_5'][bas]
            perc_DBP = (diff_DBP_val / hl_parameters['MA_DBP_5'][bas]) * 100
            diff_DBP.append((idx, value, diff_DBP_val, perc_DBP))
            diff_mean_HR_val = hl_parameters['mean_HR'][idx] - hl_parameters['MA_mean_HR_5'][bas]
            perc_mean_HR = (diff_mean_HR_val / hl_parameters['MA_mean_HR_5'][bas]) * 100
            diff_mean_HR.append((idx, value, diff_mean_HR_val, perc_mean_HR))
            diff_HRV_val = hl_parameters['HRV'][idx] - hl_parameters['MA_HRV_5'][bas]
            perc_HRV = (diff_HRV_val / hl_parameters['MA_HRV_5'][bas]) * 100
            diff_HRV.append((idx, value, diff_HRV_val, perc_HRV))
            diff_act_val = hl_parameters['act_lev'][idx] - hl_parameters['MA_act_lev_5'][bas]
            perc_act_lev = (diff_act_val / hl_parameters['MA_act_lev_5'][bas]) * 100
            diff_act_lev.append((idx, value, diff_act_val, perc_act_lev))
        prev_value = value

    mean_S3 = MA_analysis.analysis(diff_S3)
    mean_S1 = MA_analysis.analysis(diff_S1)
    mean_impedance = MA_analysis.analysis(diff_impedance)
    mean_RR = MA_analysis.analysis(diff_RR)
    mean_NHR = MA_analysis.analysis(diff_NHR)
    mean_sleep_inc = MA_analysis.analysis(diff_sleep_inc)
    mean_weight = MA_analysis.analysis(diff_weight)
    mean_SBP = MA_analysis.analysis(diff_SBP)
    mean_DBP = MA_analysis.analysis(diff_DBP)
    mean_mean_HR = MA_analysis.analysis(diff_mean_HR)
    mean_HRV = MA_analysis.analysis(diff_HRV)
    mean_act_lev = MA_analysis.analysis(diff_act_lev)

    # append the output of the different patients
    diff_S3_complete = pd.concat([diff_S3_complete, mean_S3], axis=0)
    diff_S1_complete = pd.concat([diff_S1_complete, mean_S1], axis=0)
    diff_impedance_complete = pd.concat([diff_impedance_complete, mean_impedance], axis=0)
    diff_RR_complete = pd.concat([diff_RR_complete, mean_RR], axis=0)
    diff_NHR_complete = pd.concat([diff_NHR_complete, mean_NHR], axis=0)
    diff_sleep_inc_complete = pd.concat([diff_sleep_inc_complete, mean_sleep_inc], axis=0)
    diff_weight_complete = pd.concat([diff_weight_complete, mean_weight], axis=0)
    diff_SBP_complete = pd.concat([diff_SBP_complete, mean_SBP], axis=0)
    diff_DBP_complete = pd.concat([diff_DBP_complete, mean_DBP], axis=0)
    diff_mean_HR_complete = pd.concat([diff_mean_HR_complete, mean_mean_HR], axis=0)
    diff_HRV_complete = pd.concat([diff_HRV_complete, mean_HRV], axis=0)
    diff_act_lev_complete = pd.concat([diff_act_lev_complete, mean_act_lev], axis=0)


new_S3 = MA_analysis.visualisation(diff_S3_complete)
plt.title('S3 mean differences')
new_S1 = MA_analysis.visualisation(diff_S1_complete)
plt.title('S1 mean differences')
new_impedance = MA_analysis.visualisation(diff_impedance_complete)
plt.title('Impedance mean differences')
new_RR = MA_analysis.visualisation(diff_RR_complete)
plt.title('RR mean differences')
new_NHR = MA_analysis.visualisation(diff_NHR_complete)
plt.title('NHR mean differences')
new_sleep_inc = MA_analysis.visualisation(diff_sleep_inc_complete)
plt.title('Sleep incline mean differences')
new_weight = MA_analysis.visualisation(diff_weight_complete)
plt.title('Weight mean differences')
new_SBP = MA_analysis.visualisation(diff_SBP_complete)
plt.title('SBP mean differences')
new_DBP = MA_analysis.visualisation(diff_DBP_complete)
plt.title('DBP mean differences')
new_mean_HR = MA_analysis.visualisation(diff_mean_HR_complete)
plt.title('Mean HR mean differences')
new_HRV = MA_analysis.visualisation(diff_HRV_complete)
plt.title('HRV mean differences')
new_act_lev = MA_analysis.visualisation(diff_act_lev_complete)
plt.title('Activity level mean differences')

# %% To calculate the correlations of the first, second and third degree polynomial
variables = ['S3', 'S1', 'impedance', 'RR', 'NHR', 'sleep_inc', 'weight', 'SBP', 'DBP', 'mean_HR', 'HRV', 'act_lev']
corr_coef_dict = {}

for var in variables:
    corr_coef_1, corr_coef_2, corr_coef_3 = pol_fit(globals()['new_' + var])
    corr_coef_dict[var] = (corr_coef_1, corr_coef_2, corr_coef_3)


# %% To count the amount a index occured in the patient

amount = Counter(diff_S3_complete['Height index'])
print(amount)

plt.hist(diff_S3_complete['Height index'])
plt.show()
# %%
