# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:18:46 2020

@author: admin
"""

import pandas as pd
import numpy as np

#######################\n
#data = pd.read_csv('C:/Users/admin/Downloads/COVID COLOMBIA/Casos_positivos_de_COVID-19_en_Colombia.csv')
data0 = pd.read_csv('https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD')
Ultimo_registro = ( '\nCasos: ' + str(data0.iloc[-1,:]['ID de caso']) + ' \nFecha: ' + data0.iloc[-1,:]['fecha reporte web'] )

# list(data.columns)
data = data0.loc[:,:].copy()


data = data.rename(columns={'Código DIVIPOLA municipio':'Código DIVIPOLA'}).copy()

data['Código DIVIPOLA'] = data['Código DIVIPOLA'].replace(27,27001).replace(25,11001)

data['Cod_M'] = data['Código DIVIPOLA']
data['Cod_D'] = data['Código DIVIPOLA'].apply(lambda x : round(x/1000,0))
#data = data.drop('Código DIVIPOLA',axis=1)


data['fecha reporte web'] = pd.to_datetime(data['fecha reporte web'],format="%d/%m/%Y %H:%M:%S")
data['Fecha de notificación'] = pd.to_datetime(data['Fecha de notificación'],format="%d/%m/%Y %H:%M:%S")
data['Fecha de muerte'] = pd.to_datetime(data['Fecha de muerte'],format="%d/%m/%Y %H:%M:%S")
data['Fecha de recuperación'] = pd.to_datetime(data['Fecha de recuperación'],format="%d/%m/%Y %H:%M:%S")
data['Fecha de diagnóstico'] = pd.to_datetime(data['Fecha de diagnóstico'],format="%d/%m/%Y %H:%M:%S")



'''
['fecha reporte web',
 'ID de caso',
 'Fecha de notificación',
 'Código DIVIPOLA departamento',
 'Nombre departamento',
 'Código DIVIPOLA municipio',
 'Nombre municipio',
 'Edad',
 'Unidad de medida de edad',
 'Sexo',
 'Tipo de contagio',
 'Ubicación del caso',
 'Estado',
 'Código ISO del país',
 'Nombre del país',
 'Recuperado',
 'Fecha de inicio de síntomas',
 'Fecha de muerte',
 'Fecha de diagnóstico',
 'Fecha de recuperación',
 'Tipo de recuperación',
 'Pertenencia étnica',
 'Nombre del grupo étnico']
'''

#######################

pop = pd.read_csv('C:/Users/admin/Downloads/COVID COLOMBIA/Pop_Col.csv')

pop = pop.drop(['COD1','COD_dpto','Area','Area_dep'],axis=1)

data_pop = pop.set_index('COD').join(data.set_index('Cod_M'),how='right')

data_pop = data_pop.reset_index(col_fill='COD_M')

data_pop = data_pop.rename(columns={'index':'Cod_M'})

del pop

#######################

#tests = pd.read_csv('C:/Users/admin/Downloads/COVID COLOMBIA/Muestras_procesadas_de_COVID-19_en_Colombia.csv')
tests = pd.read_csv('https://www.datos.gov.co/api/views/8835-5baf/rows.csv?accessType=DOWNLOAD')
Ultimo_test = tests.iloc[-1,:]['Fecha'] 
tests['Atlantico'] = np.where( tests['Barranquilla'].isnull(), tests['Atlantico'], tests['Atlantico'] + tests['Barranquilla'])
tests['Bolivar']   = np.where( tests['Cartagena'].isnull()   , tests['Bolivar']  , tests['Bolivar']   + tests['Cartagena']   )
tests['Magdalena'] = np.where( tests['Santa Marta'].isnull() , tests['Magdalena'], tests['Magdalena'] + tests['Santa Marta'] )




#Fix date Feb
tests = tests.fillna(0).replace('Acumulado Feb','2020-02-28T00:00:00.000')
tests['Diarias'] = tests['Acumuladas']  - tests['Acumuladas'].shift()


# Unpivot departments
tests = pd.pivot_table(tests,columns=['Fecha','Acumuladas','Diarias']).reset_index()


add_code = {'Amazonas':91,'Antioquia':5,'Arauca':81,'Atlantico':8,'Bogota':11,'Bolivar':13,'Boyaca':15,'Caldas':17,'Caqueta':18,
            'Casanare':85,'Cauca':19,'Cesar':20,'Choco':27,'Cordoba':23,'Cundinamarca':25,'Guainia':94,'Guajira':44,'Guaviare':95,
            'Huila':41,'Magdalena':47,'Meta':50,'Narino':52,'Norte de Santander':54,'Putumayo':86,'Quindio':63,'Risaralda':66,
            'San Andres':88,'Santander':68,'Sucre':70,'Tolima':73,'Valle del Cauca':76,'Vaupes':97,'Vichada':99}

tests['COD_depto'] = tests['level_0'].map(add_code)
tests = tests.drop('level_0',axis=1)

tests.columns = ['Fecha','test_Pais_total','test_Pais_dia','test_Dpto_total','COD_dpto']

tests['test_Dpto_dia'] = tests['test_Dpto_total']  - tests['test_Dpto_total'].shift()
tests.loc[ (tests.loc[:,'test_Dpto_dia'] < 0) , 'test_Dpto_dia' ] = 0




#######################
tests['Fecha'] = pd.to_datetime(tests['Fecha'],format="%Y-%m-%d %H:%M:%S.%f")
####tests['Fecha'] = tests['Fecha'].apply(lambda x : x[0:10])
tests.index = tests['Fecha'].apply(str)+ tests['COD_dpto'].apply(str)

#######data_pop['fecha reporte web'] = data_pop['fecha reporte web'].apply(lambda x : x[0:10])
data_pop.index = data_pop['fecha reporte web'].apply(str)+ data_pop['Cod_D'].apply(str)




data_tests = data_pop.join(tests,how='left')
data_tests = data_tests.sort_index(axis=1)

data_tests['Cod_M'] = data_tests['Cod_M'].apply(lambda x : '0'+str(x) if ( len(str(x)) == 4 ) else str(x))


del add_code, data_pop, tests












###############################################################################
###############################################################################
###############################################################################










'''
###############################################################################
###############################################################################

import pandas as pd
import numpy as np


#total = pd.read_csv('https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD')
total = data.copy()


total = total.rename(columns={'Código DIVIPOLA municipio':'Código DIVIPOLA'})

total['Fecha de muerte'] = total['Fecha de muerte'].fillna(0)
total['Código DIVIPOLA'] = total['Código DIVIPOLA'].replace(5,5001)
total['COD_D'] = total['Código DIVIPOLA'].apply(lambda x : np.floor(x/1000) )


deaths = total.loc[ (total.loc[:,'Fecha de muerte'] != 0) ,('COD_D','Fecha de muerte')]
deaths['DEATHS'] = 1  
deaths = deaths.rename(columns={'Fecha de muerte':'DATE'})

deaths = deaths.groupby(['COD_D','DATE']).count().reset_index()

#list(deaths.columns)
#list(total.columns)
cases = total.loc[ : ,('COD_D','Fecha de inicio de síntomas')]
cases['CASES'] = 1   
cases = cases.rename(columns={'Fecha de inicio de síntomas':'DATE'})
cases = cases.loc[ cases.loc[:,'DATE']!= 'Asintomático' , :]


cases = cases.groupby(['COD_D','DATE']).count().reset_index()

total = pd.merge(cases,deaths,how='outer',on=['COD_D','DATE'])

total = total.fillna(0)

#total['DATE'] = pd.to_datetime( total['DATE'] )


dates = total['DATE'].drop_duplicates()
dptos = total['COD_D'].drop_duplicates()


for dpto in dptos:
    for date in dates:
        if date not in list(total.loc[ total.loc[:,'COD_D'] == dpto ,'DATE']):
            temp = pd.DataFrame([[dpto,date,0,0]], columns=list(total.columns))
            total = total.append(temp)
        else:
            continue


#list(database.columns)




for dpto in dptos:
    #dpto = dptos[0]
    temp = total.loc[ total.loc[:,'COD_D']==dpto ,['CASES','DEATHS','DATE']]
    
    new_cols = [['CASES','cum_cases'],['DEATHS','cum_deaths']]
    #col = ['CASES','cum_cases']
    for col in new_cols:
        temp = total.loc[ total.loc[:,'COD_D']==dpto ,[col[0],'DATE']].sort_values(by=['DATE'])
        
        temp_dict = dict(zip( temp['DATE'] , np.cumsum(temp[col[0]]) ))
        
        total.loc[ total.loc[:,'COD_D']==dpto ,col[1]] = total.loc[ total.loc[:,'COD_D']==dpto ,'DATE'].map(temp_dict)




pop = pd.read_csv('C:/Users/admin/Downloads/COVID COLOMBIA/Pop_Col.csv')

name_d = dict(zip(pop['COD_dpto'],pop['DPTO']))
pop_d = dict(zip(pop['COD_dpto'],pop['Pobl_dep']))



total['Pop']  =  total['COD_D'].map(pop_d)
total['State'] = total['COD_D'].map(name_d)

COVID_COL = total.drop(['COD_D'],axis=1)


COVID_COL.to_csv('C:/Users/admin/Downloads/Peru/Colombia_COVID_99.csv',index=False)

del cases, col, date, dates, deaths, dpto, dptos, name_d, new_cols, pop, pop_d, temp, temp_dict, total
'''

print('\n\nUltimo registro: ',Ultimo_registro,  '\nTests hasta: ',Ultimo_test)

data_tests.to_csv('C:/Users/admin/Downloads/COVID COLOMBIA/COVID_COL_201224.csv',index=False)

del Ultimo_registro, Ultimo_test, data_tests









