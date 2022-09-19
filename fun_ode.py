import numpy as np
import random
# import sys
# sys.path.insert(0, './ModuloAgua')
# import WaterFlows as WaterFlows
# import ConsumptionFlows as ConsumptionFlows
import pandas as pd
from ModuloAgua import WaterFlows
from ModuloDiversidadActividadesProductivas import PopulationFlows
from ModuloTejidoSocial import SocialFabric
from ModuloTejidoSocial import SocioenvironmentalConflicts
from ModuloTejidoSocial import SF_auxiliary

def differential_equations(x0, t, cover_rates, cover_rates_t, nx0_cover, dw, dConect, dp, dsf):
     
    derivatives = np.zeros(len(x0))
    ColEA, EnfInt, IntCom, TranConsConfColAct, TranConsConfCAgua, mca, mcf, mcb = SF_auxiliary.SF_auxiliary_variables(x0, dsf)
    
    # 1- soil covers module
    for k in range(nx0_cover):
        derivatives[k] = sum(x0[0:nx0_cover]*cover_rates[k][:]) - sum(x0[k]*cover_rates_t[k][:])
              
    # 2- water resource module
    
    PAE = sum(x0[13:16])
    Infil, FS, Perco, DH = WaterFlows.water_inputs_outputs(x0, dw, mca, PAE)

    derivatives[k + 1] = Infil - DH - FS - Perco
    
    # 3- habitat and diversity of ecological functions
    
    tConectBO = (dConect[1,1] - dConect[0,1]) / (dConect[3,1] - dConect[2,1])
    derivatives[k + 2] = tConectBO * x0[12] 
    
    # 4- diversity of economic activities
    tNaciPAE = dp[0,1]
    tCreciPoET = dp[1,1]  
    tEnvejPEA = dp[2,1]
    tMortaNoNa = dp[3,1]
    tMortaPoET = dp[4,1]
    tMortaPoAM = dp[5,1]
    InmigracionNoNa = dp[6,1]
    InmigracionPoET = dp[7,1]
    InmigracionPoAM = dp[8,1]
    EmigracionNoNa = dp[9,1]
    EmigracionPoET = dp[10,1]
    EmigracionPoAM = dp[11,1]
    NoNa = x0[13]
    PoET = x0[14]
    PoAM = x0[15]

    derivatives[k + 3] = tNaciPAE * PAE + InmigracionNoNa - tCreciPoET * NoNa - tMortaNoNa * NoNa - EmigracionNoNa
    derivatives[k + 4] = tCreciPoET * NoNa + InmigracionPoET - tEnvejPEA * PoET - tMortaPoET * PoET - EmigracionPoET
    derivatives[k + 5] = tEnvejPEA * PoET + InmigracionPoAM - tMortaPoAM * PoAM - EmigracionPoAM 
    
    # 4- social fabric 
    
    derivatives[k + 6] = SocialFabric.social_fabric_increase(x0, dsf, dp, ColEA, EnfInt) - SocialFabric.social_fabric_decrease(x0, dsf, IntCom)
    derivatives[k + 7] = SocioenvironmentalConflicts.conflict_increment(x0, dsf, EnfInt) - SocioenvironmentalConflicts.conflict_tranformation(x0, TranConsConfColAct, TranConsConfCAgua)
    
    return derivatives