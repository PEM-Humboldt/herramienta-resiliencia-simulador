

def flow_input(x0, dw, tsaoc):
    pac = dw[38,1]
    sum_water_flows = pac*tsaoc*x0[11]
    return sum_water_flows

def water_consumption(dw, mca):
    tpca = dw[39,1]
    consumptios = dw[22:32,1]
    sum_water_consumption = tpca*mca*sum(consumptios)
    return sum_water_consumption