# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 12:29:49 2020

@author: admin
"""

import pandas as pd
import numpy as np
import scipy.stats


file1 = 'C:/Users/admin/Downloads/COVID19Casos (9).csv'

#######################\
# Read from the path - It takes long because it is a excel file
df = pd.read_csv(file1)

del file1

list(df.columns)

df['count'] = 1

df['fallecido'] = df['fallecido'].replace('NO',0).replace('SI',1)


df = df.loc[:,['residencia_departamento_nombre', 'residencia_provincia_nombre','fecha_apertura','fecha_fallecimiento','clasificacion_resumen','fecha_diagnostico','count']]


df = df.rename(columns={'residencia_provincia_nombre':'provincia','residencia_departamento_nombre':'departamento','clasificacion_resumen':'clasif'})
df['index'] = df['departamento'] + df['provincia'] + df['fecha_apertura']


df_eval = df.loc[:,['clasif','provincia','fecha_apertura','count']].groupby(['clasif','provincia','fecha_apertura']).sum().reset_index()
df_eval['index'] = df['departamento'] + df_eval['provincia'] +df_eval['fecha_apertura']


#cond = (df['clasificacion_resumen'] == 'Confirmado') | (df['clasificacion_resumen'] == 'Sospechoso')
cond = df['clasif'] != 'x'

df_cases = df.loc[cond,['clasif','departamento','provincia','fecha_apertura','count']].groupby(['clasif','departamento','provincia','fecha_apertura']).sum().reset_index()
df_cases['index'] = df_cases['departamento'] + df_cases['provincia'] +df_cases['fecha_apertura']

cond = pd.notna(df['fecha_fallecimiento'])
df_deaths = df.loc[cond,['clasif','departamento','provincia','fecha_fallecimiento','count']].groupby(['clasif','departamento','provincia','fecha_fallecimiento']).sum().reset_index()
df_deaths['index'] = df_deaths['departamento'] + df_deaths['provincia'] +df_deaths['fecha_fallecimiento']


#provincias = df['provincia'].drop_duplicates()
#dates = df['fecha_apertura'].drop_duplicates()
#classif = df['clasificacion_resumen'].drop_duplicates()
#df['fecha_fallecimiento'].drop_duplicates()

25*239

df_main = df.loc[:,['clasif','departamento','provincia', 'fecha_apertura',]].drop_duplicates()

df_main['index'] = df_main['departamento'] +df_main['provincia'] + df_main['fecha_apertura']


dict_data = dict(zip( df_eval['index'] , df_eval['count'] ))
df_main['tests'] = df_main['index'].map(dict_data)

dict_data = dict(zip( df_cases['index'] , df_cases['count'] ))
df_main['cases'] = df_main['index'].map(dict_data)

dict_data = dict(zip( df_deaths['index'] , df_deaths['count'] ))
df_main['deaths'] = df_main['index'].map(dict_data)

df_main = df_main.fillna(0)

df_main = df_main.drop(['index'],axis=1)


df_main.to_csv('C:/Users/admin/Downloads/Peru/COVID_ARG_210105.csv',index=False)

del cond, df
