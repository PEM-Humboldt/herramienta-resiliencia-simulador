import numpy as np

def Airquality(AN, transA, dav, pos_AN, pos_transA, LongVias):
    pPm10Acij = dav[12:23, 1]
    pPm10Aci = pPm10Acij[pos_transA]
    pPm10Acj = pPm10Acij[pos_AN]
    pPm10Ac_vias = dav[23, 1]
    
    AirqualityIndex = (sum(pPm10Aci * transA) + pPm10Ac_vias * LongVias) / (1+sum(pPm10Acj * AN))
    return AirqualityIndex

def Ladscapequality(AN, transA):
    LadscapequalityIndex = sum(AN) / (1 + sum(transA))
    return LadscapequalityIndex

def SoundPressurequality(AN, transA, dav, pos_AN, pos_transA, LongVias):
    pmDcAcij = dav[0:11, 1]
    pmDcAci = pmDcAcij[pos_transA]
    pmDcAcj = pmDcAcij[pos_AN]
    pmDcAc_vias = dav[12, 1]
    
    SoundPressurequalityIndex = (sum(pmDcAci * transA) + pmDcAc_vias * LongVias) / (1+sum(pmDcAcj * AN))
    return SoundPressurequalityIndex