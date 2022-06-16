

def water_inputs(x0, dw):
    EaOc = dw[34,1]
    tprpm = dw[32,1]
    fac = dw[33,1]
    
    AT = sum(x0[0:11])
    sum_flows_in = tprpm*fac*AT + EaOc
    return sum_flows_in

def water_outputs(x0, dw, RH, tsaoc, Um_RH):

    Fpera_min = dw[36,1] 
    
    if RH > Um_RH:
        Fpera = Fpera_min
    else:
        Fpera = 1
        
    sum_flows_out = Fpera*x0[11] + tsaoc*x0[11]
    return sum_flows_out