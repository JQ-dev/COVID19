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


data = data[data['ID de caso'].notnull()]

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


list(data_tests.columns)


data_tests2 = data_tests.drop('ID de caso',axis=1).drop_duplicates()




print('\n\nUltimo registro: ',Ultimo_registro,  '\nTests hasta: ',Ultimo_test)




data_tests2.to_csv('C:/Users/admin/Downloads/COVID COLOMBIA/COVID_COL_01092021.csv',index=False)

del Ultimo_registro, Ultimo_test, data_tests


###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
# SUMMARIZE AND ADD MOBILITY


df = pd.read_csv('C:/Users/admin/Downloads/COVID COLOMBIA/COVID_COL_01092021.csv')

# Removing useless columns
list(df.columns)

remove_col = ['COD_dpto',
 'Cod_D',
 'Cod_M',
 'Código DIVIPOLA',
 'Código DIVIPOLA departamento',
 'Código ISO del país',
 'Edad',
 'Estado',
 'Fecha',
 'Fecha de diagnóstico',
 'Fecha de inicio de síntomas',
 'Fecha de notificación',
 'Fecha de recuperación',
 'ID de caso',
 'MUNICIPIO',
 'Nombre del grupo étnico',
 'Nombre del país',
 'Pertenencia étnica',
 'Recuperado',
 'Sexo',
 'Tipo de contagio',
 'Tipo de recuperación',
 'Ubicación del caso',
 'Unidad de medida de edad',
 'test_Dpto_total',
 'test_Pais_dia',
 'test_Pais_total',
 'DPTO',
 'Poblacion']

df = df.drop(remove_col , axis=1, errors='ignore')
del remove_col

# Cases 

df1 = df.copy()

df1['Cases'] = 1

df1 = df1.drop(['Fecha de muerte'] , axis=1)

df1['Nombre departamento'] = df1['Nombre departamento'].replace('STA MARTA D.E.','MAGDALENA').replace('BARRANQUILLA','ATLANTICO').replace('CARTAGENA','BOLIVAR')


df1 = df1.groupby(['Nombre departamento',
 'Pobl_dep','fecha reporte web']).agg({'Cases':'sum','test_Dpto_dia':'max'}).reset_index()

df1['Nombre departamento'].drop_duplicates()


df1 = df1.rename(columns={'fecha reporte web':'Date'})



# Deaths

df2 = df.copy()
df2['Deaths'] = 1

df2 = df2.drop(['fecha reporte web'] , axis=1)

df2 = df2[df2['Fecha de muerte'].notnull()]

df2['Nombre departamento'] = df2['Nombre departamento'].replace('STA MARTA D.E.','MAGDALENA').replace('BARRANQUILLA','ATLANTICO').replace('CARTAGENA','BOLIVAR')


df2 = df2.groupby(['Nombre departamento','Pobl_dep','Fecha de muerte']).agg({'Deaths':'sum','test_Dpto_dia':'max'}).reset_index()

df2 = df2.rename(columns={'Fecha de muerte':'Date'})

df2 = df2.drop('test_Dpto_dia' , axis=1)

df0 = pd.merge(df1,df2,how='outer',on=['Nombre departamento','Pobl_dep','Date'])

df0['Nombre departamento'].drop_duplicates()



#df = pd.read_csv(path0)

mob = pd.read_csv('C:/Users/admin/Downloads/Global_Mobility_Report.csv')

mob = mob[mob['country_region']=='Colombia']
#list(df.columns)
#list(mob.columns)

mob = mob[mob['sub_region_2'].isnull()]
mob = mob[mob['sub_region_1'].notnull()]



#mob.to_csv('C:/Users/admin/Downloads/COVID COLOMBIA/MOB_COL_210104.csv',index=False)
#



mob = mob.drop(['country_region_code', 'country_region',
 'sub_region_2', 'metro_area', 'iso_3166_2_code',
 'census_fips_code','place_id'],axis=1)

mob.columns =   ['Dpto', 'Date',
 'retail_and_recreation', 'grocery_and_pharmacy',
 'parks', 'transit_stations', 'workplaces', 'residential']  
  


  
mob['Dpto'] = mob['Dpto'].str.upper()

mob['Dpto'].drop_duplicates()

mob['Dpto'] = mob['Dpto'].replace('NORTH SANTANDER','NORTE SANTANDER').replace('SAN ANDRES AND PROVIDENCIA','SAN ANDRES')

mob['Dpto'] = mob['Dpto'].replace('LA GUAJIRA','GUAJIRA').replace('VALLE DEL CAUCA','VALLE').replace('NARINO','NARIÑO')

mob = mob.rename(columns={'Dpto':'Nombre departamento'})

#renaming = [['CALLAO REGION','CALLAO'],['METROPOLITAN MUNICIPALITY OF LIMA','LIMA'],['UNITED ARAB EMIRATES','UAE'],
#           ['CAPE VERDE','CABO VERDE'],['MYANMAR (BURMA)','MYANMAR'],['SOUTH KOREA','S. KOREA'],
#           ['THE BAHAMAS','BAHAMAS'],['CÔTE D\'IVOIRE','IVORY COAST'],['',''],['','']]
#
#
#
#for new_name in renaming:
#    print(new_name[0],new_name[1])
#    mob['country'] = mob['country'].replace(new_name[0],new_name[1])
#
#
#mob = mob.rename(columns={'dates':'FECHA','country':'DEPARTAMENTO DOMICILIO'})
#
#
c_join = pd.merge(df0, mob, how='right', on=['Date','Nombre departamento'])
#



dfIV = pd.read_csv('C:/Users/admin/Downloads/COVID COLOMBIA/Mercado Ivermectina Colombia.csv')


list(dfIV.columns)

dfIV = dfIV[ dfIV['Variable'] == 'Unidades' ]


remove_col = ['Region',
 'Laboratorio',
 'Producto',
 'Tipo Mercado',
 'Tipo Producto',
 'CT IV',
 'Presentacion',
 'Forma Farmacéutica',
 'FACTOR',
 'FF III',
 'Variable']

dfIV = dfIV.drop(remove_col , axis=1)
del remove_col




dfIV = dfIV.groupby(['Departamento','Mes']).sum().reset_index()
dfIV.to_csv(('C:/Users/admin/Downloads/COVID COLOMBIA/COVID_COL_2020IVM.csv'),index=False)
#






c_join.to_csv(('C:/Users/admin/Downloads/COVID COLOMBIA/COVID_COL_01092021210718b.csv'),index=False)
#
#
##del c_df, c_mob
#del c_join, consecutive, df, mob, path1, renaming, new_name
#
#
#

del df,df0,df1,df2,mob,dfIV,data,data0,c_join










