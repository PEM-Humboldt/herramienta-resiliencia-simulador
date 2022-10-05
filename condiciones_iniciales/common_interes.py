from operator import index
import pandas as pd

def IntCom_fun(parametersPath):
    data = pd.read_excel (parametersPath, sheet_name='Common_interes')
    df = pd.DataFrame(data, columns= ['Indicador', 'Valor'])
    df = df.to_numpy()
    natural_capital = df[0:2, 1]
    production = df[2:4, 1]
    wellbeing = df[4:6, 1]
    governance = df[6:12, 1]
    
    Comm_int = (sum(natural_capital) + sum(production) + sum(wellbeing) + sum(governance)) / 2
    
    return Comm_int