from sqlalchemy import column
from condiciones_iniciales import initial_cond_cover
from condiciones_iniciales import initial_cond_water
from condiciones_iniciales import initial_cond_conectivity
from condiciones_iniciales import initial_cond_population
from condiciones_iniciales import initial_cond_social_tissue
from condiciones_iniciales import common_interes
from ModuloDisponibilidadHabitat import Habitat
from ModuloTejidoSocial import SF_auxiliary
from ModuloSalud import Health_auxiliary
from ModuloDisponibilidadHabitat import Habitat_Espi
from ModuloAgua import WaterUseIndex
# from ModuloDiversidadActividadesProductivas import Population
import fun_ode as ode
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import resilience_indicators
import sys
import getopt

workspace = ''
conditionsPath = r'./condiciones_iniciales/'
parametersFile = 'parameters.xlsx'
result_name = 'model_time_series.csv'
decimalSeparator='coma'

if sys.argv[1:]:
    opts = getopt.getopt(sys.argv[1:], "o:w:d:")[0]

    for opt, arg in opts:
        if (opt == '-o'):
            outputName = arg
        if (opt == '-w'):
            workspace = arg
        if (opt == '-d'):
            decimalSeparator = arg

    parametersFile = f'{workspace}_parameters.xlsx'
    result_name = f'{workspace}_{outputName}'

parametersPath = conditionsPath + parametersFile

# initial conditions for covers (Cobi)
data_cover = sorted(initial_cond_cover.initial_cover(workspace))

def f_cover(l):
    l2 = []
    for i in data_cover:
        for j in range(len(i)-2):
             l2.append((i[j], i[-2]))
    return l2

def g_cover(l):
    l2 = []
    for i in data_cover:
        for j in range(len(i)-2):
             l2.append((i[-1]))
    return l2

data1_cover = f_cover(data_cover)
data1_cover_cod = g_cover(data_cover)
data1_cover_name = [i for i,j in data1_cover]
data1_cover_value = [j for i,j in data1_cover]

# data1_cover_cod = data1_cover_cod[0:11]
# data1_cover_name = data1_cover_name[0:11]
# data1_cover_value = data1_cover_value[0:11]

num_cover = len(data1_cover_name)
unique_values_cod = ['232', '222', '311', '322', '411', '231', '331', '121', '131', '313', '334']
unique_values_cover = ['Agropecuario heterogeneo',
                    'Agrícola homogeneo',
                    'Bosques',
                    'Herbazales y arbustales',
                    'Humedales',
                    'Pasturas homogeneas',
                    'Suelos desprovistos de vegetación (natural)',
                    'Urbano - urbanizado',
                    'Usos extractivos',
                    'Vegetación secundaria o seminatural',
                    'Áreas degradadas']
if num_cover != 11:
    data0_cover = [[None for unique_values_cod in range(2)] for unique_values_cod in range(11)]
    
    for i in range(11):
        if (unique_values_cod[i] in data1_cover_cod[:]):
            idx = data1_cover_cod[:].index(unique_values_cod[i])
            data0_cover[i][0] = data1_cover_name[idx]
            data0_cover[i][1] = data1_cover_value[idx]
        else:
            data0_cover[i][0] = unique_values_cover[i]
            data0_cover[i][1] = 0
else:
    data0_cover = [[None for unique_values_cod in range(2)] for unique_values_cod in range(11)]
    for i in range(11):
        idx = data1_cover_cod[:].index(unique_values_cod[i])
        data0_cover[i][0] = data1_cover_name[idx]
        data0_cover[i][1] = data1_cover_value[idx]
        

x0_cover = [row[1] for row in data0_cover]
name_cover = [row[0] for row in data0_cover]
nc = len(x0_cover)
# conda install openpyxl if necessary
df = pd.read_excel (parametersPath, sheet_name='transformation_rates')
arr = df.to_numpy()
cover_rates = arr[0:nc,1:nc+1]

# initial volume of water retation
data0_water = initial_cond_water.initial_water(parametersPath)
x0_water =  [row[1] for row in data0_water]
name_water = [row[0] for row in data0_water]
data_water = pd.read_excel (parametersPath, sheet_name='water_parameters')
dw = pd.DataFrame(data_water, columns= ['Nombre', 'Valor'])
dw = dw.to_numpy()

# initial conectivity
data0_ConectBO = initial_cond_conectivity.initial_conectBO(parametersPath)
x0_ConectBO = [row[1] for row in data0_ConectBO]
name_ConectBO = [row[0] for row in data0_ConectBO]
data_ConectBO = pd.read_excel (parametersPath, sheet_name='Habitat_Availability')
dConect = pd.DataFrame(data_ConectBO, columns= ['Nombre', 'Valor'])
dConect = dConect.to_numpy()

# initial population in the study area
data0_population = initial_cond_population.initial_population(parametersPath)
x0_population =  [row[1] for row in data0_population]
name_population = [row[0] for row in data0_population]
data_population = pd.read_excel (parametersPath, sheet_name='Diversity_of_activities')
dp = pd.DataFrame(data_population, columns= ['Nombre', 'Valor'])
dp = dp.to_numpy()

# initial social fabric + socioenvironmental conflicts
data0_SF_CSA = initial_cond_social_tissue.initial_social_tissue(parametersPath)
x0_SF_CSAt=  [row[1] for row in data0_SF_CSA]
name_SF_CSAt = [row[0] for row in data0_SF_CSA]
x0_SF_CSA = x0_SF_CSAt[0:2]
name_SF_CSA = name_SF_CSAt[0:2]

data_SF_CSA = pd.read_excel (parametersPath, sheet_name='social_tissue')
dsf = pd.DataFrame(data_SF_CSA, columns= ['Nombre', 'Valor'])
dsf = dsf.to_numpy()

# initial health
data_health = pd.read_excel (parametersPath, sheet_name='Health')
dhealth = pd.DataFrame(data_health, columns= ['Nombre', 'Valor'])
dhealth = dhealth.to_numpy()

# initial common interest
data_common = pd.read_excel (parametersPath, sheet_name='Common_interes')
dci = pd.DataFrame(data_common, columns= ['Indicador', 'Valor'])
dci = dci.to_numpy()

# INTEGRATOR CONFIGURATION
tmin = x0_SF_CSAt[2]
tmax = x0_SF_CSAt[3] + 1
time = np.arange(tmin, tmax, 1)
name_year = np.array(['Año'])
ntime = len(time)

x0_cover = np.array(x0_cover)
nx0_cover = len(x0_cover)
cover_rates = np.array(cover_rates)
cover_rates_t = cover_rates.transpose()

x0_water = np.array(x0_water)
nx0_water = len(x0_water)

x0_ConectBO = np.array(x0_ConectBO)
nx0_ConectBO = len(x0_ConectBO)

x0_population = np.array(x0_population)
nx0_population = len(x0_population)

x0_SF_CSA = np.array(x0_SF_CSA)
nx0_SF_CSA = len(x0_SF_CSA)

# Integration by RK45
x_0 = np.concatenate((x0_cover, x0_water, x0_ConectBO, x0_population, x0_SF_CSA), axis=0) # [cover, water]
Ys = odeint(ode.differential_equations, x_0, time, args=(cover_rates, cover_rates_t, nx0_cover, dw, dConect, dp, dsf, x_0, parametersPath, workspace, dhealth, dci)) #+  random.uniform(-5000, 5000)
# SPECIAL INDICATORS

# 0. landscape diversity
ACob = Ys[:, 0:11] 
Yt = np.sum(Ys[:, 0:nx0_cover],axis = 1) # axis=1 --> add rows, axis=0 --> add columns
ACob_norm = ACob / Yt[0]
ACob_log = ACob_norm * np.log(ACob_norm)
ACob_log = np.nan_to_num(ACob_log)
Yt_log = -np.sum(ACob_log[:, 0:nx0_cover],axis=1)
name_Land_Div = np.array(['Diversidad del paisaje'])
NA = np.sum(Ys[:, 2:5], axis = 1)
name_NA = np.array(['Áreas naturales'])
name_AT = np.array(['Área total'])

# 1. Water quality
mca = np.zeros(ntime)
mcf = np.zeros(ntime)
mcb = np.zeros(ntime)
name_WQ = np.array(['ICA OD', 'ICA SST', 'ICA DQO', 'ICA CE', 'ICA pH'])
name_mv_original = np.array(['ICA agua promedio regional'])
name_mv_modificada = np.array(['ICA agua promedio regional con cuidado del agua'])
data_WQ = pd.read_excel (parametersPath, sheet_name='wate_quality')
dwq = pd.DataFrame(data_WQ, columns= ['ICA OD', 'ICA SST', 'ICA DQO', 'ICA CE', 'ICA pH'])
dwq = dwq.to_numpy()
ICAi = np.nanmean(dwq, axis=0)
ICAm = np.nanmean(ICAi)
ICAiv_original = np.transpose([[None for ICAi in range(ntime)] for ICAi in range(len(ICAi))])
ICAmv_original = [None for ICAm in range(ntime)]
ICAmv_modificada = [None for ICAm in range(ntime)]

# 2. Productive activities
tOACobj = dp[12:16,1]
posCobj = [0, 1, 5, 8]
VacOAci = dp[16:30,1]
pPoEcAc = dp[30,1]
Num_UPA = dhealth[2, 1]
Num_UPA_AutCons = dhealth[3, 1]
Autoconsumo = Num_UPA_AutCons / Num_UPA
Ind_pobreza = dhealth[4, 1]
EnfIntefr_Cobi = np.zeros(ntime)
ColEA = np.zeros(ntime)
IntCom = np.zeros(ntime)
sum_pyg = np.zeros(ntime)
TransCSA_ColEA = np.zeros(ntime)
TransCSA_CuiA = np.zeros(ntime)
ProgIyP = np.zeros(ntime)
for i in range(ntime):
    Prod_usos = Ys[i, 0] + Ys[i, 1] + Ys[i, 8]
    HabitatESi = Habitat_Espi.habitat_area_Espi(x_0[2], Ys[i, 2],workspace)
    num_Espi = len(HabitatESi)
    VacOCobj = tOACobj * Ys[i, posCobj]
    PoETEA = pPoEcAc * Ys[i, 14]
    PoOcu = sum(VacOCobj) + sum(VacOAci) - PoETEA
    
    if PoOcu >= 0:
        IndVacOpup = 1
    else:
        IndVacOpup = 0
    IntCom[i], sum_pyg[i] = common_interes.IntCom_fun(sum(Ys[i, 2:5]), sum(Ys[i, 0:11]), Prod_usos, HabitatESi, num_Espi, IndVacOpup, Ys[i, 12], Autoconsumo, Ind_pobreza, dci)

    ColEA[i], EnfIntefr_Cobi[i],TransCSA_ColEA[i], TransCSA_CuiA[i], mca[i], mcf[i], mcb[i], ProgIyP[i] = SF_auxiliary.SF_auxiliary_variables(Ys[i,:], dsf, IntCom[i], x_0)
    ICAiv_original[i,:] = ICAi
    ICAmv_original[i] = ICAm
    ICAmv_modificada[i] = (ICAm / 4) * (1 + 2 * ICAm ** -(0.5+mca[i]))

## Abiotic variables

# 3. Air quality
name_AirQ = np.array(['ICA PM10', 'ICA PM 2.5', 'ICA CO', 'ICA SO2', 'ICA NO2', 'ICA O3'])
name_mv_AirQ = np.array(['ICA aire promedio regional'])
data_AirQ = pd.read_excel (parametersPath, sheet_name ='Air_quality')
dairq = pd.DataFrame(data_AirQ, columns= ['ICA PM10', 'ICA PM 2,5', 'ICA CO', 'ICA SO2', 'ICA NO2', 'ICA O3'])
dairq = dairq.to_numpy()
ICAairi = np.nanmean(dairq, axis=0)
ICAairm = 1-np.nanmean(ICAairi) / 500
ICAairiv = np.transpose([[None for ICAairi in range(ntime)] for ICAairi in range(len(ICAairi))])
ICAairmv = [None for ICAairm in range(ntime)]

for i in range(ntime):
    ICAairiv[i,:] = ICAairi
    ICAairmv[i] = ICAairm

# 4. Sound presure - Noise attenuation indicator
name_NoiseAte = np.array(['Atenuación día Agricola', 'Atenuación día Bosque',
                      'Atenuación día Herbazales', 'Atenuación día Humedales', 
                      'Atenuación día Pasturas homogeneas', 'Atenuación día Suelos desprovistos de vegetación (natural)',
                      'Atenuación día Urbano', 'Atenuación día Usos extractivos',
                      'Atenuación día Vegetación secundaria', 'Atenuación día Áreas degradadas',                      
                      'Atenuación noche Agricola', 'Atenuación noche Bosque',                   
                      'Atenuación noche Herbazales', 'Atenuación noche Humedales',
                      'Atenuación noche Pasturas homogeneas', 'Atenuación noche Suelos desprovistos de vegetación (natural)',
                      'Atenuación noche Urbano', 'Atenuación noche Usos extractivos',
                      'Atenuación noche Vegetación secundaria', 'Atenuación noche Áreas degradadas'])

name_mv_NoiseAte = np.array(['Atenuación regional día', 'Atenuación regional noche'])
                    
data_sound = pd.read_excel (parametersPath, sheet_name = 'Sound_pressure')
dav = pd.DataFrame(data_sound, columns= ['Umbral día (db)',	'Umbral noche (db)',
                                         'Atenuación (db)',	'Promedio día (db)',
                                         'Promedio noche (db)'])
dav = dav.to_numpy()
davm = np.nanmean(dav, axis=0)
a3 = dav[:,3]
a4 = dav[:,4]
a3[np.isnan(a3)] = davm[3]
a4[np.isnan(a4)] = davm[4]
dav[:,3] = a3
dav[:,4] = a4

NoiseAttenuationMatriz = np.transpose([[None for name_NoiseAte in range(ntime)] for name_NoiseAte in range(len(name_NoiseAte))])
NoiseAttenuationVector_mv = np.transpose([[None for name_NoiseAte in range(ntime)] for name_NoiseAte in range(2)])

for i in range(ntime):
    NoiseAttenuationMatriz[i,0] = -((dav[0,3] - dav[0,0]) / dav[0,3]) + abs((((dav[0,3] - dav[0,2] * (sum(ACob[i,0:2]) / sum(ACob[i,:])) ** (1/5)) - dav[0,0]) / (dav[0,3] - dav[0,2] * (sum(ACob[i,0:2]) / sum(ACob[i,:])) ** (1/5)))) # agricola dia
    NoiseAttenuationMatriz[i,10] = -((dav[0,4] - dav[0,1]) / dav[0,4]) + abs((((dav[0,4] - dav[0,2] * (sum(ACob[i,0:2]) / sum(ACob[i,:])) ** (1/5)) - dav[0,1]) / (dav[0,4] - dav[0,2] * (sum(ACob[i,0:2]) / sum(ACob[i,:])) ** (1/5)))) # agricola noche
    
    NoiseAttenuationMatriz[i,1:10] = -((dav[1:10,3] - dav[1:10,0]) / dav[1:10,3]) + abs((((dav[1:10,3] - dav[1:10,2] * (sum(ACob[i,0:2]) / sum(ACob[i,:])) ** (1/5)) - dav[1:10,0]) / (dav[1:10,3] - dav[1:10,2] * (ACob[i,2:11] / sum(ACob[i,:])) ** (1/5)))) # agricola dia
    NoiseAttenuationMatriz[i,11:20] = -((dav[1:10,4] - dav[1:10,1]) / dav[1:10,4]) + abs((((dav[1:10,4] - dav[1:10,2] * (sum(ACob[i,0:2]) / sum(ACob[i,:])) ** (1/5)) - dav[1:10,1]) / (dav[1:10,4] - dav[1:10,2] * (ACob[i,2:11] / sum(ACob[i,:])) ** (1/5)))) # agricola noche
    NoiseAttenuationVector_mv[i,0] = np.nanmean(NoiseAttenuationMatriz[i,0:10])
    NoiseAttenuationVector_mv[i,1] = np.nanmean(NoiseAttenuationMatriz[i,10:20])
   
# 5. Potential habitat availability
HumHa = 0.3
BO = Ys[:, 2] # forest
ConectBO = (2/3) ** Ys[:, 12] # Conectivity
for i in range(ntime):
    if ConectBO[i] <= 1:
        ConectBO[i] = ConectBO[i]
    else:
        ConectBO[i] = 1
    
FunDiv = [None for ii in range(ntime)]
S_ES = [None for ii in range(ntime)]
dfd = pd.read_excel (parametersPath, sheet_name='Functional_diversity')
arrfd = dfd.to_numpy()
dfd_names_col = dfd.columns.values
dfd_names_col = np.delete(dfd_names_col, 0, 0)
dfd_names_row = arrfd[:, 0]

for i in range(ntime):
    HabitatESi, PersistenceESi, ExistenceESi, species_names, n_species = Habitat.habitat_area(dConect, BO[i], BO[0], ConectBO[i], mcf[i], mcb[i], workspace)
    if i==0:
        HabES_i = HabitatESi
        IperES_i = PersistenceESi
        ExistenceEs_i = ExistenceESi
    else:
        HabES_i = np.vstack([HabES_i, HabitatESi])
        IperES_i = np.vstack([IperES_i, PersistenceESi])
        ExistenceEs_i = np.vstack([ExistenceEs_i, ExistenceESi])
        
    S_ES[i] = np.count_nonzero(ExistenceEs_i[i, :] == 1)
    
fd_matriz = arrfd[0:n_species,1:len(dfd_names_col)+1]
max_FUN = sum(fd_matriz)
num_ESP = len(fd_matriz[:,0])
fd_num = [[None for jj in range(len(max_FUN))] for kk in range(ntime)]
fd_per = [[None for jj in range(len(max_FUN))] for kk in range(ntime)]
esp_all_mper = [None for kk in range(ntime)]
fd_all_mper = [None for kk in range(ntime)]

for i in range(int(ntime)):
    posi = np.where(IperES_i[i, :] == 0)
    posi2 = np.where(max_FUN != 0)[0]
    fd_matriz[posi, :] = 0
    for j in range(len(posi2)):
        fd_num[i][posi2[j]] = sum(fd_matriz[:,posi2[j]])
        
    sum_fd_all_mper = 0   
    for j in range(len(fd_matriz[0,:])):
        id_fun = np.where(fd_matriz[:, j] * IperES_i[i,:] != 0)
        if max_FUN[j] != 0:
            fd_per[i][j] = np.sum(IperES_i[i, id_fun]) / max_FUN[j]
            sum_fd_all_mper += fd_per[i][j]
            
    nonzeroind = np.nonzero(fd_num[i][:])[0]
    FunDiv[i] = len(nonzeroind)
    esp_all_mper[i]= np.sum(IperES_i[i, :]) / num_ESP
    fd_all_mper[i]= sum_fd_all_mper / len(posi2)
    
name_S = np.array(['Riqueza de especies'])
name_FD = np.array(['Diversidad de funciones ecológicas'])
name_all_mper_Esp = np.array(['Persistencia promedio de todas las especies'])
name_all_mper_fun = np.array(['Persistencia promedio de todas las funciones'])


# 6. Species per Function
name_EspixFun = {}
name_PperxFun = {}
for i in range(len(dfd_names_col)):
    name_EspixFun[i] = "Número de especies - " + dfd_names_col[i]
    name_PperxFun[i] = "Persistencia promedio de - " + dfd_names_col[i]
    
data__EspixFun = np.array(list(name_EspixFun.items()))
name_EspixFun = data__EspixFun[:, 1]
data_PperxFun = np.array(list(name_PperxFun.items()))
name_PperxFun = data_PperxFun[:, 1]

name_PHaA = {}
name_PperES = {}
name_Existence = {}
for i in range(n_species):
    name_PHaA[i] = "Hábitat - " + species_names[i]
    name_PperES[i] = "Persistencia - " + species_names[i]
    name_Existence[i] = "Existencia - " + species_names[i]
data_PHaA = np.array(list(name_PHaA.items()))
name_PHaA = data_PHaA[:, 1]
data_PperES = np.array(list(name_PperES.items()))
name_PperES = data_PperES[:, 1]
data_Existence = np.array(list(name_Existence.items()))
name_Existence = data_Existence[:, 1]

# 7. Health indicator
HealthIndex = np.zeros(ntime)
InProvAliCobi = np.zeros(ntime)
DivSisAlimLocal = np.zeros(ntime)
Con_Acces = np.zeros(ntime)
name_Health = np.array(['Indice de salud'])
name_DivSisAlimLocal = np.array(['Diversidad del sistema alimentario local'])
name_Con_Acces = np.array(['Indice de condiciones de acceso'])

peso_Cobi = np.array([50, 30, 35, 40, 50, 25, 5, 15, 0, 40, 10])
# print(sum(peso_Cobi))

for i in range(int(ntime)):
    InProvAliCobi[i] = sum((peso_Cobi * Ys[i, 0:11]) ) / (max(peso_Cobi) * sum(Ys[i, 0:11]))
    
    HealthIndex[i], DivSisAlimLocal[i], Con_Acces[i] = Health_auxiliary.health_index(time[0], time[i], time, dhealth, fd_all_mper[i], len(dfd_names_col)-1, ICAmv_modificada[i],
                                                   np.mean(NoiseAttenuationVector_mv[i,:]),  ICAairmv[i], InProvAliCobi[i])


# 8. Diversity of productive activities
tOACobj = dp[12:16,1]
posCobj = [0, 1, 5, 8]
VacOAci = dp[16:30,1]
pPoEcAc = dp[30,1]
PersFortHabEmpren_0 = (x_0[16])
PersFortDivInclu_0 = (x_0[17])

PoETEA = np.zeros(ntime)
PoOcu = np.zeros(ntime)
VacOCobj = np.zeros(ntime)
VacO = np.zeros(ntime)
IDivAPro = np.zeros(ntime)
AporteDivEmpren = np.zeros(ntime)
AporteDivInclus = np.zeros(ntime)

for i in range(int(ntime)):
    VacOCobj = (tOACobj * Ys[i, posCobj])
    VacO[i] = (sum(VacOCobj) + sum(VacOAci))
    PoETEA[i] = (pPoEcAc * Ys[i, 14])
    PoOcu[i] = (sum(VacOCobj) + sum(VacOAci) - PoETEA[i])
    
    if  Ys[i, 16] < PersFortHabEmpren_0:
        AporteDivEmpren[i] = (Ys[i, 16]) / PersFortHabEmpren_0
    else:
        AporteDivEmpren[i] = 1
        
    if  Ys[i, 17] < PersFortDivInclu_0:
        AporteDivInclus[i] = (Ys[i, 17]) / PersFortDivInclu_0
    else:
        AporteDivInclus[i] = 1
   
    IDivAPro[i] = (((AporteDivEmpren[i] + AporteDivInclus[i]) / 2) 
                   * (1 - (sum(VacOCobj * (VacOCobj - 1 )) + sum(VacOAci * (VacOAci - 1))) 
                   / ((sum(VacOCobj) + sum(VacOAci)) * ((sum(VacOCobj) + sum(VacOAci)) - 1)))) ** (1 - DivSisAlimLocal[i])

    if VacO[i] - PoETEA[i] >= 0:
        PoOcu[i] = 1
    else:
        PoOcu[i] = VacO[i] - PoETEA[i]
name_IDivAPro = np.array(['Indice de diversidad de actividades productivas'])
name_OandE = np.array(['Personas que están ocupadas'])

# 9. Standardized conectivity
ConectBOn = (2/3) ** (Ys[:,12])
name_ConectBOn = np.array(['Conectividad normalizada'])
# 10. Total population
Ys[:,13] = (Ys[:,13])
Ys[:,14] = (Ys[:,14])
Ys[:,15] = (Ys[:,15])
Ys[:,16] = (Ys[:,16])
Ys[:,17] = (Ys[:,17])
PAE = (Ys[:,13]) + (Ys[:,14]) + (Ys[:,15])
name_PAE = np.array(['Población total'])
# 11. Water consumption
ConsHDomes_con = dw[7,1] * PAE *(1-dw[15,1]) * (1-(mca ** 3) / 3)
name_ConsHDomes_con = np.array(['Consumo de agua doméstico con cuidado del agua'])
ConsHDomes_sin = dw[7,1] * PAE *(1-dw[15,1])
name_ConsHDomes_sin = np.array(['Consumo de agua doméstico sin cuidado del agua'])

Consumption = (ConsHDomes_con +
               dw[0,1] * (1 - dw[8,1]) +
               dw[1,1] * (1 - dw[9,1]) +
               dw[2,1] * (1 - dw[10,1]) +
               dw[3,1] * (1 - dw[11,1]) +
               dw[4,1] * (1 - dw[12,1]) +
               dw[5,1] * (1 - dw[13,1]) +
               dw[6,1] * (1 - dw[14,1]))

OHTD = dw[33,1]
Qm_con = OHTD - Consumption
name_Qm_con = np.array(['Caudal medio de salida con cuidado del agua'])
Qm_sin = OHTD - (Consumption - ConsHDomes_con + ConsHDomes_sin)
name_Qm_sin = np.array(['Caudal medio de salida sin cuidado del agua'])

IUA = np.zeros(ntime)
for i in range(int(ntime)):
    IUA[i] = WaterUseIndex.water_use_index(Ys[i,:], dw)

# 12. Productive activities indices
name_VacOcup = np.array(['Vacantes de ocupación'])
name_AporEmpren = np.array(['Aporte a la diversidad de actividades productivas desde el fortalecemiento de emprendimiento'])
name_AporDiver = np.array(['Aporte a la diversidad de actividades productivas desde el fortalecimiento en diversidad e inclusión'])
name_PoETEA = np.array(['Población economicamente activa'])
# 13. Social tissue indices
name_EnfInte = np.array(['Enfoque integrado'])
name_ColAct = np.array(['Colaboración entre actores'])
name_IntCom = np.array(['Interés Común'])
name_TransCSA_ColEA = np.array(['Transformación de conflictos por colaboración entre actores'])
name_TransCSA_CuiA = np.array(['Transformación de conflictos por cuidado del agua'])
name_ProgIyP = np.array(['Programas de información y participación comunitaria'])
name_sum_pyf = np.array(['Diversidad de programas y prácticas de cuidado'])

name_mca = np.array(['Indicador de cuidado del agua'])
name_mcf = np.array(['Indicador de cuidado de la fauna'])
name_mcb = np.array(['Indicador de cuidado del bosque'])
# 14. Health indices
name_InProvAliCobi = np.array(['Indice de provisión de alimento por coberturas'])

# Exporting time series as a .csv file
names = np.concatenate((name_year, 
                        name_cover, 
                        name_water, 
                        name_ConectBO, 
                        name_population, 
                        name_SF_CSA,
#--------------------------------------------------------------------   
                        name_AT,
                        name_NA,
                        name_Land_Div,
                        name_PAE,
                        name_ConectBOn,
                        name_ConsHDomes_con,
                        name_ConsHDomes_sin,
                        name_Qm_con,
                        name_Qm_sin,
                        # name_WQ, # si
                        name_mv_original,
                        name_mv_modificada,
                        # name_AirQ, # si
                        name_mv_AirQ,
                        # name_NoiseAte, # si
                        name_mv_NoiseAte, 
                        # name_PHaA,  # si
                        # name_PperES, # si
                        # name_Existence, # si
                        name_S,
                        name_FD,
                        name_EspixFun,
                        name_PperxFun,
                        name_all_mper_Esp,
                        name_all_mper_fun,
                        name_Health,
                        name_Con_Acces,
                        name_DivSisAlimLocal, 
                        name_InProvAliCobi,
                        name_IDivAPro, 
                        name_VacOcup,
                        # name_AporEmpren, # si
                        # name_AporDiver, # si
                        name_OandE,
                        name_PoETEA,
                        name_EnfInte,
                        name_ColAct,
                        name_IntCom,
                        name_TransCSA_ColEA,
                        name_TransCSA_CuiA,
                        name_ProgIyP,
                        name_sum_pyf,
                        name_mca,
                        name_mcf,
                        name_mcb
                        ))
output = np.c_[time, 
               Ys[:,0],
               Ys[:,1],
               Ys[:,2],
               Ys[:,3],
               Ys[:,4],
               Ys[:,5],
               Ys[:,6],
               Ys[:,7],
               Ys[:,8],
               Ys[:,9],
               Ys[:,10],
               Ys[:,11],
               Ys[:,12],
               np.trunc(Ys[:,13]),
               np.trunc(Ys[:,14]),
               np.trunc(Ys[:,15]),
               np.trunc(Ys[:,16]),
               np.trunc(Ys[:,17]),
               Ys[:,18],
               Ys[:,19],
#----------------------------------------------------------------------------------------
               Yt,
               NA,
               Yt_log,
               np.trunc(PAE),
               ConectBOn,
               ConsHDomes_con,
               ConsHDomes_sin,
               Qm_con,
               Qm_sin,
            #    ICAiv_original, # si
               ICAmv_original,
               ICAmv_modificada,
            #    ICAairiv, # si
               ICAairmv, 
            #    NoiseAttenuationMatriz, # si
               NoiseAttenuationVector_mv,
            #    HabES_i,  # si
            #    IperES_i,  # si
            #    ExistenceEs_i, # si
               S_ES, 
               FunDiv, 
               fd_num,
               fd_per,
               esp_all_mper,
               fd_all_mper,
               HealthIndex, 
               Con_Acces,
               DivSisAlimLocal, 
               InProvAliCobi,
               IDivAPro, 
               np.trunc(VacO),
            #    AporteDivEmpren, # si
            #    AporteDivInclus, # si
               np.trunc(PoOcu),
               np.trunc(PoETEA),
               EnfIntefr_Cobi,
               ColEA,
               IntCom,
               TransCSA_ColEA,
               TransCSA_CuiA,
               ProgIyP,
               sum_pyg,
               mca,
               mcf,
               mcb
               ]
model_time_series = pd.DataFrame(output, columns=names).apply(pd.to_numeric)

names_DA = np.array([name_cover[-1]])
names_HeterAg = np.array([name_cover[0]])
name_SF = np.array([name_SF_CSA[0]])
name_SAConfli = np.array([name_SF_CSA[1]])
name_p_fort_empren = np.array([name_population[3]])
name_p_fort_inclu = np.array([name_population[4]])
name_mv_NoiseAte_d = np.array([name_mv_NoiseAte[0]])
name_water = np.array([name_water[0]])
name_PperxFun_nectar = np.array([name_PperxFun[2]])
name_PperxFun_frugi = np.array([name_PperxFun[0]])
name_PperxFun_semilla = np.array([name_PperxFun[4]])

output_indicator = resilience_indicators.slope_time_series(model_time_series,
                                                     name_year,
                                                     #------------1----------------
                                                     name_Land_Div,
                                                     names_DA,
                                                     name_NA,
                                                     names_HeterAg,
                                                     name_all_mper_Esp,
                                                     name_all_mper_fun,
                                                     name_IDivAPro,
                                                     name_DivSisAlimLocal,
                                                     #-------------2----------------
                                                     name_PperxFun_nectar,
                                                     name_PperxFun_frugi,
                                                     name_PperxFun_semilla,
                                                     name_ConectBOn,
                                                     name_water,
                                                     name_SF,
                                                     name_Con_Acces,
                                                     #------------3----------------
                                                     name_p_fort_empren,
                                                     name_p_fort_inclu,
                                                     #------------4----------------
                                                     name_SAConfli,
                                                     #------------5---------------
                                                     name_sum_pyf,
                                                     name_IntCom,
                                                     name_Health,
                                                     #------------------------------------
                                                     Yt[1],
                                                     name_PAE,
                                                     posi2)

output_final = pd.concat([model_time_series, output_indicator], axis = 1)

if decimalSeparator=="punto":
        separator = '.'
else:
    separator = ','

output_final.to_csv(f'./outputs/{result_name}', sep=';', decimal=separator, encoding='utf-8-sig')


# # OPTIONAL - PLOT TIME SERIES
# k = 1
# plt.figure(k)
# for i in range(nx0_cover):
#     plt.plot(time, Ys[:, i], label = name_cover[i])
#     plt.scatter(time, Ys[:, i])
# plt.plot(time, Yt, label='Área total')
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# plt.figure(k + 1)
# plt.plot(time, Ys[:,11], label = name_water[0])
# plt.scatter(time, Ys[:,11])
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# fig, axes = plt.subplots(2)
# axes[0].plot(time, Ys[:,12], label = name_ConectBO[0])
# axes[0].scatter(time, Ys[:,12])
# axes[0].legend(loc='best')
# axes[1].plot(time, ConectBOn, label = name_ConectBOn[0])
# axes[1].scatter(time, ConectBOn)
# axes[1].legend(loc='best')
# plt.xlabel('tiempo')
# plt.show()

# k = k + 1
# plt.figure(k)
# for i in range(len(name_population)):
#     plt.plot(time, Ys[:,13+i], label = name_population[i])
#     plt.scatter(time, Ys[:,13+i])
# plt.plot(time, np.trunc(PoETEA), label = name_PoETEA[0])
# plt.scatter(time, np.trunc(PoETEA))
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# k = k + 1
# plt.figure(k)
# for i in range(len(name_SF_CSA)):
#     plt.plot(time, Ys[:,18+i], label = name_SF_CSA[i])
#     plt.scatter(time, Ys[:,18+i])
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# k = k + 1
# plt.figure(k)
# plt.plot(time, ConsHDomes_con, label = name_ConsHDomes_con[0])
# plt.scatter(time, ConsHDomes_con)
# plt.plot(time, ConsHDomes_sin, label = name_ConsHDomes_sin[0])
# plt.scatter(time, ConsHDomes_sin)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# k = k + 1
# plt.figure(k)
# for i in range(n_species):
#     plt.plot(time, HabES_i[:, i], label = name_PHaA[i])
#     plt.scatter(time, HabES_i[:, i])
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# k = k + 1
# plt.figure(k)
# for i in range(n_species):
#     plt.plot(time, IperES_i[:, i], label = name_PperES[i])
#     plt.scatter(time, IperES_i[:, i])
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# k = k + 1
# plt.figure(k)
# for i in range(n_species):
#     plt.plot(time, ExistenceEs_i[:, i], label = name_Existence[i])
#     plt.scatter(time, ExistenceEs_i[:, i])
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# k = k + 1
# plt.figure(k)
# plt.plot(time, S_ES, label = name_S[0])
# plt.scatter(time, S_ES)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# k = k + 1
# plt.figure(k)
# plt.plot(time, FunDiv, label = name_FD[0])
# plt.scatter(time, FunDiv)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# k = k + 1
# plt.figure(k)
# for i in range(len(name_EspixFun)):
#     coli = [tple[i] for tple in fd_num]
#     plt.plot(time, coli, label = name_EspixFun[i])
#     plt.scatter(time, coli)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# k = k + 1
# plt.figure(k)
# for i in range(len(name_PperxFun)):
#     coli = [tple[i] for tple in fd_per]
#     plt.plot(time, coli, label = name_PperxFun[i])
#     plt.scatter(time, coli)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# k = k + 1
# plt.figure(k)
# plt.plot(time, HealthIndex, label = name_Health[0])
# plt.scatter(time, HealthIndex)
# plt.plot(time, Con_Acces, label = name_Con_Acces[0])
# plt.scatter(time, Con_Acces)
# plt.plot(time, DivSisAlimLocal, label = name_DivSisAlimLocal[0])
# plt.scatter(time, DivSisAlimLocal)
# plt.plot(time, InProvAliCobi, label = name_InProvAliCobi[0])
# plt.scatter(time, InProvAliCobi)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# k = k + 1
# plt.figure(k)
# plt.plot(time, IDivAPro, label = name_IDivAPro[0])
# plt.scatter(time, IDivAPro)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# k = k + 1
# plt.figure(k)
# plt.plot(time, np.trunc(VacO), label = name_VacOcup[0])
# plt.scatter(time, np.trunc(VacO))
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# k = k + 1
# plt.figure(k)
# fig, axes = plt.subplots(3)
# axes[0].plot(time, EnfIntefr_Cobi, label = name_EnfInte[0])
# axes[0].scatter(time, EnfIntefr_Cobi)
# axes[0].legend(loc='best')
# axes[1].plot(time, ColEA, label = name_ColAct[0])
# axes[1].scatter(time, ColEA)
# axes[1].legend(loc='best')
# axes[2].plot(time, IntCom, label = name_IntCom[0])
# axes[2].scatter(time, IntCom)
# axes[2].legend(loc='best')
# plt.xlabel('tiempo')
# plt.show()

# k = k + 1
# plt.figure(k)
# plt.plot(time, Qm_con, label = name_Qm_con[0])
# plt.scatter(time, Qm_con)
# plt.plot(time, Qm_sin, label = name_Qm_sin[0])
# plt.scatter(time, Qm_sin)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()
