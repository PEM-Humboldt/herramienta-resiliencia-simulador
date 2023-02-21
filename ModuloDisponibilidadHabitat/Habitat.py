from turtle import pd
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from db_functions import db_connect, set_query

load_dotenv()

def habitat_area(dh, BO, BO0, ConectBO, mcf, mcb, workspace):

    module = 'habitat'
    fields = ['Name', 'area_hc', 'Umbral']
    
    cnx = db_connect()

    ### query SQL to get data
    data_query = set_query(workspace, module, fields)
    layers = pd.read_sql_query(data_query, cnx)

    # Determines elements of existing categories in the shape layer
    BO_max = dh[4,1] 
    if BO_max < BO0:
        BO_max = BO0
    species_names = layers[["name"]].values.ravel()
    IdoHaES_i = layers[["area_hc"]].values.ravel()
    percentage_Ha_ES_i = layers[["umbral"]].values.ravel() / 100
    
    percentage_Ha_ES_i[0] = 0
    percentage_Ha_ES_i[4] = 0
    UmEs_i = percentage_Ha_ES_i * IdoHaES_i
    nonzeroUmEs_i = np.nonzero(UmEs_i)[0]
    zeroUmEs_i = np.where(UmEs_i == 0)[0]  
    
    error_Es_i = np.zeros(len(IdoHaES_i))
    for i in range(len(nonzeroUmEs_i)):
        posi_error = nonzeroUmEs_i[i]
        if BO0 - IdoHaES_i[posi_error] < 0:
            error_Es_i[posi_error] = 0
        else:
            error_Es_i[posi_error] = np.abs((BO0 - IdoHaES_i[posi_error]) / BO0)

    HabES_i = BO * (1 - np.array(error_Es_i))
    ExistenceEs_i = np.zeros(len(UmEs_i))
    IperES_i = np.zeros(len(UmEs_i))
# -------------------------------------------------------------------       
    for i in range(len(nonzeroUmEs_i)):
        if HabES_i[nonzeroUmEs_i[i]] > UmEs_i[nonzeroUmEs_i[i]]:
            IperES_i[nonzeroUmEs_i[i]] = ((HabES_i[nonzeroUmEs_i[i]] - UmEs_i[nonzeroUmEs_i[i]]) / HabES_i[nonzeroUmEs_i[i]]) * ((mcf + mcb) / 2) * ConectBO
        else:
            IperES_i[nonzeroUmEs_i[i]] = 0      
        
    for i in range(len(zeroUmEs_i)):
        if BO <= 0.3 * BO_max:
            IperES_i[zeroUmEs_i[i]] =  (mcf * ConectBO) / 2
        else:
            IperES_i[zeroUmEs_i[i]] = mcf * ConectBO
      
# ------------------------------------------------------------------
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
