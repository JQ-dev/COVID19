

import pandas as pd 

version = '500'
path0 = 'D:/COVID/CovidIndia_'+version+'.csv'
path1 = 'D:/COVID/CovidIndia_mob_'+version+'.csv'
path4 = 'D:/COVID/CovidIndia_vax_'+version+'.csv'


i = 1
raw_d = []
while True:
    try:
        url = f"https://data.covid19bharat.org/csv/latest/raw_data{i}.csv"
        df = pd.read_csv(url)
        #df.to_csv(f'./tmp/csv/latest/raw_data{i}.csv',index=False)
        raw_d.append(df)
        i = i+1
        print(i)
    except:
        break



raw_all = pd.DataFrame()


for chunk in raw_d:
    raw_all = raw_all.append(chunk)




keep_col = ['Date Announced','Detected District','Detected State','Current Status','Num Cases','State code']


dfIndia = raw_all.loc[:,keep_col]


dfIndia.loc[ dfIndia['Detected State'] == 'Delhi','Detected District'] = 'Delhi'

dfIndia = dfIndia.loc[ dfIndia['Current Status'] != 'Recovered']
dfIndia = dfIndia.loc[ dfIndia['Current Status'] != 'Migrated_other']
dfIndia = dfIndia.loc[ dfIndia['Current Status'] != 'Migrated_Other']
dfIndia = dfIndia.loc[ dfIndia['Current Status'] != 'Migrated']

dfIndia['District_Key'] = (dfIndia['State code'] + '_' + dfIndia['Detected District']).str.strip().str.upper()


#a = dfIndia['District_Key'].drop_duplicates()

#dfIndia['District_Key'] = (dfIndia['District_Key'].replace('DL_SOUTH WEST DELHI','DELHI').
#replace('DL_NORTH DELHI','DELHI').replace('DL_NEW DELHI','DELHI').
#replace('DL_NORTH WEST DELHI','DELHI').replace('DL_SOUTH DELHI','DELHI') )


#dfIndia['District_Key'] = dfIndia['State code'] + '_' + dfIndia['Detected District'].str.strip().str.upper()
#




#dfIndia.loc[ dfIndia['Detected District'] == None,'Detected State']



#df_tests = pd.read_csv('https://api.covid19india.org/csv/latest/districts.csv')


#
#
#
#vax = pd.read_csv('http://api.covid19india.org/csv/latest/cowin_vaccine_data_districtwise.csv')
#
#vax = vax.drop(['S No', 'State_Code', 'State', 'Cowin Key', 'District'],axis=1)
#
#vax.iloc[0,0] = 'Measure'
#
#vax = vax.set_index('District_Key').T
#
#
#
#vax.set_index('Measure',append=True,inplace=True)
#
#
#vax = vax.stack()
#
#vax = vax.reset_index()
#
#vax['level_0'] = vax['level_0'].str.split('.',expand=True)[0]
#
#vax.columns = ['Date','Measure','District_Key','Amount']
#
#vax['District_Key'] = vax['District_Key'].str.upper()
#
#
#vax['Amount'] = vax['Amount'].apply(int)
#
#vax = vax[vax['Measure'] != 'Total Individuals Registered']
#vax = vax[vax['Measure'] != 'Total Sessions Conducted']
#vax = vax[vax['Measure'] != 'Total Sites ']
#vax = vax[vax['Measure'] != 'Male(Individuals Vaccinated)']
#vax = vax[vax['Measure'] != 'Female(Individuals Vaccinated)']
#vax = vax[vax['Measure'] != 'Transgender(Individuals Vaccinated)']
#
#
#vax = vax.rename(columns={'Date':'Date Announced',
#                          'Measure':'Current Status',
#                          'Amount':'Num Cases'})
#
#    
#vax['District_Key'] = (vax['District_Key'].replace('DL_SOUTH WEST DELHI','DL_DELHI').
#replace('DL_NORTH DELHI','DL_DELHI').replace('DL_NEW DELHI','DL_DELHI').replace('DL_WEST DELHI','DL_DELHI').
#replace('DL_NORTH WEST DELHI','DL_DELHI').replace('DL_SOUTH DELHI','DL_DELHI').
#replace('DL_CENTRAL DELHI','DL_DELHI').replace('DL_EAST DELHI','DL_DELHI').
#replace('DL_NORTH EAST DELHI','DL_DELHI').replace('DL_SOUTH EAST DELHI') )    
#    
#
#
#vax = vax.groupby(['Date Announced','Current Status','District_Key']).sum().reset_index()
#
#vax1 = vax[ vax['District_Key'].apply(lambda x: 'DELHI' in x) ]
#    
#
#temp_dict = dfIndia.loc[:,['District_Key','Detected District']].drop_duplicates()
#
#
#
#temp_dict = dict(zip(temp_dict['District_Key'],temp_dict['Detected District']))
#
#vax['Detected District'] = vax['District_Key'].map(temp_dict)
#
#
#
#temp_dict = dfIndia.loc[:,['District_Key','Detected State']].drop_duplicates()
#
#temp_dict = dict(zip(temp_dict['District_Key'],temp_dict['Detected State']))
#
#vax['Detected State'] = vax['District_Key'].map(temp_dict)
#
#
#
##a = vax[ vax['District_Key']=='TN_CHENNAI' ]
##
#
#
#
#dfIndia = dfIndia.append(vax)

#b = dfIndia[ dfIndia['District_Key']=='TN_CHENNAI' ]


df_pop = pd.read_csv('D:/COVID/India_pop.csv')


dict_pop = dict(zip(df_pop['District Key'],df_pop['Pop']))



dfIndia['distr_pop'] = dfIndia['District_Key'].map(dict_pop)


#check = dfIndia.loc[:,['District_Key','Num Cases']].groupby('District_Key').sum().reset_index()

#check['distr_pop'] = check['District_Key'].map(dict_pop)


dfIndia = dfIndia.drop('State code',axis=1)


dfIndia['Detected District'] = dfIndia['Detected District'].str.strip().str.upper()
dfIndia['Detected State'] = dfIndia['Detected State'].str.strip().str.upper()

dfIndia['District_Key'] = dfIndia['Detected State']+'__'+dfIndia['Detected District']
a = dfIndia.loc[dfIndia['distr_pop']>0,['District_Key', 'distr_pop']].drop_duplicates().fillna('xx')


dict_pop = dict(zip(a['District_Key'],a['distr_pop']))

dfIndia['distr_pop2'] = dfIndia['District_Key'].map(dict_pop)



dfIndia.to_csv(path0,index=False)







mob = pd.read_csv('D:/COVID/Global_Mobility_Report.csv',sep=',')


#a = mob['country_region_code'].drop_duplicates()
#Filter Countries
mob = mob.loc[ mob['country_region_code'] == 'IN' , : ]



mob.to_csv(path1,index=False)

del mob

