from sqlalchemy import column
from condiciones_iniciales import initial_cond_cover
from condiciones_iniciales import initial_cond_water
from condiciones_iniciales import initial_cond_population
from ModuloAgua import WaterQuality
from ModuloDisponibilidadHabitat import Habitat
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

# initial volume of water stored (Vaa) and water available for consumption (Adc)
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


# INTEGRATOR CONFIGURATION
tmin = 2020
tmax = 2030
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

mca = 0.4 # este valor se asume mientras se acopla con lo social

# Integration by RK45
x_0 = np.concatenate((x0_cover, x0_water, x0_population), axis=0) # [cover, water]
Ys = odeint(ode.differential_equations, x_0, time, args=(cover_rates, cover_rates_t, nx0_cover, dw, dp, mca)) #+  random.uniform(-5000, 5000)
Yt = np.sum(Ys[:, 0:nx0_cover],axis=1) # axis=1 --> add rows, axis=0 --> add columns

# SPECIAL INDICATORS

# Water quality
WaterQualityIndex = np.zeros(ntime)
name_WQ = np.array(['Indice de calidad del agua'])
for i in range(ntime):
    WaterQualityIndex[i] = WaterQuality.Wquality(Ys[i,0:11], dw, mca)
    
# Potential habitat availability
data_habitat = pd.read_excel (r'./condiciones_iniciales/parameters.xlsx', sheet_name='Habitat_Availability')
dh = pd.DataFrame(data_habitat, columns= ['Nombre', 'Valor'])
dh = dh.to_numpy()
n_species = int(len(dh[:,1])/2) # number of species
AN = Ys[:, [2, 3, 4, 6, 9]] # natural areas position
name_PHaA = dh[0:n_species,0]
DpohaEs_i = np.zeros((int(ntime),int(n_species)))
PdEs_i = np.zeros((int(ntime),int(n_species)))
ExistenceEs_i = np.zeros((int(ntime),int(n_species)))
DivFun = np.zeros(int(ntime))
S = np.zeros(int(ntime)) # species richness

dfd = pd.read_excel (r'./condiciones_iniciales/parameters.xlsx', sheet_name='Functional_diversity')
arrfd = dfd.to_numpy()
dfd_names_col = dfd.columns.values
dfd_names_row = arrfd[:, 0]
fd_matriz = arrfd[0:n_species,1:n_species+1]

for i in range(ntime):
    DpohaEs_i[i, :], PdEs_i[i, :], ExistenceEs_i[i, :] = Habitat.habitat_area(dh,AN[i,:], AN[0,:])
    S[i] = np.count_nonzero(ExistenceEs_i[i, :] == 1)
    posi = np.where(PdEs_i[i, :] == 1)
    fd_matriz[posi, :] = 0
    DivFun[i] = np.sum(fd_matriz)
    # print(DivFun[i])

name_S = np.array(['Riqueza de especies'])
name_DF = np.array(['Diversidad Funcional'])
# Exporting time series as a .csv file
names = np.concatenate((name_year, name_cover, name_water, name_population, name_WQ, name_PHaA, name_S, name_DF))
output = np.c_[time, Ys, WaterQualityIndex, DpohaEs_i, S, DivFun]
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
#     plt.plot(time, Ys[:, nx0_cover + i], label=names[nx0_cover + i + 1])
#     plt.scatter(time, Ys[:, nx0_cover + i])

# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# plt.figure(3)
# plt.plot(time, WaterQualityIndex, label='Indice de calidad del agua')
# plt.scatter(time, WaterQualityIndex)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# plt.figure(4)
# for i in range(n_species):
#     plt.plot(time, DpohaEs_i[:, i])
#     plt.scatter(time, DpohaEs_i[:, i])

# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.title('Distribución potencial de hábitat')
# plt.grid()
# plt.show()

# plt.figure(5)
# for i in range(n_species):
#     plt.plot(time, PdEs_i[:, i])
#     plt.scatter(time, PdEs_i[:, i])

# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.title('Probabilidad de desaparición de especies')
# plt.grid()
# plt.show()

# plt.figure(6)
# for i in range(n_species):
#     plt.plot(time, ExistenceEs_i[:, i])
#     plt.scatter(time, ExistenceEs_i[:, i])

# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.title('Existencia de especies')
# plt.grid()
# plt.show()

# plt.figure(7)
# plt.plot(time, S, label='Riqueza de especies')
# plt.scatter(time, S)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()

# plt.figure(8)
# plt.plot(time, DivFun, label='Diversidad funcional')
# plt.scatter(time, DivFun)
# plt.legend(loc='best')
# plt.xlabel('tiempo')
# plt.grid()
# plt.show()
