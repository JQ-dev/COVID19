# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 10:19:17 2020

@author: juanjchamie@gmail.com
"""

import pandas as pd
import numpy as np
import scipy.stats


file1 = 'C:/Users/admin/Downloads/SINADEF_DATOS_ABIERTOS_19102020.xlsx'

#######################\
# Read from the path - It takes long because it is a excel file
fallecidosX = pd.read_excel(file1, sheet_name='Tabla_SINADEF',usecols='A:AE',skiprows=3)

del file1

fallecidos = fallecidosX.copy()



# Changing babies age from months to 0 ages
fallecidos.loc[ fallecidos['TIEMPO EDAD'] != 'AÑOS'  ,'EDAD'] = 0
fallecidos = fallecidos.drop(['TIEMPO EDAD'],axis=1)

fallecidos = fallecidos[(fallecidos.loc[:,'EDAD'] != 'SIN REGISTRO')]


#fallecidos.loc[fallecidos['ESTADO CIVIL']=='SEPARADO','EDAD'].mean()

# Rounding age
fallecidos['EDAD'] = fallecidos['EDAD'].astype(float)
fallecidos = fallecidos[ fallecidos['EDAD'] >= 60]


# Formatting date
fallecidos['FECHA'] = pd.to_datetime(fallecidos['FECHA'])

# Grouping weeks
#fallecidos['WEEK'] = fallecidos['FECHA'] - pd.to_timedelta(fallecidos['FECHA'].dt.dayofweek, unit='d')


# LIMA
list(fallecidos.columns)
a = fallecidos['DEPARTAMENTO DOMICILIO'] == 'LIMA'
b = fallecidos['PROVINCIA DOMICILIO'] != 'LIMA'
c = a&b == False

# Remove Dep Lima Prov No Lima
fallecidos = fallecidos.loc[ c ,:]

# Convert distr to province in Lima
fallecidos.loc[a,'PROVINCIA DOMICILIO'] = fallecidos.loc[a,'DISTRITO DOMICILIO']


# Adding values without district
fallecidos['COUNT'] = 1

fallecidos = fallecidos.groupby(['DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','FECHA']).sum().reset_index()

fallecidos = fallecidos.drop(['Nº','EDAD','AÑO','MES'],axis=1)


# Case Number

fallecidos['CASE'] = 0

case_lists = [['LIMA','SAN MARTIN DE PORRES',1],
              ['LIMA','SAN JUAN DE LURIGANCHO',2],
              ['LIMA','LIMA',3],
              ['LIMA','SAN JUAN DE MIRAFLORES',4],
              ['LIMA','SANTA ANITA',5],
              ['JUNIN','HUANCAYO',1],
              ['PIURA','PIURA',2],
              ['CUSCO','CUSCO',3],
              ['UCAYALI','CORONEL PORTILLO',4],
              ['LORETO','MAYNAS',5]         
             ]



for case in case_lists:
    a = fallecidos['DEPARTAMENTO DOMICILIO'] == case[0]
    b = fallecidos['PROVINCIA DOMICILIO'] == case[1]
    fallecidos.loc[a&b,'CASE'] = case[2]


fallecidos = fallecidos[fallecidos['CASE']!=0]





## Population -
#poblacion = pd.read_csv('C:/Users/admin/Downloads/Peru/Pobl Peru.csv',sep=',')
#poblacion = poblacion.drop(['UB1','UB2','UBIGEO','DISTRITO','PROVINCIA','Mas de 60','Promedio','Total','0','10','20','30','40','50'],axis=1)
#
#
## Removing districts and provinces
#poblacion = poblacion.groupby(['DEPARTAMENTO']).sum().reset_index()
#
#poblacion['60+'] = poblacion['60'] + poblacion['70'] + poblacion['80']
#poblacion = poblacion.drop(['60','70','80'],axis=1)
#
#
#
#
#
#
## Joining *****
#
#fallecidos = fallecidos.rename(columns={'DEPARTAMENTO DOMICILIO':'DEPARTAMENTO'})
#
#
#fallecidos = pd.merge(fallecidos, poblacion, how='left',on=['DEPARTAMENTO'])
#
#
#del poblacion, fallecidosX
###############################################################################
###############################################################################
from scipy import stats
import matplotlib.pyplot as plt

a = fallecidos['CASE'] == 1
b1 = fallecidos['DEPARTAMENTO DOMICILIO'] == 'LIMA'
b2 = fallecidos['DEPARTAMENTO DOMICILIO'] != 'LIMA'
c = fallecidos['FECHA'] < '2020-01-01 00:00:00' 

x1 = fallecidos.loc[a&b1&c,'COUNT']
x2 = fallecidos.loc[a&b2&c,'COUNT']

stats.kstest
#kstest(rvs, cdf, args=(), N=20, alternative='two-sided', mode='approx')
scipy.


plt.figure(figsize=(9,6))
plt.plot(x1,'.')
plt.plot(x2,'+')

sorted_val = np.sort(x1)
scaled_val = (sorted_val-sorted_val.mean())/sorted_val.std()

#from scipy.stats.kde import gaussian_kde
#from numpy import linspace
#
#import statsmodels.api as sm



a = fallecidos['DEPARTAMENTO'] == 'LIMA'
b = fallecidos['WEEK'] < '2020-04-05 00:00:00' 
c = fallecidos['WEEK'] > '2017-01-01 00:00:00'

x = fallecidos.loc[ a&b&c ,['COUNT']]

# histogram
plt.hist(x['COUNT'])




# estimate the probability density function (PDF)
kde = gaussian_kde(x)
# return evenly spaced numbers over a specified interval
dist_space = linspace(min(x), max(x), 100)
# plot the results
plt.plot(dist_space, kde(dist_space))



stats.probplot(x, plot=plt)



y = fallecidos.loc[ a&b&c ,['WEEK']]


ols = sm.OLS(y, x).fit()
print(ols.summary())












plt.figure(figsize=(9,6))














