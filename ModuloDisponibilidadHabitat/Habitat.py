from turtle import pd
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def habitat_area(dh, BO, BO0, ConectBO, mcf, mcb, workspace):

    POSTGRES_ADDRESS = os.getenv('POSTGRES_ADDRESS')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DBNAME = os.getenv('POSTGRES_DBNAME')
    # Do not change this long string that contains the necessary MongoDB login information
    postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
                                                                                            password=POSTGRES_PASSWORD,
                                                                                            ipaddress=POSTGRES_ADDRESS,
                                                                                            port=POSTGRES_PORT,
                                                                                            dbname=POSTGRES_DBNAME))

    # Create the connection
    cnx = create_engine(postgres_str)

    ### query SQL to get data

    layers = pd.read_sql_query(f'SELECT Name, area_hc, Umbral FROM public.{workspace}_habitat', cnx)

    # Determines elements of existing categories in the shape layer
    species_names = layers[["name"]].values.ravel()
    IdoHaES_i = layers[["area_hc"]].values.ravel()
    percentage_Ha_ES_i = layers[["umbral"]].values.ravel() / 100

    error_Es_i = [None for x in range(len(IdoHaES_i))]
    for i in range(len(IdoHaES_i)):
        if BO0 - IdoHaES_i[i] < 0:
            error_Es_i[i] = 0
        else:
            error_Es_i[i] = np.abs((BO0 - IdoHaES_i[i]) / BO0)


    UmEs_i = percentage_Ha_ES_i * IdoHaES_i
    HabES_i = BO * (1 - np.array(error_Es_i))
    ExistenceEs_i = np.zeros(len(UmEs_i))
    IperES_i = np.zeros(len(UmEs_i))
    
    for i in range(len(IdoHaES_i)):
        if HabES_i[i] > UmEs_i[i]:
            IperES_i[i] = ((HabES_i[i] - UmEs_i[i]) / HabES_i[i]) * ((mcf + mcb) / 2) * ConectBO
        else:
            IperES_i[i] = 0

    for i in range(len(UmEs_i)):
        if IperES_i[i] > 0:
            ExistenceEs_i[i] = 1
        else:
            ExistenceEs_i[i] = 0

    n_species = len(species_names) # number of species

    HabES_i = HabES_i.reshape(1, -1)
    IperES_i = IperES_i.reshape(1, -1)
    ExistenceEs_i = ExistenceEs_i.reshape(1, -1)
    return HabES_i, IperES_i, ExistenceEs_i, species_names, n_species
