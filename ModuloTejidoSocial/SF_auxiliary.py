import math
import numpy as np

def SF_auxiliary_variables(x0, dsf, IntCom):
    pmPerProgParCom = dsf[4, 1]
    pPer_1ProgParCom = dsf[5, 1]
    pPer_2ProgParCom = dsf[6, 1]
    # IntCom = dsf[11, 1]
    
    # if t == tmin:
    #     IntCom = 3 # dsf[25,1]
    # else:
    #     IntCom = common_interes(AN, connectivity, AirQualityIndex, WaterQualityIndex, ATrans, Population, PovertyIndex, Ocupation,
    #                DivSisAliLoc, ProgIyP)
    
    facTransConsCSA_ColAc = dsf[1, 1]
    facTransConsCSA_CuAg = dsf[2, 1]
    PAE = sum(x0[13:16])
    ProgIyP = math.trunc(pPer_1ProgParCom * (1+pPer_2ProgParCom) * PAE / pmPerProgParCom)
    ColEA = IntCom * np.log((ProgIyP + 1))
    TranConsConfColAct = (facTransConsCSA_ColAc * ColEA) / 15
    
    tCrecEI = dsf[3, 1]
    EnfInt = tCrecEI * (IntCom / 5) * x0[18]
    
    pCagua = dsf[7, 1]
    pCfauna = dsf[8, 1]
    pCbosque = dsf[9, 1]
    mca = EnfInt ** (1-pCagua)
    mcf = EnfInt ** (1-pCfauna)
    mcb = EnfInt ** (1-pCbosque)
    
    TranConsConfCAgua = (facTransConsCSA_CuAg * ColEA) / 2
    return ColEA, EnfInt, TranConsConfColAct, TranConsConfCAgua, mca, mcf, mcb