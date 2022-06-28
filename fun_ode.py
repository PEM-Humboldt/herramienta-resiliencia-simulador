import numpy as np
import random
# import sys
# sys.path.insert(0, './ModuloAgua')
# import WaterFlows as WaterFlows
# import ConsumptionFlows as ConsumptionFlows
import pandas as pd
from ModuloAgua import WaterFlows
from ModuloAgua import ConsumptionFlows
from ModuloDiversidadActividadesProductivas import PopulationFlows
from ModuloTejidoSocial import SocialFabric
from ModuloTejidoSocial import SocioenvironmentalConflicts
from ModuloTejidoSocial import SF_auxiliary

def differential_equations(x0, t, cover_rates, cover_rates_t, nx0_cover, dw, dp, dsf):    
    derivatives = np.zeros(len(x0))
    ColEA, EnfIntefr_Cobi, IntCom, TransCSA_ColEA, TransCSA_CuiA, mca, mcf = SF_auxiliary.SF_auxiliary_variables(x0, dsf)
    
    # 1- soil covers module
    for k in range(nx0_cover):
        derivatives[k] = sum(x0[0:nx0_cover]*cover_rates[k][:]) - sum(x0[k]*cover_rates_t[k][:])
              
    # 2- water resource module
    tretCobj = dw[0:11, 1]
    Capr = sum(tretCobj * x0[0:11])
    RH = x0[11] * Capr
    Um_RH = dw[35, 1]
    tsaoc_min = dw[37, 1]
    if RH > Um_RH:
        tsaoc = tsaoc_min
    else:
        tsaoc = 1
    derivatives[k + 1] = WaterFlows.water_inputs(x0, dw) - WaterFlows.water_outputs(x0, dw, RH, tsaoc, Um_RH)
    derivatives[k + 2] = ConsumptionFlows.flow_input(x0, dw, tsaoc) - ConsumptionFlows.water_consumption(dw, mca)
    
    
     # 3- diversity of economic activities
    derivatives[k + 3] = PopulationFlows.population_inputs(x0, dp) - PopulationFlows.population_outputs(x0, dp)
    
    # 4- social fabric 
    
    derivatives[k + 4] = SocialFabric.social_fabric_increase(x0, dsf, dp, ColEA, EnfIntefr_Cobi) - SocialFabric.social_fabric_decrease(x0, dsf, IntCom)
    derivatives[k + 5] = SocioenvironmentalConflicts.conflict_increment(x0, dsf, EnfIntefr_Cobi) - SocioenvironmentalConflicts.conflict_tranformation(x0, TransCSA_ColEA, TransCSA_CuiA)
    
    return derivatives