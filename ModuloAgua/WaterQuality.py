
def Wquality(x0, dw, mca):
    
    Iacti = dw[26:37,1]
    RACobi = x0[0:11]/sum(x0)
    
    WqualityIndex = (1 + mca) / (1 + sum(RACobi * Iacti))
    return WqualityIndex