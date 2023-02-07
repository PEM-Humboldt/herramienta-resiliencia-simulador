import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
from db_functions import db_connect, set_query

load_dotenv()

def initial_cover(workspace):

    module = 'coberturas'
    fields = ['codigo_clc', 'cobertura', 'area_ha']
    
    cnx = db_connect()

    ### query SQL to get data
    data_query = set_query(workspace, module, fields)
    layers = pd.read_sql_query(data_query, cnx)

    # Create a copy of the layer for possible modifications
    layers_new = layers.rename(columns={'codigo_clc':'codigo_clc_new'})
#-------------------------------------------------------------------------------------------------------------
    # Determines the number of existing categories in the shape layer
    column_values = layers_new[["cobertura", "codigo_clc_new"]].values
    matrix_data= np.vstack({tuple(e) for e in column_values}) # 11 x 2
    n = len(matrix_data[:,0]) # 11
    
    sum_cover = [[None for unique_values in range(3)] for unique_values in range(n)] # 11 x 3

    # Creates a list with the category name, sum of area and cod of cover
    for i in range(n):
        idx = layers_new.index[layers_new['cobertura'] == matrix_data[i,0]].tolist()
        sum_cover[i][0] = matrix_data[i,0]
        sum_cover[i][1] = sum(layers_new.iloc[idx]["area_ha"])
        sum_cover[i][2] = matrix_data[i, 1]
    return sum_cover
#-------------------------------------------------------------------------------------------------------------
    ## Determines the number of existing categories in the shape layer
    # column_values = layers_new[["cobertura", "codigo_clc_new"]].values
    # matrix_data= np.vstack({tuple(e) for e in column_values}) # 11 x 2
    # unique_values = sorted(pd.unique(matrix_data[:,0]))
    # unique_cod = ['232', '222', '311', '322', '411', '231', '331', '121', '131', '313', '334']
    # n = len(unique_values) # 11
    
    # sum_cover = [[None for unique_values in range(3)] for unique_values in range(n)] # 11 x 3

    # # Creates a list with the category name, sum of area and cod of cover
    # for i in range(n):
    #     idx = layers_new.index[layers_new['cobertura'] == unique_values[i]].tolist()
    #     sum_cover[i][0] = unique_values[i]
    #     sum_cover[i][1] = sum(layers_new.iloc[idx]["area_ha"])
    #     sum_cover[i][2] = unique_cod[i]
    # return sum_cover
#----------------------------------------------------------------------------------------------------------------

    # # define el nivel a usar en la agrupación de capas ¿debería ser menor o igual a min_level?
    # # num_digits = 2

    # cod = layers_new['codigo_clc_new']
    # cod_new = [None for cod in range(len(cod))]

    # for i in range(len(cod)):
    #     num_str = str(cod[i])
    #     cod_new[i] = len(num_str)
    #     layers_new['codigo_clc_new'][i] = num_str[0:num_digits]

    # # min_level = min(cod_new)

    # column_values = layers_new[["codigo_clc_new"]].values.ravel()
    # unique_values =  pd.unique(column_values) # numero de coberturas diferentes para el nivel establecido
    # n = len(unique_values)
    # # sum_cover = [None for unique_values in range(n)]
    # sum_cover = [[None for unique_values in range(2)] for unique_values in range(n)]

    # # crea una lista con los digitos del nivel y la suma de las shape_area ¿Cuales son las unidades de área?
    # for i in range(len(unique_values)):
    #     idx = layers_new.index[layers_new['codigo_clc_new'] == unique_values[i]].tolist()
    #     sum_cover[i][0] = unique_values[i]
    #     sum_cover[i][1] = sum(layers_new.iloc[idx]["area_ha"])

    # return sum_cover
