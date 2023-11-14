

import pandas as pd






url1 = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
url2 = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"

c = pd.read_csv(url1)
d = pd.read_csv(url2)

#c1 = c.T
#d1 = d.T 

population = d.loc[:,['UID','Admin2','Province_State','Population']].drop_duplicates()


state_pop = population.groupby('Province_State').sum().reset_index()

add_col = dict(zip(state_pop['Province_State'],state_pop['Population']))

population['state_pop'] = population['Province_State'].map(add_col)




c = c.drop(['iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
       'Country_Region', 'Lat', 'Long_','Combined_Key'],axis=1)
d =d.drop(['iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
       'Country_Region', 'Lat', 'Long_','Combined_Key','Population'],axis=1)



dates = list(c.columns[1:])
no_dates = list(c.columns[:1])

c1 = c.copy()
d1 = d.copy()

c = c.set_index('UID')
c = c.astype(int)
c = c - c.shift(1,axis=1)
c = c.reset_index()

d = d.set_index('UID')
d = d.astype(int)
d = d - d.shift(1,axis=1)
d = d.reset_index()







con = pd.melt(c, id_vars=no_dates, var_name='date', value_name='cases')
dea = pd.melt(d, id_vars=no_dates, var_name='date', value_name='deaths')



con = con.fillna(0)
dea = dea.fillna(0)

dates = con.append(dea)['date'].drop_duplicates()



total = con.append(dea).groupby(['UID','date']).sum().reset_index()

#total = pd.merge(con,dea,how='outer',on=['UID','date'])




#con.index = con['UID'].astype(str) + con['date'].astype(str)
#dea.index = dea['UID'].astype(str) + dea['date'].astype(str)


# Add state

add_col = dict(zip(population['UID'],population['Province_State']))
total['State'] = total['UID'].map(add_col)

add_col = dict(zip(population['UID'],population['Admin2']))
total['County'] = total['UID'].map(add_col)

add_col = dict(zip(population['UID'],population['Population']))
total['Population'] = total['UID'].map(add_col)

add_col = dict(zip(population['Province_State'],population['state_pop']))
total['state_pop'] = total['State'].map(add_col)


total = total.fillna(0)

a = total[total['State']=='Florida']

total['County'] = total['County'].astype(str)


total['date'] = pd.to_datetime(total['date'])


a1 = total[total['UID']=="84048497"]



vaxx = pd.read_csv('D:/COVID-19_Vaccinations_in_the_United_States_County.csv')





vaxx = vaxx.loc[:,['Date', 'FIPS','Series_Complete_65PlusPop_Pct']]

vaxx['date'] = pd.to_datetime(vaxx['Date'])

vaxx['Vax_60+'] = vaxx['Series_Complete_65PlusPop_Pct']

vaxx['UID'] = '840' + vaxx['FIPS'].astype(str)


vaxx = vaxx.loc[:,['UID', 'date','Vax_60+']]

vaxx['UID'] = vaxx['UID'].replace('840UNK','0')

vaxx['UID'] = vaxx['UID'].astype(int)

a2 = total.head(1000)



final = pd.merge(total,vaxx,how='left',on=['UID', 'date'])

a = final.head(1000)


final['County'] = final['County'].replace('0','')

del add_col, total, c, c1,con, d, d1, dea, population, no_dates, dates, url1, url2, state_pop, vaxx

final.to_csv('D:/US_covid-19_120122.csv',index=False)



# NURSING HOMES


df20 = pd.read_csv('D:/faclevel_2020.csv')
df21 = pd.read_csv('D:/faclevel_2021.csv')
df22 = pd.read_csv('D:/faclevel_2022.csv')

#a = df.columns.tolist()
#a = df.head(100)
#a[191]

keep = ['Week Ending','Provider Name', 'Provider City', 'Provider State',
        'Number of Residents Staying in this Facility for At Least 1 Day This Week',
        'Residents Weekly Confirmed COVID-19',
        'Residents Weekly Admissions COVID-19',
        'Residents Weekly Suspected COVID-19',
        'Residents Weekly All Deaths',
        'Residents Weekly COVID-19 Deaths',
        'Staff Weekly Confirmed COVID-19',
        'Staff Weekly Suspected COVID-19',
        'Staff Weekly COVID-19 Deaths',
        'Percentage of Current Residents who Received a Completed COVID-19 Vaccination at Any Time',
        'Percentage of Current Healthcare Personnel who Received a Completed COVID-19 Vaccination at Any Time',
        'Number of All Healthcare Personnel Eligible to Work in this Facility for At Least 1 Day This Week']


df20 = df20.loc[:,keep]

df21 = df21.loc[:,keep]

df22 = df22.loc[:,keep]

df = df20.append(df21)

df = df.append(df22)


del df20, df21, df22

df = df.rename(columns={'Percentage of Current Residents who Received a Completed COVID-19 Vaccination at Any Time':'Residents vax share',
                        'Percentage of Current Healthcare Personnel who Received a Completed COVID-19 Vaccination at Any Time':'Workers vax share',
                        'Number of All Healthcare Personnel Eligible to Work in this Facility for At Least 1 Day This Week':'Workers',
                        'Number of Residents Staying in this Facility for At Least 1 Day This Week':'Residents'
                        })





df = df.fillna(0)

df['Resid vax'] = df['Residents'] * df['Residents vax share'] /100
df['Work vax'] = df['Workers'] * df['Workers vax share'] / 100


df = df.drop(['Provider Name','Provider City'],axis=1)

df = df.groupby(['Week Ending','Provider State',]).sum().reset_index()


df['Residents vax share'] = df['Resid vax'] / df['Residents'] *  100
df['Workers vax share'] = df['Work vax'] / df['Workers'] *  100



uscode = pd.read_csv('D:/US_StateCodes.csv')

df['state'] = df['Provider State'].map(dict(zip(uscode.Code,uscode.Name)))

df['population'] = df['Provider State'].map(dict(zip(uscode.Code,uscode.Population)))

df['Week Ending'] = pd.to_datetime(df['Week Ending'])

final['date'] = pd.to_datetime(final['date'])

final = final.drop(['UID', 'County', 'Population','state_pop', 'Vax_60+'],axis=1)



final.columns

final = final.groupby(['date','State']).sum()
final = final.reset_index()

new_final = pd.merge(final,df,how='left', left_on=['State','date'], right_on=['state','Week Ending'] )


new_final.to_csv('D:/US_NursingHomes_130122.csv',index=False)





#
#
#
#
#import pandas as pd
##import datetime as dt
#
#us_groups = pd.read_csv('C:/Users/admin/Downloads/COVID-19_Case_Surveillance_Public_Use_Data.csv')
#
#us_groups['Date'] = pd.to_datetime(us_groups['Date'],format='%Y%m%d')
#
##us_groups['day_of_week'] =  us_groups['Date'].dt.day_name()
#
##us_groups = us_groups[us_groups['day_of_week']=='Sunday']
##us_groups = us_groups.drop('day_of_week',axis=1)
#
#
#us_groups = us_groups.fillna(0)
#
#
#
#
#
#
#us_groups1 = pd.melt(us_groups,id_vars=['Date','State'],value_name='Value',var_name='Measure')
#
#us_groups1['Subgroup'] = us_groups1['Measure'].str.split("_", n = 1, expand = True)[1]
#us_groups1['Measure'] = us_groups1['Measure'].str.split("_", n = 1, expand = True)[0]
#
#
#
#
#us_groups2 = us_groups1.pivot_table(index=['Date'],columns=['Measure','State','Subgroup'],values='Value').reset_index()
#
#
#us_groups2.iloc[:,1:] = us_groups2.iloc[:,1:].diff()
#
#
#
#
#us_groups3 = pd.melt(us_groups2,id_vars=['Date'])
#
#
##us_groups3 = pd.melt(us_groups2,id_vars=['Date','State'],value_name='Value',var_name='Measure')
#
#
#us_groups3.to_csv('C:/Users/admin/Downloads/Peru/Ethnic__United_States_04_30b.csv',index=False)
#
#
#
#
#
#
#
#
#
#
##import datetime as dt
#
#cdc = pd.read_csv('C:/Users/admin/Downloads/COVID-19_Case_Surveillance_Public_Use_Data.csv')
#
#a = cdc.head(100)
#
#
#cdc = cdc.drop(['cdc_case_earliest_dt ' ,'cdc_report_dt','pos_spec_dt'],axis=1)
#
#cdc = cdc[cdc['onset_dt'].notna()]
#
#cdc = cdc[cdc['death_yn'] != 'Missing']
#
#cdc['count'] = 1
#
#columns = list(cdc.columns)[:-1]
#
#columns =['onset_dt',
# 'age_group',
# 'race_ethnicity_combined',
# 'hosp_yn',
# 'icu_yn',
# 'death_yn']
#
#cdc2 = cdc.groupby(columns).sum().reset_index()
#
#
#cdc2.to_csv('C:/Users/admin/Downloads/Peru/CDC__United_States_07_30.csv',index=False)
#
#
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################


import pandas as pd

dates = pd.date_range(start='04-01-2020', end='01-15-2022')

#df.columns

dfJHU = {}

for date in dates:
    
    try: 
        date_text = date.strftime('%m-%d-%Y')
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'+date_text+'.csv'
        
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

    except:
        
        print (date_text + ' not found')

df = pd.concat(dfJHU.values(), ignore_index=True)


df.count()


df.to_csv('D:/JHU_Full_US_covid-19_01132022.csv',index=False)

del dfJHU, temp, url, date, date_text, dates
