
import math

def water_inputs_outputs(x0, dw, mca, PAE): # Infiltration
    Qm = dw[0,1]
    ConsIndusEner = dw[1,1]
    ConsOtros = dw[2,1]
    T  = dw[3,1]
    tConsDomes = dw[4,1]
    pR = dw[5,1]
    rho1 = dw[6,1]
    pCampCam = dw[7,1]
    pPtoMz = dw[8,1]
    pPHA = dw[9,1]
    pPor = dw[10,1]
    tPerco = dw[11,1]
    ConsACobj = dw[12:20,1]
    tFS = dw[20,1]
    PPT = dw[21,1]
    
     
    L = 300 + 0.25 * T + 0.0025 * T ** 2
    ETR = PPT / math.sqrt(0.9 + (PPT / L) ** 2)
    ConsHDomes = tConsDomes * PAE # * mca ** (1 / 4)  # revisar esta ecuación 
    EsC = Qm + ConsIndusEner + ConsHDomes + ConsOtros
    
    AT = sum(x0[0:11])
    AlmaSat = 10000 * AT * pPHA * pPor
    pPtoMz = pPtoMz * AlmaSat
    CapCam = pCampCam * AlmaSat
    rho = rho1 * (CapCam - pPtoMz) + pPtoMz
    
    RetHs = x0[11]
    if RetHs < rho:
        R = pR * Qm
    else:
        R = 0
    
    Infil = 10 * AT * (PPT - ETR) + R - EsC
    
    if RetHs > AlmaSat:
        FS = tFS * (RetHs - AlmaSat)
    else:
        FS = 0
        
    Perco = tPerco * RetHs
    DH_AHeter = ConsACobj[2] * x0[0]
    DH_AHomo = ConsACobj[3] * x0[1]
    DH_ABO = ConsACobj[0] * x0[2]
    DH_AHerb = ConsACobj[1] * x0[3]
    DH_APastHomo = ConsACobj[4] * x0[5]
    DH_ADveget = ConsACobj[5] * x0[6]
    DH_AVSecun = ConsACobj[6] * x0[9]
    DH_ADegra = ConsACobj[7] * x0[10]
    
    DH = DH_AHeter + DH_AHomo + DH_ABO + DH_AHerb + DH_APastHomo + DH_ADveget + DH_AVSecun + DH_ADegra
    
    return Infil, FS, Perco, DH