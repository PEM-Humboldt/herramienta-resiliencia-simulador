import numpy as np
# import sys
# sys.path.insert(0, './ModuloAgua')
# import WaterFlows as WaterFlows
# import ConsumptionFlows as ConsumptionFlows
import pandas as pd
from ModuloAgua import WaterFlows
from ModuloAgua import ConsumptionFlows

def differential_equations(x0, t, cover_rates, cover_rates_t, nx0_cover,dw, mca):
    
    # 1- soil covers module
    derivatives = np.zeros(len(x0))
    for k in range(nx0_cover):
        derivatives[k] = sum(x0[0:nx0_cover]*cover_rates[k][:]) - sum(x0[k]*cover_rates_t[k][:])
        
    # 2- water resource module
    tretCobj = dw[4:15,1]
    Capr = sum(tretCobj * x0[0:11])
    RH = x0[11] * Capr
    # print(x0[11])
    tsaoc_min = dw[15,1]
    
    if RH > 0:
        tsaoc = tsaoc_min
    else:
        tsaoc = 1
        
    derivatives[k + 1] = WaterFlows.water_inputs(x0, dw) - WaterFlows.water_outputs(x0, dw, RH, tsaoc)
    
    derivatives[k + 2] = ConsumptionFlows.flow_input(x0, dw, tsaoc) - ConsumptionFlows.water_consumption(dw, mca)
    
    return derivatives