import numpy as np

def social_fabric_increase(x0, dsf, dp, ColEA, EnfInt, PAE):
    # print(x0[16])
    DivSisCon = dp[32,1]
    DialSab = (ColEA ** DivSisCon) / 15
    social_fabric_increase_flow = EnfInt * DialSab * x0[18] * (1 - x0[18])
    return social_fabric_increase_flow

def social_fabric_decrease(x0, dsf, IntCom):
    tDeterTS = dsf[10, 1] 
    social_fabric_decrease_flow = tDeterTS * x0[18] * ((5 - IntCom) / 5)
    return social_fabric_decrease_flow