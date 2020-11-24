# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 10:40:03 2020

@author: admin
"""


###############################################################################
###############################################################################
###############################################################################




#    MEXICO


import pandas as pd


file3 = 'C:/Users/admin/Downloads/201123COVID19MEXICO.csv'

version = '100'
path5 = 'C:/Users/admin/Downloads/Peru/Mexico_Hospital_'+version+'.csv'

###############################################################################
###############################################################################

df_MX = pd.read_csv(file3,engine='python')
list(df_MX.columns)
# Only tests data
tests = df_MX.loc[:,['FECHA_INGRESO','ENTIDAD_RES','MUNICIPIO_RES','RESULTADO_LAB']]
tests['tests'] = 1
tests = tests.groupby(['FECHA_INGRESO','ENTIDAD_RES','MUNICIPIO_RES','RESULTADO_LAB']).count().reset_index()

# Creating unique code
df_MX['CODE'] = df_MX['ENTIDAD_RES']*1000 + df_MX['MUNICIPIO_RES']

# Useless columns test removal + new ones
df_MX = df_MX.loc[:,['CODE','SEXO','TIPO_PACIENTE','RESULTADO_LAB','FECHA_INGRESO','FECHA_SINTOMAS',
                     'FECHA_DEF','INTUBADO','NEUMONIA','EDAD','EMBARAZO','DIABETES','EPOC','ASMA','INMUSUPR',
                     'HIPERTENSION','OTRA_COM','CARDIOVASCULAR','OBESIDAD','RENAL_CRONICA','TABAQUISMO',
                     'OTRO_CASO','UCI','PAIS_ORIGEN']]

# Dict to assigne names
mx_sexo = {1:'Mujer',2:'Hombre',99:'N/A'}
mx_paciente = {1:'Ambulat',2:'Hospit',99:'N/A'}
mx_resultado = {1:'Positivo',2:'No positivo',3:'Pendiente'}





# Dicts for naming cities and states
mx_munic = pd.read_csv('C:/Users/admin/Downloads/Peru/Mun_Mexico.csv')
mx_munic['CODE'] = mx_munic['COD_E']*1000 + mx_munic['COD_M']


mx_code1 = mx_munic.set_index('CODE').to_dict()['MUNICIPIO']
mx_code2 = mx_munic.set_index('CODE').to_dict()['ESTADO']

df_MX['MUN'] = df_MX['CODE'].map(mx_code1)
df_MX['EST'] = df_MX['CODE'].map(mx_code2)



#rename = [['mx_sexo','SEXO'],['mx_paciente','TIPO_PACIENTE'],['mx_resultado','RESULTADO'],
#          ['mx_code1','MUN'],['mx_code2','EST']]





#for col in rename:
#    df_MX.loc[:,col[1]] = df_MX.loc[:,col[1]].map(eval(col[0]))


df_MX.to_csv(path5,index=False)


del file3, version, path5, tests, mx_sexo, mx_munic, mx_code1, mx_code2, mx_paciente, mx_resultado
