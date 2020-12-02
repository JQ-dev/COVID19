# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 22:05:13 2020

@author: admin
"""

import pandas as pd 

version = '06'
path0 = 'C:/Users/admin/Downloads/Peru/CovidIndia_'+version+'.csv'

i = 1
raw_d = []
while True:
    try:
        url = f"https://api.covid19india.org/csv/latest/raw_data{i}.csv"
        df = pd.read_csv(url)
        df.to_csv(f'./tmp/csv/latest/raw_data{i}.csv',index=False)
        raw_d.append(df)
        i = i+1
    except:
        break

raw_all = pd.DataFrame()


for chunk in raw_d:
    raw_all = raw_all.append(chunk)


list(raw_all.columns)

keep_col = ['Date Announced','Detected District','Detected State','Current Status','Num Cases']


dfIndia = raw_all.loc[:,keep_col]

dfIndia.to_csv(path0,index=False)

