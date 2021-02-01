import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_data():

    meses=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    archivos = {}
    #Cambiar Junio por 20 en vez de 2020 file
    for mes in meses:
        archivos[f'{mes}'] = pd.read_csv(f'/Users/felipeinostroza/desktop/drive-download-20210124T195157Z-001/CSV/Conta_{mes}_20.csv'\
                                         , sep=';')

    #Eliminando whitespaces en las columnas
    for mes in meses:
        archivos[mes] = archivos[mes].rename(columns=lambda x: x.strip())


    #Juntando todos los archivos
    data_full = pd.concat([archivos['Enero'], archivos['Febrero'], archivos['Marzo'], archivos['Abril'],\
               archivos['Mayo'], archivos['Junio'], archivos['Julio'], archivos['Agosto'],\
               archivos['Septiembre'], archivos['Octubre'], archivos['Noviembre'], archivos['Diciembre']], axis =0)

    data_full = data_full.reset_index().drop(columns= 'index')
    data_full = data_full[['COMPROBANTE', 'TIPO COMPROBANTE', 'FECHACOMP', 'CODPLAN', 'NOMPLAN', 'GLOSA', 'DEBE', 'HABER', 'SUBCUENTA', \
             'CODDOCU', 'DOCUMENTO', 'NOMCCOSTO', 'MES']]

    #eliminando whitespaces de las celdas
    columnas_modificar = ['NOMPLAN', 'CODDOCU', 'NOMCCOSTO']
    for columna in columnas_modificar:
        data_full[columna] = data_full[columna].str.strip().str.upper()
    #transformando a fechas (Y/m/d)
    columnas_fechas = ['FECHACOMP']
    for columna in columnas_fechas:
        data_full[columna] = pd.to_datetime(pd.to_datetime(pd.to_datetime(data_full[columna])).dt.strftime('%d-%m-%Y'))
    #Trasformando columnas importantes a int en vez de float
    columnas = ['COMPROBANTE', 'MES', 'CODPLAN']
    for columna in columnas:
        data_full[columna] = data_full[columna].fillna(999999)
        data_full[columna] = data_full[columna].astype('int64')

    #Filtrado de información (rellenadndo Nan values de columnas a texto)
    columnas = ['NOMPLAN', 'GLOSA', 'TIPO COMPROBANTE']
    for columna in columnas:
        data_full[columna] = data_full[columna].fillna('No info').str.upper()

    #Transformando a numeros las columnas de numeros
    columnas = ['HABER', 'DEBE']
    for columna in columnas:
        data_full[columna] = data_full[columna].fillna('0')
        data_full[columna] = data_full[columna].astype(str).str.strip().replace('-','0').str.replace('.','').astype(int)

    return data_full


def get_episodes(name):

    response = requests.get(f'https://cdn.animenewsnetwork.com/encyclopedia/api.xml?title=~{name}')

    soup = BeautifulSoup(response.text,'html.parser')


    anime = soup.find_all('anime', type ='TV')

    season = 0

    epis = {  }

    for i in range(len(anime)):

       if anime[i].find_all('episode'):

            episodes = anime[i].find_all('episode')

            season += 1


            for index, episode in enumerate(episodes):

                n_partes_episodios = len( episode.find_all('title', lang = 'EN') )

                for parte_n in range ( n_partes_episodios ):

                    nombre_parte = episode.find_all('title')[parte_n].string

                    if n_partes_episodios > 1:
                        jkey = f'S{season}E{index + 1}P{parte_n + 1}'

                        detalle = f'Season {season} ,' + 'Episodio ' + f' {index + 1}: '+ f'Parte: {parte_n + 1}'
                        impresion = detalle + ' {} '
                        epis[jkey] = nombre_parte

                       # print (impresion.format(nombre_parte))
                    else:

                        jkey = f'S{season}E{index + 1}'

                        detalle = f'Season {season} ,' + 'Episodio ' + f' {index + 1}: '
                        impresion = detalle +' {} '
                        epis[jkey] = nombre_parte

                      #  print (impresion.format(nombre_parte))

    return pd.DataFrame(index =epis.keys(), columns = {'Nombre Episodio'}, data = epis.values())






