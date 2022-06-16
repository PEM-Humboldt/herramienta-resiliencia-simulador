import pandas as pd

def initial_population():
    
    data = pd.read_excel (r'./condiciones_iniciales/parameters.xlsx', sheet_name='initial_conditions')
    df = pd.DataFrame(data, index=[2], columns= ['Nombre', 'Valor'])
    population_level = df.to_numpy()
    return population_level