from turtle import pd
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from db_functions import db_connect, set_query

load_dotenv()

def habitat_area_Espi(BO0, BO, workspace):

    module = 'habitat'
    fields = ['Name', 'area_hc', 'Umbral']
    
    cnx = db_connect()

    ### query SQL to get data
    data_query = set_query(workspace, module, fields)
    layers = pd.read_sql_query(data_query, cnx)

    # Determines elements of existing categories in the shape layer
    IdoHaES_i = layers[["area_hc"]].values.ravel()

    error_Es_i = [None for x in range(len(IdoHaES_i))]
    for i in range(len(IdoHaES_i)):
        if BO0 - IdoHaES_i[i] < 0:
            error_Es_i[i] = 0
        else:
            error_Es_i[i] = np.abs((BO0 - IdoHaES_i[i]) / BO0)

    HabES_i = BO * (1 - np.array(error_Es_i))
    
    return HabES_i