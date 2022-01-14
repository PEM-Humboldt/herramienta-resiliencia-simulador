
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def initial_cover(num_digits):
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
    
    layers = pd.read_sql_query('SELECT * FROM public.cobert_tillava', cnx)
    
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
