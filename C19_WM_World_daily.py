


from bs4 import BeautifulSoup 
import re
import pandas as pd
#from selenium import webdriver
import requests
import json
from datetime import date
import datetime
import numpy as np


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
    
    database.loc[:,'dates'] = database.loc[:,'dates'].apply(lambda x : datetime.datetime.strptime( x +' 2020', '%b %d %Y') )
    
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
    
    database.to_csv(path1,index=False)
    #pop.to_csv(path2,index=False)
    
    



db_to_file('106')


########################3

#df = pd.read_csv('C:/Users/admin/Downloads/Peru/Covid_worldometers052.csv')
#
#df_pop = pd.read_csv('C:/Users/admin/Downloads/Peru/Population_worldometers048.csv')
#
#
#df0 = pd.merge(df,df_pop,left_on='country', right_on='Country')
#del df, df_pop
#
#df0['Deaths/pop'] = df0['cum_deaths'] / df0['Population (2020)']
#
#
## 1 /100.000 Cases
#df0 = df0.loc[ df0['Deaths/pop'] > 0.0000001 ,:]
#
#
#countries = df0['country'].drop_duplicates()
#
#
#df0['new_date'] = pd.to_datetime(df0['dates'])
#df0['days'] = 0
#
#pais = 'CHINA'
#
#for pais in countries:
#    day_zero = df0.loc[ df0['country'] == pais ,'new_date'].min()
#    df0.loc[ df0['country'] == pais , 'days'] = df0.loc[ df0['country'] == pais ,'new_date'] - day_zero
#
#
#df0['days'] = df0['days'] / 86400000000000
#
#
#df0.to_csv('C:/Users/admin/Downloads/Peru/COVID_Chile02.csv',index=False)





