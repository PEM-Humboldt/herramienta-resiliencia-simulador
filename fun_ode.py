import numpy as np

def differential_equations(x0, t, rates_cover, rates_cover_t):
    
    # modulo coberturas
    nx0 = len(x0)
    derivatives = np.zeros(nx0)
    # rates_cover_t = rates_cover.transpose()
    
    # suma = 0
    # for k in range(nx0):
    #     for p in range(nx0):
    #         if k != p:
    #             derivatives[k][p] = sum(x0[k]*rates_cover[k][p]) - sum(x0[p]*rates_cover_t[k][p])
    #         else:
    #             derivatives[k][p] = 0
    #     # print(x0)
        
    # return derivatives
    
    for k in range(nx0):
        derivatives[k] = sum(x0*rates_cover[k][:]) - sum(x0*rates_cover_t[k][:])
        # print(x0)
        
    return derivatives