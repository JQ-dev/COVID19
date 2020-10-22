# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:56:04 2020

@author: admin
"""


file1 = 'C:/Users/admin/Downloads/SINADEF_DATOS_ABIERTOS_19102020.xlsx'
file2 = 'C:/Users/admin/Downloads/HIST_PAINEL_COVIDBR_19out2020.csv'
file3 = 'C:/Users/admin/Downloads/201019COVID19MEXICO.csv'

version = '90'

path0 = 'C:/Users/admin/Downloads/Peru/Peru_deaths_'+version+'.csv'
path1 = 'C:/Users/admin/Downloads/Peru/fallecidos_Peru_XX'+version+'.csv'
path2 = 'C:/Users/admin/Downloads/Peru/Peru_COVID_'+version+'.csv'
path3 = 'C:/Users/admin/Downloads/Peru/Peru_Sala_Situacional_'+version+'.csv'

path4 = 'C:/Users/admin/Downloads/Peru/Brasil_COVID_'+version+'.csv'
 
path5 = 'C:/Users/admin/Downloads/Peru/Mexico_Hospital_'+version+'.csv'

path6 = 'C:/Users/admin/Downloads/Peru/Global_Mobility_Report_'+version+'.csv'






import pandas as pd
import numpy as np

#######################\n

fallecidosX = pd.read_excel(file1, sheet_name='Tabla_SINADEF',usecols='A:AE',skiprows=3)

fallecidos = fallecidosX.loc[ fallecidosX.loc[:,'MUERTE VIOLENTA']=='SIN REGISTRO' ,:]

fallecidos.loc[ fallecidos.loc[:,'TIEMPO EDAD'] != 'AÑOS'  ,'EDAD'] = 0
fallecidos = fallecidos.loc[ fallecidos.loc[:,'EDAD']!='SIN REGISTRO' ,:]
fallecidos['EDAD'] = fallecidos['EDAD'].apply(lambda x : np.floor( int(x) / 10 )*10 )
fallecidos.loc[ fallecidos.loc[:,'EDAD'] > 80  ,'EDAD'] = 80

fallecidos['FECHA'] = pd.to_datetime(fallecidos['FECHA'])
fallecidos['WEEK'] = fallecidos['FECHA'].dt.week
fallecidos['YEAR'] = fallecidos['FECHA'].dt.year


# New age groups
promedios = fallecidos.loc[ fallecidos.loc[:,'EDAD'] > 29 , ['YEAR','EDAD','SEXO','DEPARTAMENTO DOMICILIO','WEEK']]

promedios['COUNT'] = 1

promedios = promedios.groupby(['YEAR','EDAD','SEXO','DEPARTAMENTO DOMICILIO','WEEK']).count().reset_index()

# dpto
test = promedios.groupby(['YEAR','WEEK','DEPARTAMENTO DOMICILIO']).agg({'COUNT':['sum']}).reset_index().droplevel(level=1,axis=1)
test2 = test.groupby(['DEPARTAMENTO DOMICILIO']).agg({'COUNT':['sum','mean','std','count']}).droplevel(level=0,axis=1)

prom_muertes = test2.loc[:,['mean','std']].reset_index()


fallecidos1 = fallecidos.loc[:,('DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','FECHA')]
fallecidos2 = fallecidos.loc[:,('DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','EDAD','FECHA','SEXO')]

# Older than 29
fallecidos = fallecidos.loc[ fallecidos.loc[:,'EDAD'] > 29 ,:]


#list(fallecidos.columns)


fallecidos3 = pd.DataFrame()
fallecidos4 = fallecidos.loc[:,:]
respir = ['COVID','SARS','RESPIRAT','PULMON','19','NEUMON','BRONCO','BRONQU']

# INCLUDING
for clue in respir:
    cond1 = fallecidos4.loc[:,'DEBIDO A (CAUSA A)'].apply(lambda x : clue in x )
    cond2 = fallecidos4.loc[:,'DEBIDO A (CAUSA A)'].apply(lambda x : clue not in x )
    fallecidos3 = fallecidos3.append(fallecidos4.loc[cond1,:] )    
    fallecidos4 = fallecidos4.loc[cond2,:]

for clue in respir:
    cond1 = fallecidos4.loc[:,'DEBIDO A (CAUSA B)'].apply(lambda x : clue in x )
    cond2 = fallecidos4.loc[:,'DEBIDO A (CAUSA B)'].apply(lambda x : clue not in x )
    fallecidos3 = fallecidos3.append(fallecidos4.loc[cond1,:] )    
    fallecidos4 = fallecidos4.loc[cond2,:]





Peru_deaths=fallecidos4.loc[:,['EDAD','DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','FECHA']]
Peru_deaths['cuenta'] = 1   
Peru_deaths = Peru_deaths.groupby(['EDAD','DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','FECHA']).count().reset_index()



poblacion = pd.read_csv('C:/Users/admin/Downloads/Peru/Pobl Peru.csv',sep=',')
poblacion = poblacion.drop(['UB1','UB2','UBIGEO','DISTRITO','10','20','0','Mas de 60','Promedio','Total'],axis=1)
poblacion['60+'] = poblacion.loc[:,['60','70','80']].sum(axis=1)




dptos2 = ( poblacion.groupby(['DEPARTAMENTO','PROVINCIA']).sum()).reset_index()
dptos2b = ( poblacion.groupby(['DEPARTAMENTO']).sum()).reset_index()
dptos2b['PROVINCIA'] = 'Total'


dptos = dptos2.append(dptos2b)


dptos = dptos.melt(id_vars=['DEPARTAMENTO','PROVINCIA'], var_name='EDAD', value_name='Pobl')


dptos['Dep_Prov'] = dptos['DEPARTAMENTO'] + '-' + dptos['PROVINCIA'] + '-' + dptos['EDAD']

dptos = dptos.drop(['DEPARTAMENTO','PROVINCIA','EDAD'],axis=1)



#list(Peru_deaths.columns)

Peru_deaths_D = ( Peru_deaths.groupby(['DEPARTAMENTO DOMICILIO','FECHA']).agg({'cuenta':sum})).reset_index()
Peru_deaths_D['PROVINCIA DOMICILIO'] = 'Total'
Peru_deaths_D['EDAD'] = '60+.0'

Peru_deaths_D2 = ( Peru_deaths.groupby(['DEPARTAMENTO DOMICILIO','FECHA','PROVINCIA DOMICILIO']).agg({'cuenta':sum})).reset_index()
Peru_deaths_D2['EDAD'] = '60+.0'

Peru_deaths_A = ( Peru_deaths.groupby(['DEPARTAMENTO DOMICILIO','FECHA','EDAD']).agg({'cuenta':sum})).reset_index()
Peru_deaths_A['PROVINCIA DOMICILIO'] = 'Total'

Peru_deaths_final = Peru_deaths.append(Peru_deaths_D)

Peru_deaths_final = Peru_deaths_final.append(Peru_deaths_D2)
Peru_deaths_final = Peru_deaths_final.append(Peru_deaths_A)


Peru_deaths_final['EDAD'] = Peru_deaths_final['EDAD'].apply(lambda x : str(x)[:-2])


Peru_deaths_final['Dep_Prov'] = (Peru_deaths_final['DEPARTAMENTO DOMICILIO'] + '-' + 
                                Peru_deaths_final['PROVINCIA DOMICILIO'] + '-' + Peru_deaths_final['EDAD'])



Peru_deaths_final = pd.merge(Peru_deaths_final,dptos,on=['Dep_Prov'],how='left')


Peru_deaths_final = Peru_deaths_final.drop(['Dep_Prov'],axis=1)



Peru_deaths_final.to_csv(path0,index=False)

#
#
#fallecidos2['cuenta'] = 1                               
#
#sexo_edad = fallecidos2.groupby(['DEPARTAMENTO DOMICILIO','EDAD','FECHA','SEXO']).count().reset_index()
#sexo_edad = sexo_edad.drop(['PROVINCIA DOMICILIO'],axis=1)
#
#sin_edad = fallecidos2.groupby(['DEPARTAMENTO DOMICILIO','PROVINCIA DOMICILIO','FECHA']).count().reset_index()
#sin_edad = sin_edad.drop(['EDAD','SEXO'],axis=1)
#
#





###############################################################################

# POPULATION
#
#poblacion = pd.read_csv('C:/Users/admin/Downloads/Peru/Pobl Peru.csv',sep=',')
#poblacion = poblacion.drop(['UB1','UB2','UBIGEO','0','10','20','30','40','50','60','70','80'],axis=1)
#
#poblacion['Mas de 60'] = poblacion['Mas de 60'].replace('%','',regex=True).apply(float)
#poblacion['Prom_x_Pob'] = poblacion['Promedio'] * poblacion['Total']
#
#poblacion['Mas de 60'] = poblacion['Mas de 60'] / 100
#poblacion['60+'] = poblacion['Mas de 60'] * poblacion['Total'] 
#
#
#
#
#dptos = ( poblacion.groupby('DEPARTAMENTO', as_index=False)
#                .agg({  'Total':sum, '60+':sum, 'Prom_x_Pob':sum} ) )
#
#dptos['Mas de 60'] = dptos['60+'] / dptos['Total']
#dptos['Promedio'] = dptos['Prom_x_Pob'] / dptos['Total']
#
#
#provincia = ( poblacion.groupby(['DEPARTAMENTO','PROVINCIA'], as_index=False)
#                .agg({  'Total':sum, '60+':sum, 'Prom_x_Pob':sum} ) )
#
#provincia['Mas de 60'] = provincia['60+'] / provincia['Total']
#provincia['Promedio'] = provincia['Prom_x_Pob'] / provincia['Total']
#
#pobl = pd.concat([poblacion,dptos,provincia])
#
#dptos['prom_fallec'] = dptos['DEPARTAMENTO'].map( dict(zip(prom_muertes['DEPARTAMENTO DOMICILIO'],prom_muertes['mean']))  )
#dptos['std_fallec'] =  dptos['DEPARTAMENTO'].map( dict(zip(prom_muertes['DEPARTAMENTO DOMICILIO'],prom_muertes['std']))  )
#

#########################################dptos######################################

# add data with ZIP and MAP

#pairs = (['DEPARTAMENTO','Total'],['DEPARTAMENTO','Mas de 60'],['DEPARTAMENTO','Promedio'],
#         ['DEPARTAMENTO','prom_fallec'],['DEPARTAMENTO','std_fallec'])
#
#for data in pairs:
#    temp_dic = dict(zip( dptos[data[0]], dptos[data[1]]))
#    sin_edad[data[1]] = sin_edad['DEPARTAMENTO DOMICILIO'].map(temp_dic)
#
#
#for data in pairs:
#    temp_dic = dict(zip( dptos[data[0]], dptos[data[1]]))
#    sexo_edad[data[1]] = sexo_edad['DEPARTAMENTO DOMICILIO'].map(temp_dic)
#
#
#
#sexo_edad.to_csv(path1,index=False)
#
##sin_edad.to_csv('C:/Users/admin/Downloads/Peru/fallecidos_Peru_X11.csv',index=False)
#
#
#
#del fallecidos1, fallecidos2, sin_edad, sexo_edad, pairs, temp_dic
#fallecidos

###############################################################################
###############################################################################
###############################################################################




# PERU SHORRT






###############################################################################
###############################################################################

try:
    deaths = pd.read_csv('https://cloud.minsa.gob.pe/s/Md37cjXmjT9qYSa/download',sep=',',engine='python')
    #deaths = pd.read_csv('C:/Users/admin/Downloads/Peru/fallecidos_covid.csv',sep=',')
    
    cases = pd.read_csv('https://cloud.minsa.gob.pe/s/Y8w3wHsEdYQSZRp/download',sep=',',engine='python')
    #cases = pd.read_csv('C:/Users/admin/Downloads/Peru/positivos_covid.csv',sep=',')
    
    
    deaths = deaths.drop(['UUID','EDAD_DECLARADA','SEXO','FECHA_NAC','DISTRITO','PROVINCIA'],axis=1)
    deaths['DEATHS'] = 1    
    
    cases = cases.drop(['UUID','EDAD','SEXO','METODODX','DISTRITO','PROVINCIA'],axis=1)
    cases['CASES'] = 1    
    
    cases['FECHA_RESULTADO'] = cases['FECHA_RESULTADO'].replace('6/12/2020','12/06/2020').replace('6/11/2020','11/06/2020')
    
    
    cases = cases.groupby(['FECHA_RESULTADO','DEPARTAMENTO'], as_index=False).count()
    
    cases = cases.rename(columns={'FECHA_RESULTADO':'DATE'})
    
    deaths = deaths.groupby(['FECHA_FALLECIMIENTO','DEPARTAMENTO'], as_index=False).count()
    
    deaths = deaths.rename(columns={'FECHA_FALLECIMIENTO':'DATE'})
    
    
    
    total = pd.merge(cases, deaths, how='left', on=['DATE','DEPARTAMENTO'])
    
    
    
    
    total['DEATHS'] = total['DEATHS'].fillna(0)
    
    
    
    total['DATE'] = pd.to_datetime(total['DATE'],format="%Y%m%d")
    
    
    
    total['cum_cases'] = 0
    total['cum_deaths'] = 0
        
        
    dptos = total['DEPARTAMENTO'].drop_duplicates()
    #list(database.columns)
    
    for dpto in dptos:
        #dpto = dptos[0]
        temp = total.loc[ total.loc[:,'DEPARTAMENTO']==dpto ,['CASES','DEATHS','DATE']]
        
        new_cols = [['CASES','cum_cases'],['DEATHS','cum_deaths']]
        #col = ['CASES','cum_cases']
        for col in new_cols:
            temp = total.loc[ total.loc[:,'DEPARTAMENTO']==dpto ,[col[0],'DATE']].sort_values(by=['DATE'])
            
            temp_dict = dict(zip( temp['DATE'] , np.cumsum(temp[col[0]]) ))
            
            total.loc[ total.loc[:,'DEPARTAMENTO']==dpto ,col[1]] = total.loc[ total.loc[:,'DEPARTAMENTO']==dpto ,'DATE'].map(temp_dict)
    
    
    
    # POPULATION
    
    
    pop = pd.read_csv('C:/Users/admin/Downloads/Peru/Pobl Peru.csv',sep=',')
    
    pop = pop.loc[ :,['DEPARTAMENTO','Total'] ]
    
    pop = pop.groupby('DEPARTAMENTO').sum().reset_index()
    
    pop = dict(zip(pop['DEPARTAMENTO'],pop['Total']))
    
    total['pop'] = total['DEPARTAMENTO'].map(pop)
    
    
    total.to_csv(path2,index=False)

except:
    print('Peru short with problems')


###############################################################################
###############################################################################
###############################################################################




# PERU TESTS






###############################################################################
###############################################################################



dates = [
         '01052020.xlsx','02052020.xlsx','03052020.xlsx','04052020.xlsx','05052020.xlsx','06052020.xlsx','07052020.xlsx','08052020.xlsx','09052020.xlsx','10052020.xlsx',
         '11052020.xlsx','12052020.xlsx','13052020.xlsx','14052020.xlsx','15052020.xlsx','16052020.xlsx','17052020.xlsx','18052020.xlsx','19052020.xlsx','20052020.xlsx',
         '21052020.xlsx','22052020.xlsx','23052020.xlsx','24052020.xlsx','25052020.xlsx','26052020.xlsx','27052020.xlsx','28052020.xlsx','29052020.xlsx','30052020.xlsx','31052020.xlsx',
         '01062020.xlsx','02062020.xlsx','03062020.xlsx','04062020.xlsx','05062020.xlsx','06062020.xlsx','07062020.xlsx','08062020.xlsx','09062020.xlsx','10062020.xlsx',
         '11062020.xlsx','12062020.xlsx','13062020.xlsx','14062020.xlsx','15062020.xlsx','16062020.xlsx','17062020.xlsx','18062020.xlsx','19062020.xlsx','20062020.xlsx',
         '21062020.xlsx','22062020.xlsx','23062020.xlsx','24062020.xlsx','25062020.xlsx','26062020.xlsx','27062020.xlsx','28062020.xlsx','29062020.xlsx','30062020.xlsx',
         '01072020.xlsx','02072020.xlsx','03072020.xlsx','04072020.xlsx','05072020.xlsx','06072020.xlsx','07072020.xlsx','08072020.xlsx','09072020.xlsx','10072020.xlsx',
         '11072020.xlsx','12072020.xlsx','13072020.xlsx','14072020.xlsx','15072020.xlsx','16072020.xlsx','17072020.xlsx','18072020.xlsx','19072020.xlsx','20072020.xlsx',
         '21072020.xlsx','22072020.xlsx','23072020.xlsx','24072020.xlsx','25072020.xlsx','26072020.xlsx','27072020.xlsx','28072020.xlsx','29072020.xlsx','30072020.xlsx','31072020.xlsx',
         '01082020.xlsx','02082020.xlsx','03082020.xlsx','04082020.xlsx','05082020.xlsx','06082020.xlsx','07082020.xlsx','08082020.xlsx','09082020.xlsx','10082020.xlsx',
         '11082020.xlsx','12082020.xlsx','13082020.xlsx','14082020.xlsx','15082020.xlsx','16082020.xlsx','17082020.xlsx','18082020.xlsx','19082020.xlsx','20082020.xlsx',
         '21082020.xlsx','22082020.xlsx','23082020.xlsx','24082020.xlsx','25082020.xlsx','26082020.xlsx','27082020.xlsx','28082020.xlsx','29082020.xlsx','30082020.xlsx','31082020.xlsx',
         '01092020.xlsx','02092020.xlsx','03092020.xlsx','04092020.xlsx','05092020.xlsx','06092020.xlsx','07092020.xlsx','08092020.xlsx','09092020.xlsx','10092020.xlsx',
         '11092020.xlsx','12092020.xlsx','13092020.xlsx','14092020.xlsx','15092020.xlsx','16092020.xlsx','17092020.xlsx','18092020.xlsx','19092020.xlsx','20092020.xlsx',
         '21092020.xlsx','22092020.xlsx','23092020.xlsx','24092020.xlsx','25092020.xlsx','26092020.xlsx','27092020.xlsx','28092020.xlsx','29092020.xlsx','30092020.xlsx',
         '01102020.xlsx','02102020.xlsx','03102020.xlsx','04102020.xlsx','05102020.xlsx','06102020.xlsx','07102020.xlsx','08102020.xlsx','09102020.xlsx','10102020.xlsx',
         '11102020.xlsx','12102020.xlsx','13102020.xlsx','14102020.xlsx','15102020.xlsx','16102020.xlsx','17102020.xlsx','18102020.xlsx','19102020.xlsx','20102020.xlsx',
         '21102020.xlsx','22102020.xlsx','23102020.xlsx','24102020.xlsx','25102020.xlsx','26102020.xlsx','27102020.xlsx','28102020.xlsx','29102020.xlsx','30102020.xlsx','31102020.xlsx']         
         #fil = 'https://github.com/jincio/COVID_19_PERU/raw/master/data/descargas_sala_situacional/POSITIVIDAD_'

def covid_peru(fil,dates):
    new_data = []
    
    for date in dates:
        file = fil + date
        try:
            temp = pd.read_excel(file)
            temp['date'] = date
            new_data.append(temp)
            #print(date, ' FILE IMPORTED')
        except:
            #print(date, ' FILE NO AVAILABLE')
            continue
    
    
    todos = pd.DataFrame()
    
    for each in new_data:
        try:
            todos = todos.append(each)
        except:
            continue
    
    return todos

def repl_date(df):
    df['date'] = df['date'].replace('.xlsx','',regex=True)
    df['date'] = pd.to_datetime(df['date'],format='%d%m%Y')
    return df


Peru_uci = covid_peru('https://github.com/jincio/COVID_19_PERU/raw/master/data/descargas_sala_situacional/UCI_',dates)
Peru_uci = Peru_uci.groupby('date').agg({'En Uso':sum,'Disponible':sum})
Peru_uci = Peru_uci.rename(columns={'En Uso':'UCI En Uso','Disponible':'UCI Disponible'}).reset_index()
Peru_uci = repl_date(Peru_uci)
#ok


Peru_hosp = covid_peru('https://github.com/jincio/COVID_19_PERU/raw/master/data/descargas_sala_situacional/HOSPITALIZADOS_',dates)
cond = Peru_hosp.loc[:,'CATEGORIA'] == 'USO DE VENTILACION MECÁNICA'
Peru_hosp.loc[cond,'CATEGORIA'] = Peru_hosp.loc[cond,'DETALLE']
cond = Peru_hosp.loc[:,'CATEGORIA'] == 'EVOLUCIÓN'
Peru_hosp.loc[cond,'CATEGORIA'] = Peru_hosp.loc[cond,'DETALLE']
Peru_hosp = Peru_hosp.drop('DETALLE',axis=1)
Peru_hosp = Peru_hosp.groupby(['CATEGORIA','date']).agg({'TOTAL':sum}).reset_index()
Peru_hosp['CATEGORIA']['CATEGORIA'] = Peru_hosp['CATEGORIA'].apply(lambda x : 'HOSP ' + x)
Peru_hosp = Peru_hosp.pivot(index='date',columns='CATEGORIA',values='TOTAL').reset_index()
Peru_hosp = repl_date(Peru_hosp)
#ok


Peru_casos = covid_peru('https://github.com/jincio/COVID_19_PERU/raw/master/data/descargas_sala_situacional/CASOS_',dates)
Peru_casos['Dpto'] = Peru_casos['Departamento'].where( Peru_casos['Región'].isna(), Peru_casos['Región'] )
Peru_casos['Dpto'] = Peru_casos['Dpto'].replace('LIMA METROPOLITANA','LIMA').replace('LIMA REGIÓN','LIMA')

Peru_casos = Peru_casos.drop(['PCR   (+)','PRUEBA RÁPIDA (+)','Pais','LETALIDAD (%)','Departamento','Región'],axis=1)

Peru_casos = Peru_casos.groupby(['Dpto','date']).sum().reset_index()

Peru_casos = repl_date(Peru_casos)
Peru_casos = Peru_casos.sort_values(['Dpto','date'])

Peru_casos2 = Peru_casos.loc[:,['TOTAL CASOS (+)','FALLECIDOS']].diff()
Peru_casos2 = Peru_casos2.rename(columns={'TOTAL CASOS (+)':'CASOS(dia)','FALLECIDOS':'FALLECIDOS(dia)'})


Peru_casos = pd.concat([Peru_casos, Peru_casos2], axis=1)


min_date = Peru_casos['date'].min()
temp = Peru_casos.loc[ Peru_casos.loc[:,'date']==min_date , ['TOTAL CASOS (+)','FALLECIDOS'] ]
Peru_casos.loc[ Peru_casos.loc[:,'date']==min_date , ['CASOS(dia)','FALLECIDOS(dia)'] ] = temp


del Peru_casos2, temp, min_date

#ok

Peru_posit = covid_peru('https://github.com/jincio/COVID_19_PERU/raw/master/data/descargas_sala_situacional/POSITIVIDAD_',dates)
Peru_posit['Dpto'] = Peru_posit['Departamento'].where( Peru_posit['REGION'].isna(), Peru_posit['REGION'] )
Peru_posit['Dpto'] = Peru_posit['Dpto'].replace('LIMA METROPOLITANA','LIMA').replace('LIMA REGIÓN','LIMA')

Peru_posit = Peru_posit.drop(['Pais','% de Positividad','Departamento','REGION'],axis=1)

Peru_posit = Peru_posit.groupby(['Dpto','date']).sum().reset_index()

Peru_posit = repl_date(Peru_posit)
Peru_posit = Peru_posit.sort_values(['Dpto','date'])

Peru_posit2 = Peru_posit.loc[:,['Muestras', 'Confirmado (+)']].diff()
Peru_posit2 = Peru_posit2.rename(columns={'Muestras':'Muestras(dia)','Confirmado (+)':'Confirmado(dia)'})

Peru_posit = pd.concat([Peru_posit, Peru_posit2], axis=1)


min_date = Peru_posit['date'].min()
temp = Peru_posit.loc[ Peru_posit.loc[:,'date']==min_date , ['Muestras','Confirmado (+)'] ]
Peru_posit.loc[ Peru_posit.loc[:,'date']==min_date , ['Muestras(dia)','Confirmado(dia)'] ] = temp


del Peru_posit2, temp, min_date


#list(Peru_posit.columns)
#list(Peru.columns)



Peru = pd.merge(Peru_casos,Peru_posit,on=['date','Dpto'])

Peru = pd.merge(Peru,Peru_uci,on=['date'])
Peru = pd.merge(Peru,Peru_hosp,on=['date'])





Peru = Peru.drop(['EVOLUCIÓN FAVORABLE','EVOLUCIÓN DESFAVORABLE','SIN VENTILACIÓN MECÁNICA','Confirmado (+)',
                  'Confirmado(dia)','CON VENTILACIÓN MECÁNICA','EVOLUCIÓN ESTACIONARIA', 'UCI En Uso',
                  'UCI Disponible','PRESTADOR DE SALUD'],axis=1,errors='ignore')
    

del Peru_casos, Peru_hosp, Peru_posit, Peru_uci, cond, dates


    

Peru.to_csv(path3,index=False)



###############################################################################
###############################################################################
###############################################################################




#    BRASIL






###############################################################################
###############################################################################


import pandas as pd
import numpy as np



#total = pd.read_excel(file2, sheet_name='Sheet 1')
total = pd.read_csv(file2,sep=';')

total2 = total.loc[:,('estado','municipio','data','populacaoTCU2019','casosNovos','casosAcumulado','obitosNovos','obitosAcumulado')]

total2 = total2.loc[ total2.loc[:,'municipio'].isna() ,:]
total2 = total2.loc[ total2.loc[:,'populacaoTCU2019'].notna() ,:]
total2 = total2.loc[ total2.loc[:,'estado'].notna() ,:]

total2 = total2.drop('municipio',axis=1)

estados = {'AC':'Acre','AL':'Alagoas','AP':'Amapá','AM':'Amazonas','BA':'Bahia',
'CE':'Ceará','ES':'Espírito Santo','GO':'Goiás','MA':'Maranhão','MT':'Mato Grosso',
'MS':'Mato Grosso do Sul','MG':'Minas Gerais','PA':'Pará','PB':'Paraíba','PR':'Paraná',
'PE':'Pernambuco','PI':'Piauí','RJ':'Rio de Janeiro','RN':'Rio Grande do Norte',
'RS':'Rio Grande do Sul','RO':'Rondônia','RR':'Roraima','SC':'Santa Catarina',
'SP':'São Paulo','SE':'Sergipe','TO':'Tocantins','DF':'Distrito Federal'}

total2['estado'] = total2['estado'].map(estados)




total2.to_csv(path4,index=False)


del estados, total



###############################################################################
###############################################################################
###############################################################################




#    MEXICO




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



####################################3

# USA

####################################3

file = 'https://raw.githubusercontent.com/COVID19Tracking/covid-tracking-data/master/data/states_daily_4pm_et.csv'


df = pd.read_csv(file,sep=',')

list(df.columns)

df = df.loc[:,['date','state','positive','positiveIncrease','totalTestResults',
               'totalTestResultsIncrease','death','deathIncrease','hospitalizedCumulative','inIcuCumulative']]

df.to_csv('C:/Users/admin/Downloads/Peru/USA_COVID_'+version+'.csv',index=False)





mob = pd.read_csv('C:/Users/admin/Downloads/Global_Mobility_Report.csv',sep=',')

#Filter Countries
cond = mob.loc[:,'country_region_code'].apply(lambda x: x in ['AR','CO','PE','MX','US','BR','CH','PA'] )
mob1 = mob.loc[ cond , : ]

# REmove region 2 and whole country
cond = mob.loc[:,'sub_region_1'].notna()
mob1 = mob1.loc[ cond , : ]

cond = mob.loc[:,'sub_region_2'].isna()
mob1 = mob1.loc[ cond , : ]

mob1.to_csv(path6,index=False)


del df_MX,dptos,dptos2,fallecidos,fallecidos3,fallecidos4,file2,mob,mob1,clue,cond,cond1
del Peru, Peru_deaths, Peru_deaths_A, Peru_deaths_D, Peru_deaths_final,mx_code1, mx_code2, mx_munic, mx_paciente, mx_resultado, mx_sexo
del path0, path1, path2, path3, path4, path5, path6,  version, total2, tests, test2, test
del poblacion, prom_muertes, promedios
del  cond2, df, file1, file, dptos2b
del respir,col,deaths,dpto,pop,cases
del  new_cols,temp_dict, file3
del Peru_deaths_D2, fallecidos1, fallecidos2, fallecidosX

