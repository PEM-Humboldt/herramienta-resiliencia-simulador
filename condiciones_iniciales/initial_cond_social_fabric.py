import pandas as pd

def initial_social_fabric(parametersPath):

    data = pd.read_excel (parametersPath, sheet_name='initial_conditions')
    df = pd.DataFrame(data, index=[7, 8, 9, 10], columns= ['Nombre', 'Valor'])
    SF_CnSA_level = df.to_numpy()
    return SF_CnSA_level
