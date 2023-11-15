import pandas as pd

df = pd.read_csv('IMF_Mystery_Shopping.csv', delimiter=';')

df['fecha'] = pd.to_datetime(df['fecha'])

fecha_inicio = pd.to_datetime('2014-01-01')
fecha_fin = pd.to_datetime('2015-01-01')

filtro = (df['Fecha de ejecucion'] >= fecha_inicio) & (df['Fecha de ejecucion'] < fecha_fin)
df_filtrado = df[filtro]


