# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 10:38:34 2020

@author: admin
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


 
 



#states = ['pa','ap','ce','sc','am','ma','pe','rn']

#cities = {'pa':['Belém','Santarém'],'ap':['Macapá'],'ce':['Fortaleza','Sobral'],'sc':['Itajaí','Balneário Camboriú','Florinápolis','Joinville'],
#          'am':['Manaus','Tefé','Parintins','Tabatinga'],'ma':['São Luís'],'pe':['Recife'],'rn':['Natal']}



option = 1

if option == 1:
    
    states = ['sc-1 (2)','sc-2 (2)']
    cities = {'sc-1 (2)':['Joinvile','Florianópolis','Blumenau','São José','Chapecó','Itajaí',
                    'Criciúma','Jaraguá do Sul','Palhoça','Lages','Balneário Camboriú',
                    'Brusque','Camboriú','Navegantes'],
              'sc-2 (1)':['Joinvile','Florianópolis','Blumenau','São José','Chapecó','Itajaí',
                    'Criciúma','Jaraguá do Sul','Palhoça','Lages','Balneário Camboriú',
                    'Brusque','Camboriú','Navegantes'],
              'am (3)':['Manaus','Parintins']}

    #dfX = pd.read_csv('C:/Users/admin/Downloads/dados-ce.csv',sep=';',engine='python')
    
    def check_mun(x,lista):
        include = False
        for mun in lista:
            if mun == x:
                include =True
                break
        return include
    

    df = pd.DataFrame()
    
    
    for state in states:
        path = 'C:/Users/admin/Downloads/dados-' + state + '.csv'
        try:  
            df0 = pd.read_csv(path,sep=';',engine='python')
            restric = df0['municipio'].apply(lambda x : check_mun(x,cities[state]))
            restric.sum()
            df1 = df0.loc[restric,:]
            print(state, ' OK')
            df = df.append(df1)
        except:
            
            print(state, ' not OK')
        
    #list(df.columns)
    to_drop = ['ÿid','dataNascimento','cbo','paisOrigem','estadoIBGE',
                 'municipioIBGE','origem', 'cnes','estadoNotificacao',
                 'estadoNotificacaoIBGE','municipioNotificacaoIBGE','excluido', 'validado']
    df = df.drop(to_drop,axis=1)    
        
 # ,'bairro','cep'

    df.to_csv('C:/Users/admin/Downloads/Peru/Brasil_Saude_100.csv', index=False)
    
    del df, state, states, restric, df0, cities, path,df1, option, to_drop


else:
    
    
    ###############################################################   
    ###############################################################################   
    ###############################################################################    
        
        
    df = pd.read_csv('C:/Users/admin/Downloads/dados-sc.csv',sep=';',engine='python')
    
    list(df.columns)
    # Remove columns
    
    df = df.drop(['ÿid','cbo','paisOrigem','bairro','estado','estadoIBGE','municipioIBGE',
                          'cep','origem','cnes','estadoNotificacao','estadoNotificacaoIBGE',
                          'municipioNotificacao','municipioNotificacaoIBGE','numeroNotificacao',
                          'excluido','validado','classificacaoFinal'],axis=1)
    
        
        
    # Change to Date format
    
    columns = ['dataNotificacao','dataEncerramento','dataTeste','dataInicioSintomas','dataNascimento']
    #col = columns[0]
    for col in columns:  
        df[col] = df[col].apply(lambda x : str(x)[:10] ).replace('undefined', 'nan')
        df[col] = df[col].apply(lambda x : '19'+x[2:] if x[:2] not in ['20','19'] else x ).replace('19n','null')
        
    
    #Filter Null Dates
    cond = (df.loc[:,'dataNotificacao']!='null') & (df.loc[:,'dataTeste']!='null')
    df = df.loc[cond,:].copy()
    
    # Filter Dates
    df = df.loc[df.loc[:,'dataNotificacao']>'2020-06-09',:].copy()
    
    
    
    # Age as Integer
    df['idade'] = df['idade'].apply(int)
    
    
    
    # Sympthoms
    
    #df['num_symp'] = df.loc[:,'sintomas'].apply(lambda x : str(x).count(',')+1 )    
        
    sympthoms = ['Dor de Garganta','Febre','Dispneia','Tosse','Outros']
    
    df.loc[:,'sintomas'] = df.loc[:,'sintomas'].fillna('')
    
    for sym in sympthoms:
        df[sym] = df.loc[:,'sintomas'].apply(lambda x : sym in x )  
    
    
    df = df.rename(columns={'Dor de Garganta':'Sore Throat',
                                    'Febre':'Fever','Dispneia':'Shortness of Breath',
                                    'Tosse':'Cough','Outros':'Other'})
    
    del sympthoms, sym
       
     
    # Comorbidities
       
    comorbid = ['Doenças respiratórias crônicas descompensadas','Diabetes',
                'Doenças cardíacas crônicas','Imunossupressão','Gestante de alto risco',
                'Doenças renais crônicas em estágio avançado (graus 3, 4 ou 5)',
                'Gestante'] 
    
    for com in comorbid:
        df[com] = df.loc[:,'condicoes'].apply(lambda x : com in str(x) )  
    
    df = df.rename(columns={'Doenças respiratórias crônicas descompensadas':'Pulmonary',
                'Diabetes':'Diabetes ','Doenças cardíacas crônicas':'Cardiac',
                'Doenças renais crônicas em estágio avançado (graus 3, 4 ou 5)':'Renal ',
                'Imunossupressão':'Inmune','Gestante':'Pregnant'})
    
    del comorbid, com
       
     
    # Prof Salud
    temp_dict = {'Não':False,'Sim':True}      
    df['profissionalSaude'] = df['profissionalSaude'].map(temp_dict)    
       
    # Sexo
    temp_dict = {'Masculino':'M','Femenino':'F'}      
    df['sexo'] = df['sexo'].map(temp_dict)    
      
    # Test Process
    temp_dict = {'Coletado':'In process','Concluído':'Done','Solicitado':'Ordered'}      
    df['estadoTeste'] = df['estadoTeste'].map(temp_dict) 
    
    # Test Result
    temp_dict = {'Negativo':False,'Positivo':True}      
    df['resultadoTeste'] = df['resultadoTeste'].map(temp_dict)   
    #df['Test_Result'] = df['Test_Result'].map(temp_dict)   
    
    del temp_dict
    
    
    
    
    # Column names
    #list(df.columns)
    
    
    df = df.rename(columns={'dataNotificacao':'Date_Notif','idade':'Age','sexo':'Sex',
                'dataInicioSintomas':'Date_Symp ','dataNascimento':'Data_Birth','evolucaoCaso':'Follow_up',
                'profissionalSaude':'Health_prof','dataEncerramento':'Date_SocIsolat','tipoTeste':'Test',
                'estadoTeste':'Test_process','dataTeste':'Date_Test','resultadoTeste':'Test_Result'})
    
    
    df = df.drop(['sintomas','condicoes'],axis=1)
    
    
    
    ###############################################################################
    # Time Perods
    df['Periods'] = ''
    
    cond = (df.loc[:,'Date_Notif']>='2020-06-23') & (df.loc[:,'Date_Notif']<'2020-07-07')
    df.loc[ cond,'Periods' ] = 'Pre'
    
    #cond = (df.loc[:,'Date_Notif']>='2020-07-07') & (df.loc[:,'Date_Notif']<'2020-07-21')
    #df.loc[cond,'Periods'] = 'Trans'
    
    cond = (df.loc[:,'Date_Notif']>='2020-07-21') & (df.loc[:,'Date_Notif']<'2020-08-04')
    df.loc[cond,'Periods'] = 'Post'
    
    #cond = df['Periods'] == ''
    #df.loc[cond,'Periods'] = 'Other'
    
        
    ###############################################################################
    # Group Locations
    df['Group'] = ''
    df.loc[cond,'Group'] 
    df.loc[cond,:] 
    
    group = ['ita','irg','brg']
    
    ita = ['Itajaí']
    
    irg = ['Balneário Camboriú','Bombinhas','Barra Velha','Camboriú','Ilhota',
           'Itapema','Navegantes','Penha','Piçarras','Porto BeloSão João do Itaperiú']
    
    brg = ['Apiúna','Ascurra','Benedito Novo','Blumenau','Botuverá','Brusque','Doutor Pedrinho',
           'Gaspar','Guabiruba','Indaial','Luiz Alves','Pomerode','Rio dos Cedros','RodeioTimbó'] 
    
    for gr in group:
        cond = df['municipio'].apply(lambda x : x  in eval(gr) )
        df.loc[cond,'Group'] = gr
    
    cond = df['Group'] == ''
    df.loc[cond,'Group'] = 'scs'
    
    
    
    del irg, brg, ita
    # Change to Date format
    #list(df.columns)
    
    ###############################################################################
    ###############################################################################
    ###############################################################################
    
    # Testing
    
    df['P_Testing'] = ''
    
    cond = (df.loc[:,'Date_Test']>='2020-06-23') & (df.loc[:,'Date_Notif']<'2020-07-07')
    df.loc[ cond,'P_Testing' ] = 'Pre'
    
    #cond = (df.loc[:,'Date_Notif']>='2020-07-07') & (df.loc[:,'Date_Notif']<'2020-07-21')
    #df.loc[cond,'Periods'] = 'Trans'
    
    cond = (df.loc[:,'Date_Test']>='2020-07-21') & (df.loc[:,'Date_Notif']<'2020-08-04')
    df.loc[cond,'P_Testing'] = 'Post'
    
    #cond = df['Periods'] == ''
    #df.loc[cond,'Periods'] = 'Other'
    
    
    
    
    
    
    
    
    df['Test_Result2'] = df['Test_Result'].apply(float)
    
    testing = df.groupby(['Group','P_Testing']).agg({'Test_Result2':['mean','std','count']}).droplevel(level=0,axis=1)
    
    testing['lim_inf'] = testing['mean'] - testing['std'] / (testing['count'])**(0.5) * 1.96
    testing['lim_sup'] = testing['mean'] + testing['std'] / (testing['count'])**(0.5) * 1.96
    
    
    
    





    
    
    
    
    
    
    
    ###############################################################################
    ###############################################################################
    ###############################################################################
    import numpy as np
    from matplotlib.patches import Polygon
    
    
    # Fixing random state for reproducibility
    np.random.seed(19680801)
    
    # fake up some data
    spread = np.random.rand(50) * 100
    center = np.ones(25) * 50
    flier_high = np.random.rand(10) * 100 + 100
    flier_low = np.random.rand(10) * -100
    data = np.concatenate((spread, center, flier_high, flier_low))
    
    #fig, axs = plt.subplots(2, 3)
    #
    ## basic plot
    #axs[0, 0].boxplot(data)
    #axs[0, 0].set_title('basic plot')
    #
    ## notched plot
    #axs[0, 1].boxplot(data, 1)
    #axs[0, 1].set_title('notched plot')
    #
    ## change outlier point symbols
    #axs[0, 2].boxplot(data, 0, 'gD')
    #axs[0, 2].set_title('change outlier\npoint symbols')
    #
    ## don't show outlier points
    #axs[1, 0].boxplot(data, 0, '')
    #axs[1, 0].set_title("don't show\noutlier points")
    #
    ## horizontal boxes
    #axs[1, 1].boxplot(data, 0, 'rs', 0)
    #axs[1, 1].set_title('horizontal boxes')
    #
    ## change whisker length
    #axs[1, 2].boxplot(data, 0, 'rs', 0, 0.75)
    #axs[1, 2].set_title('change whisker length')
    #
    #fig.subplots_adjust(left=0.08, right=0.98, bottom=0.05, top=0.9,
    #                    hspace=0.4, wspace=0.3)
    
    # fake up some more data
    spread = np.random.rand(50) * 100
    center = np.ones(25) * 40
    flier_high = np.random.rand(10) * 100 + 100
    flier_low = np.random.rand(10) * -100
    d2 = np.concatenate((spread, center, flier_high, flier_low))
    # Making a 2-D array only works if all the columns are the
    # same length.  If they are not, then use a list instead.
    # This is actually more efficient because boxplot converts
    # a 2-D array into a list of vectors internally anyway.
    data = [data, d2, d2[::2]]
    
    # Multiple box plots on one Axes
    fig, ax = plt.subplots()
    ax.boxplot(data)
    
    plt.show()
    
    








