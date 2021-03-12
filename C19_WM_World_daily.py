


from bs4 import BeautifulSoup 
import re
import pandas as pd
#from selenium import webdriver
import requests
import json
from datetime import date
import datetime
import numpy as np
import datetime


def population():
    
    url = 'https://www.worldometers.info/world-population/population-by-country/'

    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    
    table = soup.find('table', attrs={'id': 'example2'})
    
    head = table.find('thead').find('tr').find_all('th')
    
    col = []
    for element in head:
        col.append(element.text.strip())
    
    world = pd.DataFrame( columns=col)
    
    
    body = table.find('tbody').find_all('tr')
    
    for row in body:
        line = []
        for element in row.find_all('td'):
            line.append(element.text.strip())
        world = world.append( pd.Series(line, index=world.columns) ,ignore_index=True )
    
#    list(world.columns)
    world = world.rename(columns={"Country (or dependency)": "Country"})
    
    world.loc[ world.loc[:,'Country'] == 'United States' , 'Country'] = 'USA'
    world.loc[ world.loc[:,'Country'] == 'United Kingdom' , 'Country'] = 'UK'
    world.loc[ world.loc[:,'Country'] == 'United Arab Emirates' , 'Country'] = 'UAE'
    world.loc[ world.loc[:,'Country'] == 'St. Vincent & Grenadines' , 'Country'] = 'St. Vincent Grenadines'
    world.loc[ world.loc[:,'Country'] == 'Saint Barthelemy' , 'Country'] = 'St. Barth'
    world.loc[ world.loc[:,'Country'] == 'Saint Kitts & Nevis' , 'Country'] = 'Saint Kitts and Nevis'
    world.loc[ world.loc[:,'Country'] == 'South Korea' , 'Country'] = 'S. Korea'
    world.loc[ world.loc[:,'Country'] == 'State of Palestine' , 'Country'] = 'Palestine'
    world.loc[ world.loc[:,'Country'] == 'Côte d\'Ivoire' , 'Country'] = 'Ivory Coast'
    world.loc[ world.loc[:,'Country'] == 'DR Congo' , 'Country'] = 'DRC'
    world.loc[ world.loc[:,'Country'] == 'Czech Republic (Czechia)' , 'Country'] = 'Czechia'
    world.loc[ world.loc[:,'Country'] == 'Central African Republic'     , 'Country'] = 'CAR'
    
    world.loc[ world.loc[:,'Country'] == 'Sao Tome & Principe' , 'Country'] = 'Sao Tome and Principe'    
    world.loc[ world.loc[:,'Country'] == 'Saint Pierre & Miquelon'     , 'Country'] = 'Saint Pierre Miquelon'      
#    world.loc[ world.loc[:,'Country'] == ''     , 'Country'] = ''      
#    world.loc[ world.loc[:,'Country'] == ''     , 'Country'] = ''     
#    world.loc[ world.loc[:,'Country'] == ''     , 'Country'] = ''     
#    world.loc[ world.loc[:,'Country'] == ''     , 'Country'] = ''      
#    world.loc[ world.loc[:,'Country'] == ''     , 'Country'] = ''      
    
    
    world = world.drop(['#','Yearly Change','Net Change','Density (P/Km²)','World Share','Fert. Rate'],axis=1)       
    #temp =  world.iloc[:,:]
    #world =  temp.copy()
                        
    world.iloc[:,1:] = world.iloc[:,1:].replace(',','',regex=True).replace(' %','',regex=True)    
    
    world.iloc[:,1:] = world.iloc[:,1:].replace('N.A.',None,regex=True).replace('',None,regex=True)
     
    world.iloc[:,1:] = world.iloc[:,1:].astype(int)
    
    world.iloc[:,0] = world.iloc[:,0].str.upper()
    
    return world
    
    
    
def find_str(s, char):
    index = 0
    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index
            index += 1
    return -1

###############################################################################





def country_list():
    url = 'https://www.worldometers.info/coronavirus/'

    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')

    table = soup.find('table', attrs={'id': 'main_table_countries_today'}).find_all('a')

    country_url = []
    for t in table:
        row = [t['href'],t.text.strip()]
        country_url.append(row)

    return country_url


def extract_charts(country):
    
    # country = countries[0]
    
    url = 'https://www.worldometers.info/coronavirus/' + country[0]
    
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    # a = soup.prettify()
    
    charts = soup.find_all('script', attrs={'type': 'text/javascript'})
    
    select = [  "Highcharts.chart('graph-death",
                "Highcharts.chart('cases-cured", 
                "Highcharts.chart('graph-cases"  ]
        
    ch = []
    for chart in charts:
        if (chart.text.strip())[:29] in select:
            ch.append(chart.text.strip())
    
    
    country_table = pd.DataFrame(columns=['dates'])

    
    for table in ch:
    
        l1 = (find_str(table, '('))    
        l2 = (find_str(table, ','))      
        table_name = table[l1+1:l2]   
        
        
        l1 = (find_str(table, 'xAxis: {'))
        l2 = (find_str(table, 'yAxis: {'))
        l3 = (find_str(table, 'series: [{'))
        
        temp = table[l1:l2]
        l11 = (find_str( temp, '['))
        l12 = (find_str( temp, ']'))
        temp = temp[l11:l12+1]
        dates = eval(temp)
    
        temp = table[l3:]    
        
        l11 = (find_str(temp, 'data'))
        temp = temp[l11:]    
        
        
        l11 = (find_str(temp, '['))
        l12 = (find_str(temp, ']'))    
        
        temp = temp[l11:l12+1].replace('null','0')
        
        data = eval(temp)
        
        dict_data = dict(zip( dates , data ))
    
        #New dates
        for dat in dates:
            if dat not in list(country_table['dates']):
                country_table = country_table.append( pd.DataFrame({'dates':[dat]}) , sort=True )
        
    
        country_table[table_name] = country_table['dates'].map(dict_data)

    country_table['country'] = country[1]

    return country_table


def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))



def db_to_file(last):

    pop = population()
    
    countries = country_list()
    
    database = pd.DataFrame()
    
    for country in countries:
        table = extract_charts(country)
        if database.shape[1]==0:
            database = table
        else:
            database = pd.concat([database, table])
    
    
    
    database['country'] = database['country'].replace('country/','',regex=True).replace('/','',regex=True).str.upper()
    
    database = database.fillna(0)
  
    
    
    #database.loc[:,'dates'] = database.loc[:,'dates'].apply(lambda x : datetime.datetime.strptime( '%b %d %Y') )
    database.loc[:,'dates'] = pd.to_datetime(database.loc[:,'dates'])


#    database['diff'] = (database['dates'] - database['dates'].shift(periods=1)).apply(lambda x: x.days)
#    database['diff'] = database['diff'].fillna(1)
    
    #database['dates2'] = database['dates'].copy()


#    mod_year = False
#    for row in range(1,len(database['dates'])-1):
#        diff = database['diff'].iloc[row+1]
#
#        if diff < 0:
#            mod_year = True
#            
#        if diff > 1:
#            mod_year = False            
#
#        if mod_year == True:
#            
#            try:
#                database['dates'].iloc[row+1] =  add_years(database['dates'].iloc[row+1], 1)
#                #print(diff)
#            except:
#                continue
#            
#        
#    database = database.drop(['diff'],axis=1)
    

    
    database = database.rename(columns={"'cases-cured-daily'": 'recovered',
                                        "'graph-cases-daily'": 'cases',
                                        "'graph-deaths-daily'": 'deaths'})
    
    
    
    database['cum_recovered'] = 0
    database['cum_cases'] = 0
    database['cum_deaths'] = 0
        
        
    countries = database['country'].drop_duplicates()
    #list(database.columns)
    
    for country in countries:
        
        temp = database.loc[ database.loc[:,'country']==country ,['recovered','cases','deaths','dates']]
        
        new_cols = [['recovered','cum_recovered'],['cases','cum_cases'],['deaths','cum_deaths']]
        #col = ['cases','cum_cases']
        for col in new_cols:
            temp = database.loc[ database.loc[:,'country']==country ,[col[0],'dates']].sort_values(by=['dates'])
            
            temp_dict = dict(zip( temp['dates'] , np.cumsum(temp[col[0]]) ))
            
            database.loc[ database.loc[:,'country']==country ,col[1]] = database.loc[ database.loc[:,'country']==country ,'dates'].map(temp_dict)
    
    
    del table, temp, temp_dict, countries
    
    path1 = 'C:/Users/admin/Downloads/Peru/Covid_worldometers' + last + '.csv'
    path2 = 'C:/Users/admin/Downloads/Peru/Population_worldometers' + last + '.csv'
    
    return database, last
    
    #database.to_csv(path1,index=False)
    #pop.to_csv(path2,index=False)





    
consecutive = '166' 
#last = '164'

#db_to_file(consecutive)









 

########################3

#df = pd.read_csv('C:/Users/admin/Downloads/Peru/Covid_worldometers' + consecutive + '.csv')

df, consecutive = db_to_file(consecutive)


dates = df[['dates',]].drop_duplicates()

last_index = dates.index[-1]

countries = df[['country']].drop_duplicates()

countries.index = range(last_index,last_index+countries.shape[0])

countries['key'] = 1
dates['key'] = 1


df_base = pd.merge(countries, dates, on='key').drop('key',1)


df = pd.merge(df, df_base,how='right', on=['country','dates'])

df = df.fillna(0)


mob = pd.read_csv('C:/Users/admin/Downloads/Global_Mobility_Report.csv')

list(df.columns)
list(mob.columns)

mob = mob[mob['sub_region_1'].isnull()]
mob = mob[mob['sub_region_2'].isnull()]
mob = mob[mob['metro_area'].isnull()]


mob = mob.drop(['country_region_code', 'sub_region_1',
 'sub_region_2', 'metro_area', 'iso_3166_2_code',
 'census_fips_code','place_id'],axis=1)

mob.columns =   ['country', 'dates',
 'retail_and_recreation', 'grocery_and_pharmacy',
 'parks', 'transit_stations', 'workplaces', 'residential']  
    
mob['country'] = mob['country'].str.upper()


#c_mob = mob['country'].drop_duplicates()
#c_df = df['country'].drop_duplicates()


renaming = [['UNITED KINGDOM','UK'],['UNITED STATES','USA'],['UNITED ARAB EMIRATES','UAE'],
           ['CAPE VERDE','CABO VERDE'],['MYANMAR (BURMA)','MYANMAR'],['SOUTH KOREA','S. KOREA'],
           ['THE BAHAMAS','BAHAMAS'],['CÔTE D\'IVOIRE','IVORY COAST'],['',''],['','']]



for new_name in renaming:
    print(new_name[0],new_name[1])
    mob['country'] = mob['country'].replace(new_name[0],new_name[1])

mob['dates'] = pd.to_datetime(mob['dates'])


c_join = pd.merge(df, mob, how='outer', on=['country','dates'])

path1 = 'C:/Users/admin/Downloads/Peru/Covid_worldometers' + consecutive + '.csv'

c_join.to_csv(path1,index=False)


#del c_df, c_mob
del c_join, consecutive, df, mob, path1, renaming, new_name, dates, countries, last_index, df_base




