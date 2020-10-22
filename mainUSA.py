# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 18:40:01 2020

@author: admin
"""


import pandas as pd
#import numpy as np

us_counties = pd.read_csv('C:/Users/admin/Downloads/County__United_States.csv')

us_counties = us_counties.loc[ us_counties.iloc[:,1] == 2017 , us_counties.columns[[0,2,3,4,5]] ]

us_counties['St'] = us_counties['County'].str.split(', ', n = 2, expand = True).iloc[:,1]
us_counties['Ct'] = us_counties['County'].str.split(', ', n = 2, expand = True).iloc[:,0]

us_counties['Population'] = us_counties['Population'].replace(',','',regex=True).apply(int)

#us_counties = us_counties.loc[: , ['FIPS','County','Population']]

us_counties['FIPS'] = us_counties['FIPS'].astype(str)

us_counties.loc[us_counties['FIPS'].str.len()==4,'FIPS'] = '0'+us_counties.loc[ us_counties['FIPS'].str.len()==4,'FIPS']


us_states = us_counties.groupby(['State','St']).aggregate('Population').sum()
us_states = us_states.reset_index()


us_states = us_states.append( pd.Series(['U.S. Virgin Islands','VI',104914], index=us_states.columns) ,ignore_index=True )
us_states = us_states.append( pd.Series(['Puerto Rico','PR',	3193694], index=us_states.columns) ,ignore_index=True )
us_states = us_states.append( pd.Series(['Guam','GU',	165718], index=us_states.columns) ,ignore_index=True )
us_states = us_states.append( pd.Series(['American Samoa','AS',	55641], index=us_states.columns) ,ignore_index=True )
us_states = us_states.append( pd.Series(['Northern Mariana Islands','MP',	55194], index=us_states.columns) ,ignore_index=True )


us_counties.to_csv('us_counties.csv')
us_states.to_csv('us_states.csv')

################################################################################


url1 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
url2 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/c8bfc4b23ba4acaa011bc76e67cc527937155bda/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
url3 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/c8bfc4b23ba4acaa011bc76e67cc527937155bda/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"


c = pd.read_csv(url1)
d = pd.read_csv(url2)
r = pd.read_csv(url3)

dates = list(c.columns[4:])
no_dates = list(c.columns[:4])

con = pd.melt(c, id_vars=no_dates, var_name='date', value_name='total')
dea = pd.melt(d, id_vars=no_dates, var_name='date', value_name='total')
rec = pd.melt(r, id_vars=no_dates, var_name='date', value_name='total')

con['condition'] = "Confirmed"
dea['condition'] = "Deaths"
rec['condition'] = "Recovered"


con = con.fillna('')
dea = dea.fillna('')
rec = rec.fillna('')


con.index = con.iloc[:,1]+'-'+con.iloc[:,0]
dea.index = dea.iloc[:,1]+'-'+dea.iloc[:,0]
rec.index = rec.iloc[:,1]+'-'+rec.iloc[:,0]


naming = pd.concat ( [con.iloc[:,:4] , dea.iloc[:,:4] , rec.iloc[:,:4]] ).drop_duplicates()
naming = naming.reset_index()

naming['Country'] = naming['index'].str.split('-', n = 1, expand = True).iloc[:,0]
naming['State'] = naming['index'].str.split('-', n = 0, expand = True).iloc[:,1]

naming['State'] = naming['State'].str.split(', ', n = 0, expand = True).iloc[:,0]
naming['County'] = ''

naming['St'] = naming['index'].str.split('-', n = 0, expand = True).iloc[:,1]
naming['St'] = naming['St'].str.split(', ', n = 0, expand = True).iloc[:,1]

#last_day = naming.loc[ naming.loc[:,'date'] == '3/22/20',:]
#last_day = last_day.loc[ last_day.loc[:,'Country'] == 'US',:]

naming['level'] = ''

naming.loc[ naming['State']=='' ,'level'] = 'Country' 

naming.loc[ naming['St'].notnull() ,'level'] = 'County' 

naming.loc[ naming['level']=='' ,'level'] = 'Province'



naming.loc[ naming.loc[:,'level'] == 'County' ,'County'] = naming.loc[ naming.loc[:,'level'] == 'County' , 'State' ]
naming.loc[ naming.loc[:,'level'] == 'County' ,'State'] = naming.loc[ naming.loc[:,'level'] == 'County' , 'St' ]

naming['County2'] = naming['County'] + ', ' + naming['State']

county_id = dict(zip(us_counties['County'],us_counties['FIPS']))



naming['FIPS'] = naming['County2'].map(county_id)

naming['FIPS'] = naming['FIPS'].astype(str)


naming = naming.reset_index()
name_id = dict(zip(naming['index'],naming['level_0']))


#naming['FIPS'] = naming['FIPS'].replace(np.nan, None)
#naming['FIPS'] = naming['FIPS'].replace('', None)
#naming['FIPS'] = naming['FIPS'].astype(int)
#
#naming['FIPS'] = pd.to_numeric(naming['FIPS'], errors='coerce')
#
#
#naming['FIPS'] = naming['FIPS'].replace(0, None)

naming = naming.drop(['Province/State','Country/Region','St','index','County2'],axis=1)


total = pd.concat ( [con.iloc[:,4:] , dea.iloc[:,4:] , rec.iloc[:,4:]] )

del url1,url2,url3,c,d,r,dates,no_dates, con, dea, rec

total = total.reset_index()

total['level_0'] = total['index'].map(name_id)

total['Country'] = total['index'].str.split('-', n = 1, expand = True).iloc[:,0]

total = total.drop(['index'],axis=1)

total_US = total.loc[ total.loc[ : ,'Country'] == 'US' ,  ]
naming_US = naming.loc[ naming.loc[ : ,'Country'] == 'US' ,  ]



total_US.to_csv('US_covid-19_data.csv')
#naming_US.to_csv('US_covid-19_names.csv')


del total_US,naming_US, total


