import pandas as pd
from sqlalchemy import create_engine, Table, MetaData, select
import unicodedata
from faker import Faker
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
import traceback
import yaml


fake = Faker('es_ES')

def config():
    with open('./MysteryLoader/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        return config
    
def clean_string(input_string):
    return unicodedata.normalize('NFKD', str(input_string)).encode('ascii', 'ignore').decode('ascii')
     
def get_engine():
    usuario = config()['database']['usuario']
    password = config()['database']['password']
    host = config()['database']['host']  
    puerto = config()['database']['puerto']  
    db = config()['database']['db']

    url_conexion = f'mysql+pymysql://{usuario}:{password}@{host}:{puerto}/{db}?charset=utf8mb4'
    return create_engine(url_conexion)


def is_this_field_exist(table,criterios_busqueda):
    
    Session = sessionmaker(bind=get_engine())
    session = Session()
    try:

        query = select(table).where(
            *[table.c[key] == value for key, value in criterios_busqueda.items()]
        )

        resultado = session.execute(query).one_or_none()

        return resultado is not None
    except NoResultFound:
        return False
    finally:
        session.close()

def get_id(table, criterios_busqueda):
    Session = sessionmaker(bind=get_engine())
    session = Session()
    try:
        query = select(table.c.ID).where(
        *[table.c[key] == value for key, value in criterios_busqueda.items()])
        resultado = session.execute(query).scalar()

        return resultado
    except Exception as e:
        print(f"Error al obtener el ID: {e}")
        traceback.print_exc()
        return None
    finally:
        session.close()
            
def create_if_not_exist(table, row, keys, engine, conn, params={}):
    metadata = MetaData()
    metadata.bind = engine
    
    fields = {key: row[key] for key in keys}
    
    if not bool(params):
        params = fields
        
    if not is_this_field_exist(table, params) :
        result = conn.execute(table.insert().values(**fields))
        return result.inserted_primary_key[0]
    
    return get_id(table, params)

def generate_file(df):
    
    df = df.rename(columns={
        'POBLACION' : 'Poblacion',
        'CP': 'Codigo_Postal',
        'PROVINCIA': 'Comunidad_Autonoma',
        'COD_LOC' : 'Codigo_Local',
        'NOMBRE_LOC' : 'Nombre',
        'OFICINA' : 'ID',
        'COD_AUDITOR':'Codigo_Auditor',
        'ID_EVALUACION':'Id_Evaluacion',
        'RESULTADO':'Resultado',
        'TITULO_CUESTIONARIO':'Titulo',
        'Fecha de ejecucion':'Fecha',
        'COD_PROY':'Codigo_Proyecto'
    })
    
    df['Comunidad_Autonoma'] = df['Comunidad_Autonoma'].apply(clean_string)
    df['Poblacion'] = df['Poblacion'].apply(clean_string)
    df['Nombre'] = df['Nombre'].apply(clean_string)
    df['Titulo'] = df['Titulo'].apply(clean_string)
    df['Resultado'] = df['Resultado'].str.replace(',', '.').astype(float)
    
    engine = get_engine()
    metadata = MetaData()
    metadata.bind = engine
    counter = 0
    error_counter = 0
    with engine.connect() as conn:
        
        for row in df.head(config()['records']).to_dict(orient='records'):
            try:
                counter = counter + 1
                trans = conn.begin()
                
                UbicacionTable = Table('Ubicacion', metadata, autoload_with=engine)
                keys = ['Poblacion', 'Comunidad_Autonoma', 'Codigo_Postal']
                
                ubicacion_id = create_if_not_exist(UbicacionTable, row, keys, engine, conn)

                
                LocalTable = Table('Local', metadata, autoload_with=engine)
                row['Ubicacion_ID'] = ubicacion_id
                keys = ['Codigo_Local', 'Nombre','Ubicacion_ID']

                generated_local_id = create_if_not_exist(LocalTable, row, keys, engine, conn)

                row['Nombre'] = fake.company()
                OficinaTable = Table('Oficina', metadata, autoload_with=engine)
                keys = ['ID','Nombre']
                oficina_id = create_if_not_exist(OficinaTable, row, keys, engine, conn, {'ID': row['ID']} )
                
                
                AuditorTable = Table('Auditor', metadata, autoload_with=engine)
                row['Nombre'] = fake.name()
                row['Oficina'] = oficina_id
                keys = ['Codigo_Auditor', 'Nombre', 'Oficina']
                auditor_id = create_if_not_exist(AuditorTable, row, keys, engine, conn,{'Codigo_Auditor': row['Codigo_Auditor']} )
                
                EvaluacionTable = Table('Evaluacion', metadata, autoload_with=engine)
                evaluacion = {key: row[key] for key in ['Id_Evaluacion', 'Codigo_Proyecto', 'Fecha', 'Resultado', 'Titulo']} 
                
                if evaluacion['Fecha'] is not None:
                    evaluacion['Fecha'] = datetime.strptime(evaluacion['Fecha'], '%d/%m/%Y').strftime('%Y-%m-%d')
           
                evaluacion['Auditor'] = auditor_id
                evaluacion['Id_Local'] = generated_local_id
                
                result = conn.execute(EvaluacionTable.insert().values(**evaluacion))
                
                trans.commit()
                if counter % 10 == 0:
                    print(f"insertando registro {counter}")
                             
            except Exception as e:
                print(e)
                traceback.print_exc()
                trans.rollback()
                error_counter = error_counter + 1
                
        print(f"Registros Insertados : {counter}")
        print(f"Registros con error : {error_counter}")
        
df = pd.read_csv('./inputs/IMF_Mystery_Shopping.csv', delimiter=';')

generate_file(df)