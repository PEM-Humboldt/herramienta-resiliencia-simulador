from operator import index
import pandas as pd

def IntCom_fun(AN, AE, Prod_usos, HabitatESi, num_Espi, IndVacOpup, Conect, Autoconsumo, Ind_pobreza, dci):
    protected_areas = dci[0, 1]
    BuePracAgro = dci[1, 1]
    BuePracUExt = dci[2, 1]
    governance = dci[3:7, 1] 
    sum_pyg = 1-(governance[0]*(governance[0]-1) + governance[1]*(governance[1]-1)
               + governance[2]*(governance[2]-1) + governance[3]*(governance[3]-1)) / (sum(dci[3:7, 1]) * (sum(dci[3:7, 1]) - 1))
    if governance[0] > 0:
        governance[0] = 1
    
    if governance[1] > 0:
        governance[1] = 1
        
    if governance[2] > 0:
        governance[2] = 1
        
    if governance[3] > 0:
        governance[3] = 1
    
        
    
    Comm_int = (protected_areas + BuePracAgro + BuePracUExt + sum(governance) + AN/AE + (2/3)**Conect + (sum(HabitatESi)/num_Espi) / AE + Prod_usos/AE + (1-Ind_pobreza) + IndVacOpup + Autoconsumo) / 3.2
    
    return Comm_int, sum_pyg