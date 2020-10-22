




import pandas as pd
#import math


file20 = "C:/Users/admin/Downloads/EPID_COL/Boletin INS/Boletines INS 2020.xlsx"
file19 = "C:/Users/admin/Downloads/EPID_COL/Boletin INS/Boletines INS 2019.xlsx"

df20 = pd.read_excel(file20, None)
df19 = pd.read_excel(file19, None)

del file19, file20

# 2020 DATA
#file = 
#sheets = 


sheets = []
for i in range(1,33):
    sheets.append( 'Sheet'+str(i)  )    
    
boletin20 = pd.DataFrame()

for sheet in sheets:

    df1 = df20[sheet].T.reset_index()
    
    df1['index'] = df1['index'].replace('Unnamed.*','',regex=True)
    
    df1.columns = df1.iloc[0,:]
    
    df1 = df1.iloc[1:,:]
    
    temp = ''
    for ind in df1.index:
        #print(df1.loc[ind,''])
        if df1.loc[ind,'Epidemia'] != '':
            temp = df1.loc[ind,'Epidemia']
        else:
            df1.loc[ind,'Epidemia'] = temp
    
    df1['semana'] = sheet
    
    df1['semana'] = df1['semana'].replace('Sheet','',regex=True).apply(int)

    boletin20 = pd.concat([df1,boletin20])

boletin20['Year'] = 2020

deptos = list(boletin20.columns)[2:-3]



for dpto in deptos:
    try:
        boletin20.loc[:,dpto] = boletin20.loc[:,dpto].fillna(0).replace('-',0).replace('',0)
        boletin20.loc[:,dpto] = boletin20.loc[:,dpto].apply(lambda x: x*1000 if (x%1 != 0) else x )
    except:
        print(dpto)

boletin20['Total nacional'] = boletin20.loc[:,deptos].sum(axis=1)





del df1,temp,sheet,i,sheets,ind, deptos, dpto



#boletin30 = pd.read_csv('C:/Users/admin/Downloads/EPID_COL/Boletin INS/Boletin_INS_31.csv')
#
#boletin30  = boletin30.drop(['Total nacional'],axis=1).rename(columns={'Total':'Total nacional'})
#
#boletin30['Year'] = 2020



# 2019 DATA
    
sheets = []
for i in [4,8,12,16,20,24,28,32,36]:
    sheets.append( 'Sheet'+str(i)  )

boletin19 = pd.DataFrame()

# sheet = sheets[2]

for sheet in sheets:

    df1 = df19[sheet].T.reset_index()
    
    df1['index'] = df1['index'].replace('Unnamed.*','',regex=True)
    
    df1.columns = df1.iloc[0,:]
    
    df1 = df1.iloc[1:,:]
    
    temp = ''
    for ind in df1.index:
        #print(df1.loc[ind,''])
        if df1.loc[ind,'Epidemia'] != '':
            temp = df1.loc[ind,'Epidemia']
        else:
            df1.loc[ind,'Epidemia'] = temp
    
    df1['semana'] = sheet
    
    df1['semana'] = df1['semana'].replace('Sheet','',regex=True).apply(int)
    
    df1 = df1.rename(columns={'Norte Santander':'Norte de Santander','Santa Marta':'Santa Marta D.E.'})

    boletin19 = pd.concat([df1,boletin19])

boletin19['Valor'] = boletin19['Valor'].replace('2020','2019',regex=True)
boletin19['Year'] = 2019


deptos = list(boletin19.columns)[2:-3]

for dpto in deptos:
    try:
        boletin19.loc[:,dpto] = boletin19.loc[:,dpto].fillna(0).replace('-',0).replace('',0).apply(str)
        boletin19.loc[:,dpto] = boletin19.loc[:,dpto].apply(lambda x: x.replace('.','',1) if (len(x) - len(x.replace('.','')) == 2) else x ).apply(float)
        boletin19.loc[:,dpto] = boletin19.loc[:,dpto].apply(lambda x: x*1000 if (x%1 != 0) else x )
    except:
        print(dpto)

dpto = 'Bogotá'
a = boletin19.loc[:,dpto]


boletin19['Total nacional'] = boletin19.loc[:,deptos].sum(axis=1)


del df1,temp,sheet,i,sheets,ind, deptos, dpto



#s.reindex([('foo', 'two'), ('bar', 'one'), ('qux', 'one'), ('baz', 'one')])

del df19,df20

boletin = pd.concat([boletin20,boletin19])

#boletin = boletin.drop('Total nacional',axis=1)




boletin2 = pd.pivot_table(boletin,columns=['Epidemia','Valor','semana','Year']).reset_index()

boletin2.columns = ['Dpto','Epidemia','Medida','Semana','Año','Cantidad']


#correcciones = {'':''}
#
#boletin['Epidemia'] = boletin['Epidemia'].map(correcciones)




boletin2.to_csv('C:/Users/admin/Downloads/EPID_COL/Boletin INS/Boletin INS 2020_52.csv',index=False)
