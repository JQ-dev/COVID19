

import pandas as pd



file3 = 'D:/211108COVID19MEXICO.csv'

version = '202'
path5 = 'D:/Mexico_Hospital_'+version+'.csv'

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
                     'FECHA_DEF','EDAD','UCI','SECTOR']]

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



# Basic MEXICO
#
#cases = pd.read_csv('C:/Users/admin/Downloads/Casos_Diarios_Estado_Nacional_Confirmados_20210727.csv')
#deaths =  pd.read_csv('C:/Users/admin/Downloads/Casos_Diarios_Estado_Nacional_Defunciones_20210727.csv')
#
#cases = cases.drop(['cve_ent'],axis=1)
#cases = cases.set_index()






mob = pd.read_csv('C:/Users/admin/Downloads/Global_Mobility_Report.csv',sep=',')


mob.columns
#Filter Countries
mob = mob.loc[ mob['country_region_code'] == 'MX' , : ]

# Rrmove region 2 and whole country
#cond = mob.loc[:,'sub_region_1'].notna()
#mob1 = mob1.loc[ cond , : ]
#
#cond = mob.loc[:,'sub_region_2'].isna()
#mob1 = mob1.loc[ cond , : ]

path5 = 'D:/Mexico_Hospital_'+version+'_mob.csv'

mob.to_csv(path5,index=False)


del file3, version, path5, tests, mx_sexo, mx_munic, mx_code1, mx_code2, mx_paciente, mx_resultado, df_MX


del mob


