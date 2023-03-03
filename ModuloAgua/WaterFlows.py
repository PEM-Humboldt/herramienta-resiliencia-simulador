
import math

def water_inputs_outputs(x0, dw, mca, PAE, AE): # Infiltration
    DemEner = dw[0,1]
    DemHidrocar = dw[1,1]
    DemServi = dw[2,1]
    DemIndusConstruc = dw[3,1]
    DemAgrico = dw[4,1]
    DemMinero = dw[5,1]
    DemPecuario = dw[6,1]
    DemDomes = dw[7,1]
    
    tRetorEner = dw[8,1]
    tRetorHidrocar = dw[9,1]
    tRetorServi = dw[10,1]
    tRetorIndusConstruc = dw[11,1]
    tRetorAgrico = dw[12,1]
    tRetorMinero = dw[13,1]
    tRetorPecuario = dw[14,1]
    tRetorDomes = dw[15,1]

    Kc_Bosque = dw[16,1]
    Kc_Herba = dw[17,1]
    Kc_AgroHeter = dw[18,1]
    Kc_AgriHomo = dw[19,1]
    Kc_PastHomo = dw[20,1]
    Kc_VegSecund = dw[21,1]

    T = dw[22,1]
    PPT = dw[23,1]
    pR = dw[24,1]
    rho1 = dw[25,1]
    pCampCam = dw[26,1]
    pPtoMz = dw[27,1]
    pPHA = dw[28,1]
    pPor = dw[29,1]
    tPerco = dw[30,1]
    tFS = dw[31,1]
    OHTS  = dw[32,1]
    OHTD  = dw[33,1]

    RetHs = x0[11]
    AT = sum(x0[0:11])
    
    AlmaSat = 10000 * AT * pPHA * pPor
    
    L = 300 + 0.25 * T + 0.0025 * T ** 2
    ETR = PPT / math.sqrt(0.9 + (PPT / L) ** 2)
    
    if RetHs > AlmaSat:
        FS = tFS * (RetHs - AlmaSat)
    else:
        FS = 0
        
    EsC = OHTS + FS # OHTS
    
    Qm = OHTD - (PAE * DemDomes * (1 - tRetorDomes) * (1 - (mca ** 3) / 3) +
                 DemEner * (1 - tRetorEner) +
                 DemHidrocar * (1 - tRetorHidrocar) +
                 DemServi * (1 - tRetorServi) +
                 DemIndusConstruc * (1 - tRetorIndusConstruc) +
                 DemAgrico * (1 - tRetorAgrico) +
                 DemMinero * (1 - tRetorMinero) +
                 DemPecuario * (1 - tRetorPecuario))    
    
    pPtoMz = pPtoMz * AlmaSat
    CapCam = pCampCam * AlmaSat
    rho = rho1 * (CapCam - pPtoMz) + pPtoMz
    
    if RetHs < rho:
        R = pR * Qm
    else:
        R = 0
    
    # print(10 * AT * (PPT - ETR))
    if 10 * AT * (PPT - ETR) + R - EsC <= 0:
        Infil = 0
    else: 
        Infil = 10 * AT * (PPT - ETR) + R - EsC
    
    if RetHs > AlmaSat:
        FS = tFS * (RetHs - AlmaSat)
    else:
        FS = 0
        
    Perco = tPerco * 10 * AE
    
    ABO = x0[2]
    AHerba = x0[3]
    AAgroHeter = x0[0]
    AAgriHomo = x0[1]
    APastHomo = x0[5]
    AVegSecund = x0[9]
    DH = (ETR * Kc_Bosque * 10 * ABO + 
          ETR * Kc_Herba * 10 * AHerba + 
          ETR * Kc_AgroHeter * 10 * AAgroHeter + 
          ETR * Kc_AgriHomo * 10 * AAgriHomo + 
          ETR * Kc_PastHomo * 10 * APastHomo + 
          ETR * Kc_VegSecund * 10 * AVegSecund)
    
    return Infil, FS, Perco, DH