import numpy as np

def social_fabric_increase(x0, dsf, dp, ColEA, EnfIntefr_Cobi):
    DivSisCon = dp[29, 1]
    DialSab = (ColEA ** DivSisCon) / 15
    social_fabric_increase_flow = np.prod(EnfIntefr_Cobi) * DialSab * x0[14] * (1 - x0[14])
    return social_fabric_increase_flow

def social_fabric_decrease(x0, dsf, IntCom):
    tDeterTS = dsf[21, 1] 
    social_fabric_decrease_flow = tDeterTS * ((5 - IntCom) / 5) * x0[14]
    return social_fabric_decrease_flow