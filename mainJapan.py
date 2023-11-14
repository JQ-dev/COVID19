



import pandas as pd
import time

hoy = time.ctime()[4:11] + time.ctime()[-4:]
link = 'D:/COVID_Data/Japan_'+hoy+'.csv'


df1 = pd.read_csv('https://covid19.mhlw.go.jp/public/opendata/newly_confirmed_cases_daily.csv')
df1 = df1.set_index('Date').stack().reset_index()
df1 = df1.rename(columns={'level_1':'Prefecture',0:'cases'})


dfx = pd.read_csv('https://covid19.mhlw.go.jp/public/opendata/requiring_inpatient_care_etc_daily.csv')


#df = pd.merge(df,df1,on=['Date', 'Prefecture'],how='outer')

df2 = pd.read_csv('https://covid19.mhlw.go.jp/public/opendata/deaths_cumulative_daily.csv')
df2 = df2.set_index('Date')
df2 = df2.shift(-1) - df2 
df2 = df2.stack().reset_index()
df2 = df2.rename(columns={'level_1':'Prefecture',0:'deaths'})

df = pd.merge(df1,df2,on=['Date', 'Prefecture'],how='outer')

df3 = pd.read_csv('https://covid19.mhlw.go.jp/public/opendata/severe_cases_daily.csv')
df3 = df3.set_index('Date').stack().reset_index()
df3 = df3.rename(columns={'level_1':'Prefecture',0:'sev_cases'})

df = pd.merge(df,df3,on=['Date', 'Prefecture'],how='outer')

df = df.fillna(0)


df.to_csv(link)

del df, df1, df2, df3, hoy, link

