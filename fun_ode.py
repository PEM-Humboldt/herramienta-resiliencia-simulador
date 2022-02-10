import numpy as np

def differential_equations(x0, t, cover_rates, cover_rates_t):
    
    # modulo coberturas
    nx0 = len(x0)
    derivatives = np.zeros(nx0)
    # rates_cover_t = cover_rates.transpose()
    
    # suma = 0
    # for k in range(nx0):
    #     for p in range(nx0):
    #         if k != p:
    #             derivatives[k][p] = sum(x0[k]*cover_rates[k][p]) - sum(x0[p]*cover_rates_t[k][p])
    #         else:
    #             derivatives[k][p] = 0
    #     # print(x0)
        
    # return derivatives
    
    for k in range(nx0):
        derivatives[k] = sum(x0*cover_rates[k][:]) - sum(x0[k]*cover_rates_t[k][:])
        # print(x0)
        
    return derivatives