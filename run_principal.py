from sqlalchemy import column
from condiciones_iniciales import initial_cond_cover
from condiciones_iniciales import initial_cond_water
from condiciones_iniciales import initial_cond_population
from condiciones_iniciales import initial_cond_social_fabric
from ModuloAgua import WaterQuality
from ModuloVariablesAbioticas import AbioticVariables
from ModuloDisponibilidadHabitat import Habitat
from ModuloTejidoSocial import SF_auxiliary
from ModuloSalud import Health_auxiliary
# from ModuloDiversidadActividadesProductivas import Population
import fun_ode as ode
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

# initial conditions for covers (Cobi)
data0_cover = sorted(initial_cond_cover.initial_cover())
x0_cover = [row[1] for row in data0_cover]
name_cover = [row[0] for row in data0_cover]
nc = len(x0_cover)
# conda install openpyxl if necessary
df = pd.read_excel (r'./condiciones_iniciales/parameters.xlsx', sheet_name='transformation_rates')
arr = df.to_numpy()
cover_rates = arr[0:nc,1:nc+1]

# initial volume of water stored (Vaa) + water available for consumption (Adc)
data0_water = initial_cond_water.initial_water()
x0_water =  [row[1] for row in data0_water]
name_water = [row[0] for row in data0_water]
data_water = pd.read_excel (r'./condiciones_iniciales/parameters.xlsx', sheet_name='water_parameters')
dw = pd.DataFrame(data_water, columns= ['Nombre', 'Valor'])
dw = dw.to_numpy()

# initial population in the study area
data0_population = initial_cond_population.initial_population()
x0_population =  [row[1] for row in data0_population]
name_population = [row[0] for row in data0_population]
data_population = pd.read_excel (r'./condiciones_iniciales/parameters.xlsx', sheet_name='Diversity_of_activities')
dp = pd.DataFrame(data_population, columns= ['Nombre', 'Valor'])
dp = dp.to_numpy()

# initial social fabric + socioenvironmental conflicts
data0_SF_CSA = initial_cond_social_fabric.initial_social_fabric()
x0_SF_CSA =  [row[1] for row in data0_SF_CSA]
name_SF_CSA = [row[0] for row in data0_SF_CSA]
data_SF_CSA = pd.read_excel (r'./condiciones_iniciales/parameters.xlsx', sheet_name='Social_fabric')
dsf = pd.DataFrame(data_SF_CSA, columns= ['Nombre', 'Valor'])
dsf = dsf.to_numpy()

# INTEGRATOR CONFIGURATION
tmin = 2020
tmax = 2040
time = np.arange(tmin, tmax, 1)
name_year = np.array(['Año'])
ntime = len(time)

x0_cover = np.array(x0_cover)
nx0_cover = len(x0_cover)
cover_rates = np.array(cover_rates)
cover_rates_t = cover_rates.transpose()

x0_water = np.array(x0_water)
nx0_water = len(x0_water)

x0_population = np.array(x0_population)
nx0_population = len(x0_population)

x0_SF_CSA = np.array(x0_SF_CSA)
nx0_SF_CSA = len(x0_SF_CSA)

# Integration by RK45
x_0 = np.concatenate((x0_cover, x0_water, x0_population, x0_SF_CSA), axis=0) # [cover, water]
Ys = odeint(ode.differential_equations, x_0, time, args=(cover_rates, cover_rates_t, nx0_cover, dw, dp, dsf)) #+  random.uniform(-5000, 5000)
Yt = np.sum(Ys[:, 0:nx0_cover],axis=1) # axis=1 --> add rows, axis=0 --> add columns

# SPECIAL INDICATORS

# Water quality
WaterQualityIndex = np.zeros(ntime)
name_WQ = np.array(['Indice de calidad del agua'])
for i in range(ntime):
    ColEA, EnfIntefr_Cobi, IntCom, TransCSA_ColEA, TransCSA_CuiA, mca, mcf = SF_auxiliary.SF_auxiliary_variables(Ys[i,:], dsf)
    WaterQualityIndex[i] = WaterQuality.Wquality(Ys[i,0:11], dw, mca)

## Abiotic variables
data_abiotic = pd.read_excel (r'./condiciones_iniciales/parameters.xlsx', sheet_name='Abiotic_Variables')
dav = pd.DataFrame(data_abiotic, columns= ['Nombre', 'Valor'])
dav = dav.to_numpy()
pos_AN = [2, 3, 4, 6, 9] # position of matriz og natural areas
pos_transA = [0, 1, 5, 7, 8, 10] # position of matriz of transdormed areas
AN = Ys[:, pos_AN] # natural areas position
AnoN = Ys[:, pos_transA] # Transformed areas position
LongVias = dav[24, 1]
# 1. Sound pressure
SoundPressureQualityIndex = np.zeros(ntime)
name_SPQ = np.array(['Indice de presión sonora'])
for i in range(ntime):
    SoundPressureQualityIndex[i] = AbioticVariables.SoundPressurequality(AN[i,:], AnoN[i,:], dav, pos_AN, pos_transA, LongVias)
# 2. Landscape quality
LandscapeQualityIndex = np.zeros(ntime)
name_LQ = np.array(['Indice de calidad paisajistica'])
for i in range(ntime):
    LandscapeQualityIndex[i] = AbioticVariables.Ladscapequality(AN[i,:], AnoN[i,:])
# 3. Air quality
AirQualityIndex = np.zeros(ntime)
name_AQ = np.array(['Indice de calidad de aire'])
for i in range(ntime):
   AirQualityIndex[i] = AbioticVariables.Airquality(AN[i,:], AnoN[i,:], dav, pos_AN, pos_transA, LongVias)
# 4. Potential habitat availability
data_habitat = pd.read_excel (r'./condiciones_iniciales/parameters.xlsx', sheet_name='Habitat_Availability')
dh = pd.DataFrame(data_habitat, columns= ['Nombre', 'Valor'])
dh = dh.to_numpy()
HumHa = dh[1, 1]
BO = Ys[:, 2] # forest 
FunDiv = np.zeros(int(ntime))
S = np.zeros(int(ntime)) # species richness
dfd = pd.read_excel (r'./condiciones_iniciales/parameters.xlsx', sheet_name='Functional_diversity')
arrfd = dfd.to_numpy()
dfd_names_col = dfd.columns.values
dfd_names_row = arrfd[:, 0]
for i in range(ntime):
    HabitatESi, PersistenceESi, ExistenceESi, species_names, n_species = Habitat.habitat_area(dh, BO[i], BO[0])
    if i==0:
        HabES_i = HabitatESi
        PperES_i = PersistenceESi
        ExistenceEs_i = ExistenceESi
    else:
        HabES_i = np.vstack([HabES_i, HabitatESi])
        PperES_i = np.vstack([PperES_i, PersistenceESi])
        ExistenceEs_i = np.vstack([ExistenceEs_i, ExistenceESi])
    if BO[i] <= HumHa * BO[0]:
        S[i] = 0
    else:
        S[i] = np.count_nonzero(ExistenceEs_i[i, :] == 1)
fd_matriz = arrfd[0:n_species,1:n_species+1]
ones_0 = sum(fd_matriz)
ones_i = np.zeros((int(ntime), len(ones_0)))
for i in range(int(ntime)):
    posi = np.where(PperES_i[i, :] == 0)
    fd_matriz[posi, :] = 0
    ones_i[i, :] = sum(fd_matriz)
    nonzeroind = np.nonzero( ones_i[i, :])[0]
    if BO[i] <= HumHa * BO[0]:
       FunDiv[i] = 0
    else:
        FunDiv[i] = len(fd_matriz[0, :]) - (len(fd_matriz[0, :]) - len(nonzeroind))
name_S = np.array(['Riqueza de especies'])
name_FD = np.array(['Diversidad Funcional'])
name_PHaA = {}
name_PperES = {}
name_Existence = {}
for i in range(n_species):
    name_PHaA[i] = "Hábitat - " + species_names[i]
    name_PperES[i] = "probabilidad de persistencia - " + species_names[i]
    name_Existence[i] = "Existencia - " + species_names[i]
data = np.array(list(name_PHaA.items()))
name_PHaA = data[:, 1]
data = np.array(list(name_PperES.items()))
name_PperES = data[:, 1]
data = np.array(list(name_Existence.items()))
name_Existence = data[:, 1]
# 5. Diversity of productive activities + occupation and employment
tEmpMigra = dp[25, 1]
tEmpPLocal = dp[26, 1]
pMigEL = dp[27, 1]
pPLocEL = dp[28, 1]
DivSisCon = dp[29, 1]
tOAE_usos_i = dp[0:11, 1]
tOAE_nousos_i = dp[11:21, 1]
PMigEL = np.zeros(ntime)
PLocEL = np.zeros(ntime)
TOcup = np.zeros(ntime)
IDivAPro = np.zeros(ntime)
OOandE = np.zeros(ntime)
OandE = np.zeros(ntime)
for i in range(int(ntime)):
    PMigEL[i] = pMigEL * Ys[i, 13]
    PLocEL[i] = pPLocEL * Ys[i, 13]
    TOcup[i] = PMigEL[i] + PLocEL[i]
    nei_usos = tOAE_usos_i * Ys[i, 0:11]
    Nei_usos = sum(tOAE_usos_i * Ys[i, 0:11])
    IDivAPro[i] = DivSisCon * (sum(nei_usos * (nei_usos - 1 )) + sum(tOAE_nousos_i * (tOAE_nousos_i - 1))) / ((Nei_usos + sum(tOAE_nousos_i)) * ((Nei_usos + sum(tOAE_nousos_i)) - 1))
    OOandE[i] = Nei_usos + sum(tOAE_nousos_i)
    if TOcup[i] <= OOandE[i]:
        OandE[i] = OOandE[i] - TOcup[i]
    else:
        OandE[i] = 0
name_IDivAPro = np.array(['Indice de diversidad de actividades productivas'])
name_OandE = np.array(['Ocupación y empleo'])

# 6. Healt indicator
HealthIndex = np.zeros(ntime)
name_Health = np.array(['Indice de salud'])
data_health = pd.read_excel (r'./condiciones_iniciales/parameters.xlsx', sheet_name='Health')
dhealth = pd.DataFrame(data_health, columns= ['Nombre', 'Valor'])
dhealth = dhealth.to_numpy()
for i in range(int(ntime)):
    HealthIndex[i] = Health_auxiliary.health_index(dhealth, LongVias, S[i], len(dfd_names_row), WaterQualityIndex[i],
                                                   SoundPressureQualityIndex[i], AirQualityIndex[i])

# Exporting time series as a .csv file
names = np.concatenate((name_year, name_cover, name_water, name_population, name_SF_CSA, name_WQ, name_SPQ, name_LQ, name_AQ,
                        name_PHaA,  name_PperES,  name_Existence, name_S, name_FD, name_IDivAPro, name_OandE))
output = np.c_[time, Ys, WaterQualityIndex, SoundPressureQualityIndex, LandscapeQualityIndex, AirQualityIndex, 
               HabES_i, PperES_i, ExistenceEs_i, S, FunDiv, IDivAPro, OandE]
model_time_series = pd.DataFrame(output, columns=names)
model_time_series.to_csv('./outputs/model_time_series.csv', float_format='%.2f')


# OPTIONAL - PLOT TIME SERIES
# plt.figure(1)
# for i in range(nx0_cover):
#     plt.plot(time, Ys[:, i], label=names[i+1])
#     plt.scatter(time, Ys[:, i])
# plt.plot(time, Yt, label='Área total')
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# plt.figure(2)
# for i in range(nx0_water):
#     plt.plot(time, Ys[:, nx0_cover + i], label=names[nx0_cover + i+1])
#     plt.scatter(time, Ys[:, nx0_cover + i])
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# plt.figure(3)
# plt.plot(time, WaterQualityIndex, label = name_WQ[0])
# plt.scatter(time, WaterQualityIndex)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# plt.figure(4)
# plt.plot(time, Ys[:,13], label = name_population[0])
# plt.scatter(time, Ys[:,13])
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# plt.figure(5)
# for i in range(nx0_water):
#     plt.plot(time, Ys[:, 14 + i], label=name_SF_CSA[i])
#     plt.scatter(time, Ys[:, 14 + i])
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# plt.figure(6)
# for i in range(n_species):
#     plt.plot(time, HabES_i[:, i], label = name_PHaA[i])
#     plt.scatter(time, HabES_i[:, i])
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# # plt.title('Hábitat')
# plt.grid()
# plt.show()

# plt.figure(7)
# for i in range(n_species):
#     plt.plot(time, PperES_i[:, i], label = name_PperES[i])
#     plt.scatter(time, PperES_i[:, i])
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# # plt.title('Probabilidad de persistencia de especies')
# plt.grid()
# plt.show()

# plt.figure(8)
# for i in range(n_species):
#     plt.plot(time, ExistenceEs_i[:, i], label = name_Existence[i])
#     plt.scatter(time, ExistenceEs_i[:, i])
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# # plt.title('Existencia de especies')
# plt.grid()
# plt.show()

# plt.figure(9)
# plt.plot(time, S, label = name_S[0])
# plt.scatter(time, S)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# plt.figure(10)
# plt.plot(time, FunDiv, label = name_FD[0])
# plt.scatter(time, FunDiv)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# plt.figure(11)
# plt.plot(time, IDivAPro, label = name_IDivAPro[0])
# plt.scatter(time, IDivAPro)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# plt.figure(12)
# plt.plot(time, OandE, label = name_OandE[0])
# plt.scatter(time, OandE)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# plt.figure(13)
# plt.plot(time, HealthIndex, label = name_Health[0])
# plt.scatter(time, HealthIndex)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()