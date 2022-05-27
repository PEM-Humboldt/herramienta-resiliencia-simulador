import pandas as pd

def initial_water():
    
    data = pd.read_excel (r'./condiciones_iniciales/parameters.xlsx', sheet_name='initial_conditions')
    df = pd.DataFrame(data, index=[0, 2], columns= ['Nombre', 'Valor'])
    vol_water = df.to_numpy()
    # print(vol_water[1,0])
    return vol_water