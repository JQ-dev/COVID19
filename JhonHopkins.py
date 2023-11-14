

import pandas as pd


url1 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
url2 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

c = pd.read_csv(url1)
d = pd.read_csv(url2)


c = c.drop([ 'Lat', 'Long'],axis=1)
d =d.drop(['Lat', 'Long'],axis=1)


dates = list(c.columns[2:])
no_dates = list(c.columns[:2])

c = c.set_index(['Province/State','Country/Region'])
c = c.astype(int).fillna(0)
c = c - c.shift(1,axis=1)
c = c.reset_index()

d = d.set_index(['Province/State','Country/Region'])
d = d.astype(int).fillna(0)
d = d - d.shift(1,axis=1)
d = d.reset_index()

con = pd.melt(c, id_vars=no_dates, var_name='date', value_name='cases')
dea = pd.melt(d, id_vars=no_dates, var_name='date', value_name='deaths')

con = con.fillna(0)
dea = dea.fillna(0)


total = con.append(dea).fillna(0)

total = total.groupby(['Province/State','Country/Region','date']).sum().reset_index()


total.to_csv('D:/JHU_covid-19_191221.csv',index=False)

del url1, url2 , total, c, d, con, dea, dates, no_dates




#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################




dates = pd.date_range(start='01-22-2020', end='01-25-2022')

#df.columns

dfJHU = {}

for date in dates:
    
   
    date_text = date.strftime('%m-%d-%Y')
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'+date_text+'.csv'
    
    temp = pd.read_csv(url)
    
    temp['date'] = date_text
    temp = temp.rename(columns={'Province_State':'Province/State',
                                'Country_Region':'Country/Region',
                                'Last Update':'Last_Update',
                                'Lat':'Latitude',
                                'Long_':'Longitude',
                                'Case-Fatality_Ratio':'Case_Fatality_Ratio',
                                'Incident_Rate':'Incidence_Rate'})
    

    dfJHU[date_text] = temp
    
    print(date_text)



df = pd.concat(dfJHU.values(), ignore_index=True)




df.to_csv('D:/JHU_Full_covid-19_012122.csv',index=False)

del df, dfJHU, temp, url, date, date_text
