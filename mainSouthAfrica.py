
import pandas as pd
#import numpy as np

link = 'D:/COVID/COVID_SouthAfrica_260622.csv'
link1 = 'D:/COVID/COVID_SouthAfrica_260622_mob.csv'
link2 = 'D:/COVID/COVID_SouthAfrica_260622_testing.csv'

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


#c = c.replace(0,np.NAN)
#d = d.replace(0,np.NAN)
#
#
#c = c.reset_index()
#states = c['State'].drop_duplicates()
#
#for state in states:
#    cond = (c['State']==state) & (c['cum cases']!=c['cum cases'])
#    c.loc[cond,'cum cases'] = c.loc[ c.loc[cond,'index']-1 , 'cum cases'].to_list()
#
#c = c.drop(['index'],axis=1)
#
#
#
#d = d.reset_index()
#states = d['State'].drop_duplicates()
#
#for state in states:
#    cond = (d['State']==state) & (d['cum deaths']!=d['cum deaths'])
#    d.loc[cond,'cum deaths'] = d.loc[ d.loc[cond,'index']-1 , 'cum deaths'].to_list()
#
#d = d.drop(['index'],axis=1)
#
#
#del cond, state, states





#c = c.drop(c.index[c['date'] == '07-04-2020'].tolist(), axis=0)
#c = c.drop(c.index[c['date'] == '27-03-2020'].tolist(), axis=0)


#c.loc[c['date'] == '07-04-2020','EC':'WC'] = c.loc[c['date'] == '06-04-2020','EC':'WC']
#c.loc[c['date'] == '27-03-2020','EC':'WC'] = c.loc[c['date'] == '26-03-2020','EC':'WC']


df = pd.merge(c,d,how='left',on=['date','State'])

df['date'] = pd.to_datetime(df['date'],format='%d-%m-%Y')

df = df.sort_values(by=['State','date'], axis=0).fillna(0).reset_index(drop=True)

df = df.fillna(0)

df = df.reset_index()
states = df['State'].drop_duplicates()

for state in states:
    tempdf = df[df['State']==state]
    
    cond = tempdf['cum cases']==0
    cond2 = cond.shift(-1,fill_value=False)
    cond.iloc[0] = False
    tempdf.loc[cond,'cum cases'] = tempdf.loc[cond2,'cum cases'].to_list()

    cond  = tempdf['cum deaths']==0
    cond2 = cond.shift(-1,fill_value=False)
    cond.iloc[0] = False
    tempdf.loc[cond,'cum deaths'] = tempdf.loc[cond2,'cum deaths'].to_list()

    df[df['State']==state] = tempdf
    
    del tempdf
    


del cond, cond2, state, states




df['cum cases -1'] = df['cum cases'].shift(1).fillna(0)

df['cum death -1'] = df['cum deaths'].shift(1).fillna(0)

df['cases'] = df['cum cases'] - df['cum cases -1']

df['deaths'] = df['cum deaths'] - df['cum death -1']



#df['date'] == '2020-03-05 00:00:00'
#
#df.loc[df['date'] == '2020-03-05 00:00:00',['cases','deaths']] = 0
#


df.loc[df['cases'] < 0,['cum cases']] = df.loc[df['cases'] < 0,['cum cases -1']].iloc[:,0].values

df.loc[df['deaths'] < 0,['cum deaths']] = df.loc[df['deaths'] < 0,['cum death -1']].iloc[:,0].values


df['cases'] = df['cum cases'] - df['cum cases -1']

df['deaths'] = df['cum deaths'] - df['cum death -1']

#df.loc[df['date'] == '2020-03-05 00:00:00',['cases','deaths']] = 0

df = df.drop(['cum cases -1','cum death -1'],axis=1)











df.to_csv(link,index=False)


del df, c, d, url1, url2, link









mob = pd.read_csv('D:/COVID/Global_Mobility_Report.csv',sep=',')


mob['country_region_code'].drop_duplicates()
#Filter Countries
mob = mob.loc[ mob['country_region_code'] == 'ZA' , : ]

# Rrmove region 2 and whole country
#cond = mob.loc[:,'sub_region_1'].notna()
#mob1 = mob1.loc[ cond , : ]
#
#cond = mob.loc[:,'sub_region_2'].isna()
#mob1 = mob1.loc[ cond , : ]

mob.to_csv(link1,index=False)


del mob, link1




df_testing = pd.read_csv('https://github.com/dsfsi/covid19za/raw/master/data/covid19za_provincial_timeline_testing.csv',encoding='cp1252')

df_testing = df_testing.drop(['weektag','week','source'],axis=1)

df = df_testing.set_index(['var','eowYYYYMMDD'])

df = df.stack()

df = df.reset_index()

df = df.set_index(['level_2','eowYYYYMMDD'])

df = df.pivot(columns='var')

df = df.reset_index()

df.columns = ['Province','Date','Positive','Tests']

df['Positivity'] = df['Positive']/df['Tests']

df.to_csv(link2,index=False)

del df,df_testing