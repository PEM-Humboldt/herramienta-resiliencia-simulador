import pandas as pd

def initial_population(parametersPath):

    data = pd.read_excel (parametersPath, sheet_name='initial_conditions')
    df = pd.DataFrame(data, index=[2], columns= ['Nombre', 'Valor'])
    population_level = df.to_numpy()
    return population_level
