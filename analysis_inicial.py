import pandas as pd
import csv as csv

def csv_writer(data):
    with open('./outputs/analisis_inicial.csv', mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(data)

def analize_column_quality(df, column_name) :
    
    print(f"Procesado : {column_name}")
    num_valores_faltantes = df[column_name].isnull().sum()

    num_valores_unicos = df[column_name].nunique()

    estadisticas = df[column_name].describe()

    df[column_name] = df[column_name].astype(str)
    
    csv_writer([column_name, estadisticas['count'], num_valores_faltantes, num_valores_unicos,df[column_name].max(),df[column_name].min(), df[column_name].str.len().max(), df[column_name].str.len().min()])
    
    
df = pd.read_csv('./inputs/IMF_Mystery_Shopping.csv', delimiter=';')

columns = ['COD_LOC', 'NOMBRE_LOC', 'CP', 'POBLACION', 'OFICINA', 'PROVINCIA', 'COD_PROY', 'ID_EVALUACION', 'Fecha de ejecucion', 'COD_AUDITOR', 'RESULTADO', 'TITULO_CUESTIONARIO']

for column in columns:
    analize_column_quality(df, column)