

def population_inputs(x0, dp):
    Mig = dp[21, 1]
    tINPAE = dp[22, 1]

    sum_flows_in = Mig + tINPAE * x0[12]
    return sum_flows_in

def population_outputs(x0, dp):

    tDFPAE = dp[23, 1]
    tEMig = dp[24, 1]
        
    sum_flows_out = tDFPAE * x0[12] + tEMig * x0[12]
    return sum_flows_out