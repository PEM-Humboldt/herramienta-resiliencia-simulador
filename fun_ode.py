import numpy as np
import random
# import sys
# sys.path.insert(0, './ModuloAgua')
# import WaterFlows as WaterFlows
# import ConsumptionFlows as ConsumptionFlows
import pandas as pd
import math
from ModuloAgua import WaterFlows
from ModuloAgua import ConsumptionFlows
from ModuloDiversidadActividadesProductivas import PopulationFlows
from ModuloTejidoSocial import SocialFabric
from ModuloTejidoSocial import SocioenvironmentalConflicts

def differential_equations(x0, t, cover_rates, cover_rates_t, nx0_cover, dw, dp, dsf):
    
    # 1- soil covers module
    derivatives = np.zeros(len(x0))
    for k in range(nx0_cover):
        derivatives[k] = sum(x0[0:nx0_cover]*cover_rates[k][:]) - sum(x0[k]*cover_rates_t[k][:])
        
     # 4- social_fabric 
    pmPerProgParCom = dsf[22, 1]
    pPer_1ProgParCom = dsf[23, 1]
    pPer_2ProgParCom = dsf[24, 1]
    IntCom = dsf[25,1]
    facTransConsCSA_ColAc = dsf[20, 1]
    facTransConsCSA_CuAg = dsf[19, 1]
    ProgIyP = math.trunc(pPer_1ProgParCom * pPer_2ProgParCom * x0[13] / pmPerProgParCom)
    ColEA = IntCom * np.log((ProgIyP + 1))
    TransCSA_ColEA = (facTransConsCSA_ColAc * ColEA) / 15
    
    tCreEnfIntegr_Cobi = dsf[12:18, 1]
    pos_transA = [0, 1, 5, 7, 8, 10] 
    Cobi_EnfIntegr = x0[pos_transA]
    EnfIntefr_Cobi = np.zeros(len(Cobi_EnfIntegr))
    for i in range(len(Cobi_EnfIntegr)):
        if Cobi_EnfIntegr[i] > 0:
            EnfIntefr_Cobi[i] = tCreEnfIntegr_Cobi[i] * x0[14]
        else:
            EnfIntefr_Cobi[i] = 0
    PCuAg_Cobi = dsf[0:6, 1]
    PCuFau_Cobi = dsf[6:12, 1]
    mca = sum(PCuAg_Cobi * EnfIntefr_Cobi) / len(EnfIntefr_Cobi)
    mcf = sum(PCuFau_Cobi * EnfIntefr_Cobi) / len(EnfIntefr_Cobi)
    
    TransCSA_CuiA = (mca * facTransConsCSA_CuAg) / 2

    derivatives[k + 4] = SocialFabric.social_fabric_increase(x0, dsf, dp, ColEA, EnfIntefr_Cobi) - SocialFabric.social_fabric_decrease(x0, dsf, IntCom)
    derivatives[k + 5] = SocioenvironmentalConflicts.conflict_increment(x0, dsf, EnfIntefr_Cobi) - SocioenvironmentalConflicts.conflict_tranformation(x0, TransCSA_ColEA, TransCSA_CuiA)

        
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
        
    return derivatives