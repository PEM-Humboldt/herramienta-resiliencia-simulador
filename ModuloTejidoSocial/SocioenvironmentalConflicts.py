

def conflict_increment(x0, dsf, EnfInt):
    # print(x0[17])
    fIncConfSocAm = (0.1 * dsf[0, 1]) / 300
    IncConfSocAm = (fIncConfSocAm * x0[19]) ** EnfInt
    return IncConfSocAm

def conflict_tranformation(x0, TranConsConfColAct, TranConsConfCAgua):

    TransConfSocAm =  x0[19] * (TranConsConfColAct + TranConsConfCAgua)
    return TransConfSocAm