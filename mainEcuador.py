# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 13:19:52 2021

@author: admin
"""

import pandas as pd


link = 'C:/Users/admin/Downloads/Peru/COVID_Ecuador_210303d.csv'
link2 = 'C:/Users/admin/Downloads/Peru/COVID_Ecuador_mob__210303d.csv'

#url3 = "https://github.com/dsfsi/covid19za/raw/master/data/covid19za_timeline_testing.csv"


dff1 = pd.read_csv("https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/muertes/2020/por_fecha/provincias_por_dia.csv")
dff2 = pd.read_csv("https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/muertes/por_fecha/provincias_por_dia.csv")

dfc1 = pd.read_csv("https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/positivas/2020/por_fecha/provincias_por_dia.csv")
dfc2 = pd.read_csv("https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/positivas/por_fecha/provincias_por_dia.csv")

dfd1 = pd.read_csv("https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/defunciones/2020/por_fecha/lugar_provincias_por_dia.csv")
dfd2 = pd.read_csv("https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/defunciones/por_fecha/provincias_por_dia.csv")
dfd3 = pd.read_csv("https://raw.githubusercontent.com/andrab/ecuacovid/master/datos_crudos/defunciones/2019/por_fecha/lugar_provincias_por_dia.csv")

                   
df3 = pd.DataFrame()



def combine_df(df1,df2,df3,values):

    df1 = df1.drop(['lat','lng'],axis=1)
    df2 = df2.drop(['lat','lng'],axis=1)
    
    
    df1 = df1.melt(id_vars = ['provincia','poblacion'], var_name = 'Date', value_name = values)
    
    df1['Date'] = pd.to_datetime(df1['Date'],format='%d/%m/%Y')
    
    df2 = df2.melt(id_vars = ['provincia','poblacion'], var_name = 'Date', value_name = values)
    
    df2['Date'] = pd.to_datetime(df2['Date'],format='%d/%m/%Y')
    
    
    try:
        df3 = df3.drop(['lat','lng'],axis=1)
        df3 = df3.melt(id_vars = ['provincia'], var_name = 'Date', value_name = values)
        df3['Date'] = pd.to_datetime(df3['Date'],format='%d/%m/%Y')    
        
        df = pd.concat([df1,df2,df3]) 
        print("three OK")
    except:
        df = pd.concat([df1,df2])
        print("two OK")
        
    
    return df



df_f = combine_df(dff1,dff2,df3,'fatalities')

df_c = combine_df(dfc1,dfc2,df3,'cases')

df_d = combine_df(dfd1,dfd2,dfd3,'deaths')
    
del     dff1,dff2,dfc1,dfc2,dfd1,dfd2


df = pd.concat([df_f,df_c,df_d]).fillna(0)

df.to_csv(link,index=False)


del df, df_f, df_c, df_d, link



mob = pd.read_csv('C:/Users/admin/Downloads/Global_Mobility_Report.csv',sep=',')


#a = mob['country_region_code'].drop_duplicates()
#Filter Countries
mob = mob.loc[ mob['country_region_code'] == 'EC' , : ]



mob.to_csv(link2,index=False)

del mob


