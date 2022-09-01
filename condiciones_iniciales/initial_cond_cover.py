import pandas as pd
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

    # Determines the number of existing categories in the shape layer
    column_values = layers_new[["cobertura"]].values.ravel()

    # number of different covers
    unique_values =  pd.unique(column_values)
    n = len(unique_values)


    sum_cover = [[None for unique_values in range(2)] for unique_values in range(n)]

    # Creates a list with the category name and sum of area
    for i in range(len(unique_values)):
        idx = layers_new.index[layers_new['cobertura'] == unique_values[i]].tolist()
        sum_cover[i][0] = unique_values[i]
        sum_cover[i][1] = sum(layers_new.iloc[idx]["area_ha"])

    return sum_cover

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
