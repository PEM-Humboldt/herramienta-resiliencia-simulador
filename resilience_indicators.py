import numpy as np
import pandas as pd

def slope_time_series(model_time_series,             name_Land_Div,
                                                     names_DA,
                                                     name_NA,
                                                     names_HeterAg,
                                                     name_all_mper_Esp,
                                                     name_FD,
                                                     name_IDivAPro,
                                                     name_DivSisAlimLocal,
                                                     name_PperxFun,
                                                     name_ConectBOn,
                                                     name_water,
                                                     name_SF,
                                                     name_Con_Acces,
                                                     name_p_fort_empren,
                                                     name_sum_pyf,
                                                     name_p_fort_inclu,
                                                     name_SAConfli,
                                                     name_IntCom,
                                                     name_mv_modificada,
                                                     name_mv_NoiseAte_d,
                                                     num_fun,
                                                     AT):
    
    normalized_variables = np.concatenate((name_Land_Div,
                                           name_NA,
                                           names_HeterAg,
                                           name_water,
                                           name_p_fort_empren,
                                           name_p_fort_inclu,
                                           name_SAConfli,
                                           name_mv_NoiseAte_d))
    delta_time = []
    arr = model_time_series.to_numpy()
    nrow = len(arr[:,0])
    ncolumn = len(arr[0,:])
    time_vector = arr[:,0]
    names_vector = names[1:ncolumn]
    time_vector = ["%.0f" % x for x in time_vector]
    time_series = arr[0:nrow,1:ncolumn+1]
    time_series_max = np.max(time_series, axis=0)
    time_series_relative = time_series / time_series_max
    time_series_relative_t1 = time_series_relative[0:nrow-1, :]
    time_series_relative_t2 = time_series_relative[1:nrow, :]
    
    for i in range(nrow-1):
        delta_time.append(time_vector[i] + "-" +time_vector[i+1])
    
    # slope between two consecutive points in relative time series
    slopes_2 = time_series_relative_t2 - time_series_relative_t1
    output = np.c_[delta_time, slopes_2]
    
    output_data = pd.DataFrame(output, columns=names)
    new_row = pd.DataFrame([], index=np.arange(1), columns=output_data.columns)
    output_data = pd.concat([new_row,output_data])
    
    # difference between the first point and all data given a step size of 1
    n_deltat = len(time_series_relative[:,0])
    time_series_relative_0 = time_series_relative[0,:]
    slopes_1 = []
    step = 1
    for i in range(0, n_deltat, step):
        tt = n_deltat - i
        time_series_relative_i = time_series_relative[i,:]
        if tt >= step:
            slopes_1.append((time_series_relative_i - time_series_relative_0))
        else:
            slopes_1.append(time_series_relative[n_deltat - 1, :] - time_series_relative_0)        
    return slopes_1

# name_PHaA[i] = "Hábitat - " + species_names[i]