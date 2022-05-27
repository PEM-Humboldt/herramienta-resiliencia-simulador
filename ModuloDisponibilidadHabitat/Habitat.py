from turtle import pd
import numpy as np

def habitat_area(dh, AN, AN0):
    
    # Para el simulador, inicialmente se asume que ese 
    # 100% es el área actual de coberturas naturales. Pero debería ser mayor! AN0
    DpohaEs_imax = sum(AN0) * dh[0:10,1] 
    UEsi = DpohaEs_imax * dh[10:20,1]
    DpohaEs_i = sum(AN) * dh[0:10,1]
    AtemEs_i = abs((DpohaEs_i - UEsi) / DpohaEs_i)
    
    PdEs_i = np.zeros(len(UEsi))
    ExistenceEs_i = np.zeros(len(UEsi))
    for i in range(len(UEsi)):
        if DpohaEs_i[i] > UEsi[i]:
            PdEs_i[i] = 1 - AtemEs_i[i]
            ExistenceEs_i[i] = 1
        else:
            PdEs_i[i] = 1
            ExistenceEs_i[i] = 0
    
            
    return DpohaEs_i, PdEs_i, ExistenceEs_i

    