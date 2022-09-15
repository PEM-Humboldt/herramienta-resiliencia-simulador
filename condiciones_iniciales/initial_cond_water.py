import pandas as pd

def initial_water(parametersPath):

    data = pd.read_excel (parametersPath, sheet_name='initial_conditions')
    df = pd.DataFrame(data, index=[0], columns= ['Nombre', 'Valor'])
    vol_water = df.to_numpy()
    # print(vol_water[1,0])
    return vol_water
