# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 20:27:14 2023

@author: Félix


"""
# PROGRAMA PARA COMPROBAR LAS FECHAS Y GENERAR CSV CON LOS DATOS


# La consulta web es muy lenta ya que carga muchos datos (Del orden de 5 horas en un buen 
# ordenador para unas 2000 empresas con los deatos equivalentes a 25 años por 250 días 
# cada año laboral), por lo que vamos a generar un csv que tenga todos los datos que vamos a emplear para el modelo

# Durante el estudio vamos a presentar numerosos modelos por lo que no podemos 
# tiempo en la simple carga de datos ya que se haría muy ineficiente la programación

# Por otro lado podrían actualizar la librería que hace la consulta web cambiando el 
# formato de algunos datos o algunos valores, pudiendo desembocar en errores en el código 
# o modificaciones en los resuultados, invalidando así el trabajo ya realizado. De hecho 
# esto ya ocurrió una vez durante el desarrollo del TFG

import numpy as np
import pandas as pd
import sys
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import scipy.stats as stats
import os
import yfinance as yf
import datetime

path = os.getcwd()
path = path+'/stock_ticker.csv'
data_companies = pd.read_csv(path) 

company_labels = data_companies['Symbol'].tolist()
company_labels = company_labels[:20]

company_information = pd.DataFrame()


years = 26
years = str(years)+"y"


Parameters = pd.DataFrame() 
Parameters = Parameters.assign(Company_label=None,R=None,s=None,r=None)

error_list = pd.DataFrame() 
error_list = error_list.assign(Company_label = None, Error = None)
    
for i,company in enumerate(company_labels):
    
    if '^'in company:
        
        problem = 'error1'
        error_i = pd.DataFrame({ 'Company_label': [company], 'Error': problem })
        error_list = pd.concat([error_list,error_i],ignore_index = True)
        
        continue       

    datos = yf.Ticker(company).history(years)   # Hacemos una consulta web que nos devuelve un data frame con "todos" los valores disponibles
        
    if len(datos) == 0:
        
        problem = 'error2'
        error_i = pd.DataFrame({ 'Company_label': [company], 'Error': problem })
        error_list = pd.concat([error_list,error_i],ignore_index = True)
        
        continue 
    
    dates = pd.to_datetime(datos.index) # Leemos el tiempo, después de extraerlo del índice
   
    datos['Date'] = dates 
    
    if str(dates[0]) > '1999-12-31 00:00:00-05:00':
        
        problem = 'error3: primer valor '+str(dates[0])
        error_i = pd.DataFrame({ 'Company_label': [company], 'Error': problem })
        error_list = pd.concat([error_list,error_i],ignore_index = True)
        
        continue
    
    problem = 'without problems'
    error_i = pd.DataFrame({ 'Company_label': [company], 'Error': problem })
    error_list = pd.concat([error_list,error_i],ignore_index = True)
    
    datos = datos[(datos['Date']>'1999-12-31 00:00:00-05:00') & (datos['Date']<='2022-12-31 00:00:00-05:00')] # Estudiamos hasta el 31/12/2022   

    actions = datos['Open'] # Leemos todas las acciones
    dates = datos['Date'] # Leemos el tiempo
   
    print(str(i)+' '+company+' '+str(dates[0]))    
    company_information[str(company)] = dates