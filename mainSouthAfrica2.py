# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 13:19:52 2021

@author: admin
"""

import pandas as pd


link = 'C:/Users/admin/Downloads/Peru/COVID_SouthAfrica_210124.csv'

url1 = "https://github.com/dsfsi/covid19za/raw/master/data/covid19za_provincial_cumulative_timeline_deaths.csv"
url2 = "https://github.com/dsfsi/covid19za/raw/master/data/covid19za_provincial_cumulative_timeline_confirmed.csv"
#url3 = "https://github.com/dsfsi/covid19za/raw/master/data/covid19za_timeline_testing.csv"


d = pd.read_csv(url1)
c = pd.read_csv(url2)

d = d.drop(['UNKNOWN','total','source','YYYYMMDD'],axis=1)
c = c.drop(['UNKNOWN','total','source','YYYYMMDD'],axis=1)



#t = pd.read_csv(url3)

d = pd.melt(d, id_vars=['date'], value_vars=['EC','FS','GP','KZN','LP','MP','NC','NW','WC'],value_name='cum deaths',var_name='State').reset_index(drop=True)

c = pd.melt(c, id_vars=['date'], value_vars=['EC','FS','GP','KZN','LP','MP','NC','NW','WC'],value_name='cum cases',var_name='State').reset_index(drop=True)




#c = c.drop(c.index[c['date'] == '07-04-2020'].tolist(), axis=0)
#c = c.drop(c.index[c['date'] == '27-03-2020'].tolist(), axis=0)


#c.loc[c['date'] == '07-04-2020','EC':'WC'] = c.loc[c['date'] == '06-04-2020','EC':'WC']
#c.loc[c['date'] == '27-03-2020','EC':'WC'] = c.loc[c['date'] == '26-03-2020','EC':'WC']


df = pd.merge(c,d,how='left',on=['date','State'])

df['date'] = pd.to_datetime(df['date'],format='%d-%m-%Y')

df = df.sort_values(by=['State','date'], axis=0).fillna(0).reset_index(drop=True)


df['cum cases -1'] = df['cum cases'].shift(1).fillna(0)

df['cum death -1'] = df['cum deaths'].shift(1).fillna(0)

df['cases'] = df['cum cases'] - df['cum cases -1']

df['deaths'] = df['cum deaths'] - df['cum death -1']



df['date'] == '2020-03-05 00:00:00'

df.loc[df['date'] == '2020-03-05 00:00:00',['cases','deaths']] = 0


df.loc[df['cases'] < 0,['cum cases']] = df.loc[df['cases'] < 0,['cum cases -1']].iloc[:,0].values

df.loc[df['deaths'] < 0,['cum deaths']] = df.loc[df['deaths'] < 0,['cum death -1']].iloc[:,0].values


df['cases'] = df['cum cases'] - df['cum cases -1']

df['deaths'] = df['cum deaths'] - df['cum death -1']

df.loc[df['date'] == '2020-03-05 00:00:00',['cases','deaths']] = 0

df = df.drop(['cum cases -1','cum death -1'],axis=1)


df.to_csv(link,index=False)


del df, c, d, url1, url2, link



