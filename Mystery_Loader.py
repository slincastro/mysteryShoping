import pandas as pd
from faker import Faker

fake = Faker('es_ES')

def generate_file(df, file_name):
    df.drop_duplicates(inplace=True)

    print(f"\nGenerando fichero de {file_name} : \n")
    print(df)

    df.to_csv(f'./outputs/{file_name}.csv', index=False)


def generate_ubicacion(df):
    ubicacion = df[['POBLACION', 'PROVINCIA', 'CP']]

    ubicacion = ubicacion.rename(columns={
        'CP': 'CODIGO_POSTAL',
        'PROVINCIA': 'COMUNIDAD_AUTONOMA'
    })

    generate_file(ubicacion, 'ubicacion')

def generate_local(df):
    local = df[['COD_LOC', 'NOMBRE_LOC', 'CP']]

    local = local.rename(columns={
        'COD_LOC': 'CODIGO_LOCAL',
        'NOMBRE_LOC': 'NOMBRE_LOCAL',
        'cp': 'CODIGO_POSTAL'
    })

    generate_file(local, 'local')

def generate_evaluacion(df):
    evaluacion = df[['ID_EVALUACION', 'COD_AUDITOR', 'COD_PROY', 'Fecha de ejecucion', 'RESULTADO', 'TITULO_CUESTIONARIO']]

    evaluacion = evaluacion.rename(columns={
        'fecha de ejecucion': 'FECHA_EJECUCION',
        'COD_AUDITOR': 'CODIGO_AUDITOR',
        'cod_proy': 'CODIGO_PROYECTO',
    } )

    generate_file(evaluacion, 'evaluacion')

def generate_auditor(df):
    auditor = df[['COD_AUDITOR', 'OFICINA']]
    
    auditor.drop_duplicates(inplace=True)

    auditor['NOMBRE_AUDITOR'] = [fake.name() for _ in range(len(auditor))]

    generate_file(auditor, 'auditor')
    
def generate_oficina(df):
    oficina = df[['OFICINA']]

    oficina.drop_duplicates(inplace=True)
    
    oficina['NOMBRE'] = [fake.company() for _ in range(len(oficina))]
    
    generate_file(oficina, 'oficina')


df = pd.read_csv('./inputs/IMF_Mystery_Shopping.csv', delimiter=';')
    
generate_ubicacion(df)
generate_local(df)
generate_evaluacion(df)
generate_auditor(df)
generate_oficina(df)



