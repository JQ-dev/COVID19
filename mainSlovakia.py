# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 20:15:39 2021

@author: admin
"""

import pandas as pd

version = '211118'
link = 'C:/Users/admin/Downloads/Peru/COVID_Slovakia_211118.csv'



url1 = "https://raw.githubusercontent.com/Institut-Zdravotnych-Analyz/covid19-data/main/Deaths/OpenData_Slovakia_Covid_Deaths_AgeGroup_District.csv"
url2 = "https://raw.githubusercontent.com/Institut-Zdravotnych-Analyz/covid19-data/main/DailyStats/OpenData_Slovakia_Covid_DailyStats_Regions.csv"
url3 = "https://raw.githubusercontent.com/Institut-Zdravotnych-Analyz/covid19-data/main/Hospitals/OpenData_Slovakia_Covid_Hospital_Full.csv"
url4 = "https://raw.githubusercontent.com/Institut-Zdravotnych-Analyz/covid19-data/main/Vaccination/OpenData_Slovakia_Vaccination_Regions.csv"

d = pd.read_csv(url1,encoding='ISO-8859-2',sep=';')
c = pd.read_csv(url2,encoding='ISO-8859-2',sep=';')
h = pd.read_csv(url3,encoding='ISO-8859-2',sep=';')
v = pd.read_csv(url4,encoding='ISO-8859-2',sep=';')


d = d[d['Date'] != '#VALUE!' ]


d['Date'] = pd.to_datetime(d['Date'],format='%d.%m.%Y')
c['Datum'] = pd.to_datetime(c['Datum'],format='%Y-%m-%d')
v['Date'] = pd.to_datetime(v['Date'],format='%Y-%m-%d')

h['DAT_SPRAC'] = pd.to_datetime(h['DAT_SPRAC'],format='%Y-%m-%d %H:%M:%S')
h['DATUM_VYPL'] = pd.to_datetime(h['DATUM_VYPL'],format='%Y-%m-%d %H:%M:%S')

names = list(d.columns)
names = ['d.' + s for s in names]
d.columns = names

names = list(c.columns)
names = ['c.' + s for s in names]
c.columns = names

names = list(h.columns)
names = ['h.' + s for s in names]
h.columns = names

names = list(v.columns)
names = ['v.' + s for s in names]
v.columns = names


d['db'] = 'deaths'
c['db'] = 'cases'
h['db'] = 'hospit'
v['db'] = 'vaccin'


todas = pd.concat([c,d,v,h])


todas.to_csv(link)

del c,d,h,v,names, url1, url2, url3, url4, link

del todas



mob = pd.read_csv('C:/Users/admin/Downloads/Global_Mobility_Report.csv',sep=',')


a = mob.loc[:,['country_region','country_region_code']].drop_duplicates()
#Filter Countries
mob = mob.loc[ mob['country_region_code'] == 'SK' , : ]

# Rrmove region 2 and whole country
#cond = mob.loc[:,'sub_region_1'].notna()
#mob1 = mob1.loc[ cond , : ]
#
#cond = mob.loc[:,'sub_region_2'].isna()
#mob1 = mob1.loc[ cond , : ]

path5 = 'C:/Users/admin/Downloads/Peru/Slovakia_'+version+'_mob.csv'

mob.to_csv(path5,index=False)


del  version, path5


del mob,a
