import pandas as pd


def removeDates(df):
    df['Fecha de ejecucion'] = pd.to_datetime(df['Fecha de ejecucion'])

    fecha_inicio = pd.to_datetime('2014-01-01')
    fecha_fin = pd.to_datetime('2015-01-01')

    filtro = (df['Fecha de ejecucion'] >= fecha_inicio) & (df['Fecha de ejecucion'] < fecha_fin)
    df_filtrado = df[filtro]
    
    return df_filtrado


df = pd.read_csv('./inputs/IMF_Mystery_Shopping.csv', delimiter=';')


df_filtrado = removeDates(df)
df_filtrado.to_csv('./outputs/Mystery_shoping_cleaned.csv', index=False)


