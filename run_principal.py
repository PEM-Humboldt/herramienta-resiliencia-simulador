
import sys
sys.path.insert(0, './condiciones_iniciales')

import initial_cond_cover as icc 
import fun_ode as ode
from scipy.integrate import odeint
import numpy as np
import random # puede eliminarse cuando se tengan los valores "reales" de las tasas de cambio de coberturas
import matplotlib.pyplot as plt


num_digits = 1 # define el nivel a usar en la agrupación de capas ¿debería ser menor o igual a min_level?
data0_cover = sorted(icc.initial_cover(num_digits))

# condiciones iniciales de coberturas
x0_cover = [row[1] for row in data0_cover]  
nc = len(x0_cover)

rates_cover = [[None for x0_cober in range(nc)] for x0_cover in range(nc)]
# se genera una matriz con los valores de las tasas de transformación de coberturas
# para el caso i=j, la tasa es cero - uan covertura no se transforma en si misma, o si?
for i in range(nc):
    for j in range(nc):
        if i == j:
            rates_cover[i][j] = 0
        else:
            rates_cover[i][j] = random.uniform(0.01,0.02)


# configuración del integrador

tmin = 2020
tmax = 2030
# time = [tmin, tmax]
time = np.arange(tmin, tmax, 1)

x0_cover = np.array(x0_cover)
rates_cover = np.array(rates_cover)
rates_cover_t = rates_cover.transpose()
nx0 = len(x0_cover)

# integración por RK45
Ys = odeint(ode.differential_equations, x0_cover, time, args=(rates_cover, rates_cover_t))
Yt = np.sum(Ys,axis=1) # axis=1 --> suma silas, axis=0 --> suma columnas

## Save data in array

coverageValue = {}
coverageValue1 = {}

for i in range(nx0):
    j = i + 1
    plt.plot(time, Ys[:, i], label='%s cobertura' % j)
    temp0 = '%s cobertura' % j
    temp = time + temp0
    coverageValue[temp] = Ys[:, i]
    plt.scatter(time, Ys[:, i])
    # coverageValue1[time] = Ys[:, i]

plt.plot(time, Yt, label='área total')
plt.legend(loc='best')
plt.xlabel('tiempo')
print('coverageValue: ', coverageValue)
print('coverageValue1: ', coverageValue1)
plt.grid()
plt.show()