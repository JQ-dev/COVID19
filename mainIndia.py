# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 22:05:13 2020

@author: admin
"""

import pandas as pd 

version = '107'
path0 = 'C:/Users/admin/Downloads/Peru/CovidIndia_'+version+'.csv'
path1 = 'C:/Users/admin/Downloads/Peru/CovidIndia_mob_'+version+'.csv'

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


mob = pd.read_csv('C:/Users/admin/Downloads/Global_Mobility_Report.csv',sep=',')


#a = mob['country_region_code'].drop_duplicates()
#Filter Countries
mob = mob.loc[ mob['country_region_code'] == 'IN' , : ]



mob.to_csv(path1,index=False)

del mob

