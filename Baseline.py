# -*- coding: utf-8 -*-
"""
Analysis of patient characteristics
Created: 25-04-2023
Python v3.9.5 (base: conda)
Author: M. ter Braak
"""
# %%
# Required modules
import pandas as pd
import os
import matplotlib.pyplot as plt

# Current directory should be changed to the folder with the baseline characteristics
os.chdir("C:/Users/milou/Documents/Master/TM2 - Stage 3")  # change your current directory
pat_carac = pd.read_csv('Baseline_Data_Milou.csv', sep=';')  # load file with baseline characterisics

pat_carac.describe()

# %% Continuous variables
# Histogram to check for normality
plt.hist(pat_carac['Age'])
plt.show()

plt.hist(pat_carac['BMI'])
plt.show()
# %% Categorical variables
df_carac = pd.DataFrame()

# NYHA class
df_carac['nyha_class'] = pat_carac['NYHAClass'].value_counts()
df_carac['perc_nyhaclass'] = (df_carac['nyha_class']/df_carac['nyha_class'].sum())*100

# Gender
df_carac['gender'] = pat_carac['Gender'].value_counts()
df_carac['perc_gender'] = (df_carac['gender']/df_carac['gender'].sum())*100

# Type of device
df_carac['type_CIED'] = pat_carac['TypeOFCIED'].value_counts()
df_carac['perc_CIED'] = (df_carac['type_CIED']/df_carac['type_CIED'].sum())*100
