import math
import numpy as np

# def common_interes(AN, connectivity, AirQualityIndex, WaterQualityIndex, ATrans, Population, PovertyIndex, Ocupation,
#                    DivSisAliLoc, ProgIyP):
#     PracCAgua = 1
#     PracCFauna = 1
#     PractCBO = 1
#     BuPracProduc = 1
#     return IntCom

def SF_auxiliary_variables(x0, dsf):
    pmPerProgParCom = dsf[22, 1]
    pPer_1ProgParCom = dsf[23, 1]
    pPer_2ProgParCom = dsf[24, 1]
    IntCom = dsf[25,1]
    
    # if t == tmin:
    #     IntCom = 3 # dsf[25,1]
    # else:
    #     IntCom = common_interes(AN, connectivity, AirQualityIndex, WaterQualityIndex, ATrans, Population, PovertyIndex, Ocupation,
    #                DivSisAliLoc, ProgIyP)
    
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
    return ColEA, EnfIntefr_Cobi, IntCom, TransCSA_ColEA, TransCSA_CuiA, mca, mcf