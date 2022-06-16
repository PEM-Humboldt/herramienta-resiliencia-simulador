

def conflict_increment(x0, dsf, EnfIntefr_Cobi):
    FacIncrCS = dsf[18, 1]
    conflict_increment_flow = (FacIncrCS * x0[14]) / (1+ sum(EnfIntefr_Cobi))
    return conflict_increment_flow

def conflict_tranformation(x0, TransCSA_ColEA, TransCSA_CuiA):

    conflict_transformation_flow = (TransCSA_ColEA + TransCSA_CuiA) * x0[14]
    return conflict_transformation_flow