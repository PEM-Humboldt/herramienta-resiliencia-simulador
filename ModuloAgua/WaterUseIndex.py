
import math

def water_use_index(x0, dw): # Infiltration
    DemEner = dw[0,1]
    DemHidrocar = dw[1,1]
    DemServi = dw[2,1]
    DemIndusConstruc = dw[3,1]
    DemAgrico = dw[4,1]
    DemMinero = dw[5,1]
    DemPecuario = dw[6,1]
    DemDomes = dw[7,1]
    
    
    OHTD  = dw[33,1]
    T = dw[22,1]
    PPT = dw[23,1]
    
    L = 300 + 0.25 * T + 0.0025 * T ** 2
    ETR = PPT / math.sqrt(0.9 + (PPT / L) ** 2)
        
    IUA = (DemEner + DemHidrocar + DemServi + DemIndusConstruc + DemAgrico + DemMinero +
           DemPecuario + DemDomes) / OHTD
    
    return IUA