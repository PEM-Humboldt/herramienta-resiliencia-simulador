import sys
from trace import CoverageResults
# call initial conditions for each module
from condiciones_iniciales import initial_cond_cover
from condiciones_iniciales import initial_cond_water
from ModuloAgua import WaterQuality

import fun_ode as ode
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# initial conditions for soil covers (Cobi)
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

# INTEGRATOR CONFIGURATION
tmin = 2020
tmax = 2030
time = np.arange(tmin, tmax, 1)
ntime = len(time)

x0_cover = np.array(x0_cover)
nx0_cover = len(x0_cover)
cover_rates = np.array(cover_rates)
cover_rates_t = cover_rates.transpose()

x0_water = np.array(x0_water)
nx0_water = len(x0_water)

mca = 0.4 # este valor se asume mientras se acopla con lo social

# Integration by RK45
x_0 = np.concatenate((x0_cover, x0_water), axis=0) # [cover, water]
names = np.concatenate((name_cover, name_water))
Ys = odeint(ode.differential_equations, x_0, time, args=(cover_rates, cover_rates_t, nx0_cover, dw, mca))
Yt = np.sum(Ys[:, 0:nx0_cover],axis=1) # axis=1 --> add rows, axis=0 --> add columns

# Special indicators
WaterQualityIndex = np.zeros(ntime)
for i in range(ntime):
    WaterQualityIndex[i] = WaterQuality.Wquality(Ys[i,0:11], dw, mca)

# Export time series as a .csv file
model_time_series = pd.DataFrame(Ys, columns=names)
model_time_series.to_csv('./outputs/model_time_series.csv', float_format='%.2f')


# OPTIONAL - PLOT TIME SERIES
plt.figure(1)
for i in range(nx0_cover):
    plt.plot(time, Ys[:, i], label=names[i])
    plt.scatter(time, Ys[:, i])

plt.plot(time, Yt, label='Área total')
plt.legend(loc='best')
plt.xlabel('tiempo')
plt.grid()
plt.show()

plt.figure(2)
for i in range(nx0_water):
    plt.plot(time, Ys[:, nx0_cover + i], label=names[nx0_cover + i])
    plt.scatter(time, Ys[:, nx0_cover + i])

plt.legend(loc='best')
plt.xlabel('tiempo')
plt.grid()
plt.show()

plt.figure(3)
plt.plot(time, WaterQualityIndex, label='Indice de calidad del agua')
plt.scatter(time, WaterQualityIndex)
plt.legend(loc='best')
plt.xlabel('tiempo')
plt.grid()
plt.show()