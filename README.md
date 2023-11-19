# mysteryShoping

MysteryShoping :

* infaestructura : esta carpeta contiene los archivos de infraestructura necesarios para levantar el ambiente del datawarehouse
    - docker-compose.yml : es el arcivo de configuracion de la red , contenedor de base de datos y contenedor de ETL
    - Dockerfile : es el archivo de definicion del contenedor de docker para el ETL de python
    - init-db.sql : es el archivo de creacion de la base de datos
    - requirements.txt : es el archivo que contiene las linrerias necesarias para la instalacion del ambiente
    - wait-for-db-sh : script para verificar que la base de datos esta disponible
* inputs: carpeta que contiene el csv del ejercicio
* Mystery Loader : carpeta con el codigo fuente necesario para la ejecucion y configuracion del ETL
    -   config.yaml : archivo de configuracion de coneccion y de la cantidad de filas que se quiere migrar desde el archivo csv
* outputs : carpeta donde se generan los csvs
* analisis_inicial.py : script que analiza el archivo csv
* Mystery_csv_Loader.py : script que genera archivos separados de csv
* MysteryShoppingAnalysys.twb : Archivo de analisis de datos de Tableu

| se debe tener instalado docker y acceso a internet

1. creacion de ambiente
`cd infraestructura`

2. Limpiar ambiente
`docker-compose down --volumes`

3. Levantar la infraestructura 
`docker-compose up`

