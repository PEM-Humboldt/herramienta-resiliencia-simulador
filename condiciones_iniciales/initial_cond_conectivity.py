import pandas as pd

def initial_conectBO(parametersPath):
    
    data = pd.read_excel (parametersPath, sheet_name='initial_conditions')
    df = pd.DataFrame(data, index=[1], columns= ['Nombre', 'Valor'])
    ConectBO = df.to_numpy()
    
    return ConectBO