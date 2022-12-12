import numpy as np
import random
# import sys
# sys.path.insert(0, './ModuloAgua')
# import WaterFlows as WaterFlows
# import ConsumptionFlows as ConsumptionFlows
import pandas as pd
from ModuloAgua import WaterFlows
from ModuloDiversidadActividadesProductivas import PopulationFlows
from ModuloTejidoSocial import SocialTissue
from ModuloTejidoSocial import SocioenvironmentalConflicts
from ModuloTejidoSocial import SF_auxiliary
from condiciones_iniciales import common_interes
from ModuloDisponibilidadHabitat import Habitat_Espi

def differential_equations(x0, t, cover_rates, cover_rates_t, nx0_cover, dw, dConect, dp, dsf, x_0, parametersPath, workspace, dhealth, dci):
     
    derivatives = np.zeros(len(x0))
    
    AN = x0[2] + x0[3] + x0[4]
    AE = sum(x0[0:11])
    Prod_usos = x0[0] + x0[1] + x0[8]
    HabitatESi = Habitat_Espi.habitat_area_Espi(x_0[2], x0[2],workspace)
    num_Espi = len(HabitatESi)
    
    tOACobj = dp[12:16,1]
    posCobj = [0, 1, 5, 8]
    VacOAci = dp[16:30,1]
    pPoEcAc = dp[30,1]
    VacOCobj = (tOACobj * x0[posCobj])
    PoETEA = (pPoEcAc * x0[14])
    PoOcu = sum(VacOCobj) + sum(VacOAci) - PoETEA
    
    if PoOcu >= 0:
        IndVacOpup = 1
    else:
        IndVacOpup = 0
        
    Num_UPA = dhealth[2, 1]
    Num_UPA_AutCons = dhealth[3, 1]
    Autoconsumo = Num_UPA_AutCons / Num_UPA
    Ind_pobreza = dhealth[4, 1]
 
    IntCom = common_interes.IntCom_fun(AN, AE, Prod_usos, HabitatESi, num_Espi, IndVacOpup, x0[12], Autoconsumo, Ind_pobreza, dci)
    # print(IntCom)
    
    ColEA, EnfInt, TranConsConfColAct, TranConsConfCAgua, mca, mcf, mcb, ProgIyP = SF_auxiliary.SF_auxiliary_variables(x0, dsf, IntCom)
     
    # 1- soil covers module
    for k in range(nx0_cover):
        tCobiCobj = cover_rates[k][:]
        tCobjCobi = cover_rates_t[:][k]
        
        derivatives[k] = sum(tCobjCobi * x0[0:nx0_cover]) - sum(tCobiCobj * x0[k])
              
    # 2- water resource module
    
    PAE = ((x0[13]) + (x0[14]) + (x0[15]))
    Infil, FS, Perco, DH = WaterFlows.water_inputs_outputs(x0, dw, mca, PAE)

    derivatives[k + 1] = Infil - DH - FS - Perco
    
    # 3- habitat and diversity of ecological functions
    Conect_ano1 = dConect[0,1]
    Conect_ano2 = dConect[1,1]
    tConectAN = (((Conect_ano2 - Conect_ano1) / (dConect[3,1] - dConect[2,1])))
    derivatives[k + 2] = tConectAN * x0[12]
    
    # 4- diversity of economic activities
    tNaciPAE = dp[0,1]
    tCreciPoET = dp[1,1]  
    tEnvejPEA = dp[2,1]
    tMortaNoNa = dp[3,1]
    tMortaPoET = dp[4,1]
    tMortaPoAM = dp[5,1]
    InmigracionNoNa = dp[6,1]
    InmigracionPoET = dp[7,1]
    InmigracionPoAM = dp[8,1]
    EmigracionNoNa = dp[9,1]
    EmigracionPoET = dp[10,1]
    EmigracionPoAM = dp[11,1]
    tFortEmpren = dp[31, 1]
    tFortDivInclu = dp[32, 1]
    VigenciaPersFortHabEmpren = dp[33, 1]
    VigenciaPersFortDivInclu = dp[34, 1]
    

    NoNa = (x0[13])
    PoET = (x0[14])
    PoAM = (x0[15])
    PersFortHabEmpren = (x0[16])
    PersFortDivInclu = (x0[17])

    derivatives[k + 3] = tNaciPAE * PAE + InmigracionNoNa - tCreciPoET * NoNa - tMortaNoNa * NoNa - EmigracionNoNa
    derivatives[k + 4] = tCreciPoET * NoNa + InmigracionPoET - tEnvejPEA * PoET - tMortaPoET * PoET - EmigracionPoET
    derivatives[k + 5] = tEnvejPEA * PoET + InmigracionPoAM - tMortaPoAM * PoAM - EmigracionPoAM
    
    PAE0 = (x_0[13]) + (x_0[14]) + (x_0[15])
    tEmigPoET = (EmigracionPoET / PAE0)
    tDisPersFortHabEmpren = tMortaPoET + tEnvejPEA + tEmigPoET
    derivatives[k + 6] = tFortEmpren * pPoEcAc * PoET - VigenciaPersFortHabEmpren * tDisPersFortHabEmpren * PersFortHabEmpren
    
    tDisPersFortDivInclu = (tMortaNoNa + tMortaPoET + tMortaPoAM) / 3 + (EmigracionNoNa + EmigracionPoET + EmigracionPoAM) / (3 * PAE0)
    derivatives[k + 7] = tFortDivInclu * PAE - VigenciaPersFortDivInclu * tDisPersFortDivInclu * PersFortDivInclu
    
    # 5- social fabric 
    
    derivatives[k + 8] = SocialTissue.social_fabric_increase(x0, dsf, ColEA, EnfInt, PAE) - SocialTissue.social_fabric_decrease(x0, dsf, IntCom)
    derivatives[k + 9] = SocioenvironmentalConflicts.conflict_increment(x0, dsf, EnfInt) - SocioenvironmentalConflicts.conflict_tranformation(x0, TranConsConfColAct, TranConsConfCAgua)
    
    return derivatives