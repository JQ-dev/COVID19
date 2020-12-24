# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 12:29:49 2020

@author: admin
"""

import pandas as pd
import numpy as np
import scipy.stats


file1 = 'C:/Users/admin/Downloads/COVID19Casos (6).csv'

#######################\
# Read from the path - It takes long because it is a excel file
df = pd.read_csv(file1)

del file1

list(df.columns)

df['count'] = 1

df['fallecido'] = df['fallecido'].replace('NO',0).replace('SI',1)


df = df.loc[:,[ 'residencia_provincia_nombre','fecha_apertura','fecha_fallecimiento','clasificacion_resumen','fecha_diagnostico','count']]


df = df.rename(columns={'residencia_provincia_nombre':'provincia'})
df['index'] = df['provincia'] + df['fecha_apertura']


df_eval = df.loc[:,['provincia','fecha_apertura','count']].groupby(['provincia','fecha_apertura']).sum().reset_index()
df_eval['index'] = df_eval['provincia'] +df_eval['fecha_apertura']


cond = (df['clasificacion_resumen'] == 'Confirmado') | (df['clasificacion_resumen'] == 'Sospechoso')
df_cases = df.loc[cond,['provincia','fecha_apertura','count']].groupby(['provincia','fecha_apertura']).sum().reset_index()
df_cases['index'] = df_cases['provincia'] +df_cases['fecha_apertura']

cond = pd.notna(df['fecha_fallecimiento'])
df_deaths = df.loc[cond,['provincia','fecha_fallecimiento','count']].groupby(['provincia','fecha_fallecimiento']).sum().reset_index()
df_deaths['index'] = df_deaths['provincia'] +df_deaths['fecha_fallecimiento']


#provincias = df['provincia'].drop_duplicates()
#dates = df['fecha_apertura'].drop_duplicates()
#classif = df['clasificacion_resumen'].drop_duplicates()
#df['fecha_fallecimiento'].drop_duplicates()

25*239

df_main = df.loc[:,['provincia', 'fecha_apertura',]].drop_duplicates()

df_main['index'] = df_main['provincia'] + df_main['fecha_apertura']


dict_data = dict(zip( df_eval['index'] , df_eval['count'] ))
df_main['tests'] = df_main['index'].map(dict_data)

dict_data = dict(zip( df_cases['index'] , df_cases['count'] ))
df_main['cases'] = df_main['index'].map(dict_data)

dict_data = dict(zip( df_deaths['index'] , df_deaths['count'] ))
df_main['deaths'] = df_main['index'].map(dict_data)

df_main = df_main.fillna(0)

df_main = df_main.drop(['index'],axis=1)


df_main.to_csv('C:/Users/admin/Downloads/Peru/COVID_ARG_201213.csv',index=False)

del cond, df
