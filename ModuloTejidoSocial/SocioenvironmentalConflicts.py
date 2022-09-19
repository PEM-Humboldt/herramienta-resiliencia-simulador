

def conflict_increment(x0, dsf, EnfInt):
    # print(x0[17])
    fIncConfSocAm = dsf[0, 1]
    IncConfSocAm = (fIncConfSocAm * x0[17]) / (1+ EnfInt)
    return IncConfSocAm

def conflict_tranformation(x0, TranConsConfColAct, TranConsConfCAgua):

    TransConfSocAm =  x0[17] * (TranConsConfColAct + TranConsConfCAgua)
    return TransConfSocAm