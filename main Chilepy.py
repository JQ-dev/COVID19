# -*- coding: utf-8 -*-
"""
Created on Sat May 29 22:11:40 2021

@author: admin
"""

import pandas as pd

link = 'C:/Users/admin/Downloads/Peru/COVID_Chile_300525.csv'

url1 = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/HospitalizadosUCIEtario.csv"
url2 = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/FallecidosEtario.csv"
url3 = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/UCI.csv"
url4 = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/PCR.csv"
ur15 = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/CasosConfirmadosTotales.csv"


d = pd.read_csv(url2)
u = pd.read_csv(url3)
h = pd.read_csv(url1)
t = pd.read_csv(url4)
c = pd.read_csv(ur15)


h = h.set_index('Grupo de edad')
h = h.stack().reset_index()
h.columns = ['edad','date','hospi']


d = d.set_index('Grupo de edad')
d = d - d.shift(1,axis=1).fillna(0)

d = d.stack().reset_index()
d.columns = ['edad','date','deaths']

dh_age = pd.merge(h,d,how='outer')

dh_age.to_csv(link)