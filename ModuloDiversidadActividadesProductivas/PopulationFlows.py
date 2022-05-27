

def population_inputs(x0, dp):
    tPMig = dp[0, 1]
    tINPAE = dp[1, 1]

    sum_flows_in = tPMig + tINPAE * x0[12]
    return sum_flows_in

def population_outputs(x0, dp):

    tDFPAE = dp[2, 1]
    tEMig = dp[3, 1]
        
    sum_flows_out = tDFPAE * x0[12] + tEMig * x0[12]
    return sum_flows_out