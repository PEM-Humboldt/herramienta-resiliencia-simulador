from turtle import pd
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def habitat_area(dh, BO, BO0, workspace):

    DB_SYSTEM = os.getenv('DB_SYSTEM')
    DB_ADDRESS = os.getenv('DB_ADDRESS')
    DB_PORT = os.getenv('DB_PORT')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')

    if DB_SYSTEM=='oracle':
        SQL_DRIVER = 'cx_oracle'
        connection_str = ('{dbsystem}+{sqldriver}://{username}:{password}@{ipaddress}:{port}/?service_name={dbname}'.format(dbsystem=DB_SYSTEM,
                                                                                                sqldriver=SQL_DRIVER,
                                                                                                username=DB_USERNAME,
                                                                                                password=DB_PASSWORD,
                                                                                                ipaddress=DB_ADDRESS,
                                                                                                port=DB_PORT,
                                                                                                dbname=DB_NAME))
        data_query = f'SELECT Name, area_hc, Umbral FROM {workspace}_habitat'
    else:
        # Do not change this long string that contains the necessary MongoDB login information
        connection_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(dbsystem=DB_SYSTEM,
                                                                                                username=DB_USERNAME,
                                                                                                password=DB_PASSWORD,
                                                                                                ipaddress=DB_ADDRESS,
                                                                                                port=DB_PORT,
                                                                                                dbname=DB_NAME))
        data_query = f'SELECT Name, area_hc, Umbral FROM public.{workspace}_habitat'

    # Create the connection
    cnx = create_engine(connection_str)

    ### query SQL to get data

    layers = pd.read_sql_query(data_query, cnx)

    # Determines elements of existing categories in the shape layer
    species_names = layers[["name"]].values.ravel()
    IdoHaES_i = layers[["area_hc"]].values.ravel()
    percentage_Ha_ES_i = layers[["umbral"]].values.ravel() / 100
    ConecBOactual = dh[0, 1]

    error_Es_i = [None for x in range(len(IdoHaES_i))]
    for i in range(len(IdoHaES_i)):
        if BO0 - IdoHaES_i[i] < 0:
            error_Es_i[i] = 0
        else:
            error_Es_i[i] = np.abs((BO0 - IdoHaES_i[i]) / BO0)


    UmEs_i = percentage_Ha_ES_i * IdoHaES_i
    HabES_i = BO * (1 - np.array(error_Es_i))
    ExistenceEs_i = np.zeros(len(UmEs_i))
    PperES_i = np.abs((HabES_i - UmEs_i) / HabES_i) * ConecBOactual

    for i in range(len(UmEs_i)):
        if PperES_i[i] > 0:
            ExistenceEs_i[i] = 1
        else:
            ExistenceEs_i[i] = 0

    n_species = len(species_names) # number of species

    HabES_i = HabES_i.reshape(1, -1)
    PperES_i = PperES_i.reshape(1, -1)
    ExistenceEs_i = ExistenceEs_i.reshape(1, -1)
    return HabES_i, PperES_i, ExistenceEs_i, species_names, n_species
