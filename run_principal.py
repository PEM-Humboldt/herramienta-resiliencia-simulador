
import sys
from trace import CoverageResults
sys.path.insert(0, './condiciones_iniciales')

import initial_cond_cover as icc 
import fun_ode as ode
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random # puede eliminarse cuando se tengan los valores "reales" de las tasas de cambio de coberturas

data0_cover = sorted(icc.initial_cover())

# initial conditions for soil covers
x0_cover = [row[1] for row in data0_cover]
name_cover = [row[0] for row in data0_cover]
nc = len(x0_cover)

# conda install openpyxl
df = pd.read_excel (r'./condiciones_iniciales/parameters.xlsx', sheet_name='transformation_rates')
arr = df.to_numpy()
cover_rates = arr[0:nc,1:nc+1]

# cover_rates = [[None for x0_cober in range(nc)] for x0_cover in range(nc)]
# # generates a matrix with the values of the coverage transformation rates
# # for the case i = j, the rate is one - a cover does not transform itself
# for i in range(nc):
#     for j in range(nc):
#         if i == j:
#             cover_rates[i][j] = 0
#         else:
#             cover_rates[i][j] = random.uniform(0.005,0.01)

# INTEGRATOR CONFIGURATION

tmin = 2020
tmax = 2030
# time = [tmin, tmax]
time = np.arange(tmin, tmax, 1)

x0_cover = np.array(x0_cover)
cover_rates = np.array(cover_rates)
cover_rates_t = cover_rates.transpose()
nx0 = len(x0_cover)

# Integration by RK45
Ys = odeint(ode.differential_equations, x0_cover, time, args=(cover_rates, cover_rates_t))
Yt = np.sum(Ys,axis=1) # axis=1 --> add rows, axis=0 --> add columns

# Export time series as .csv file
cover_time_series = pd.DataFrame(Ys, columns=name_cover)
cover_time_series.to_csv('./outputs/cover_time_series.csv', float_format='%.2f')


# OPTIONAL - PLOT TIME SERIES
for i in range(nx0):
    j = i + 1
    plt.plot(time, Ys[:, i], label=name_cover[i])
    plt.scatter(time, Ys[:, i])

plt.plot(time, Yt, label='Área total')
plt.legend(loc='best')
plt.xlabel('tiempo')
plt.grid()
plt.show()