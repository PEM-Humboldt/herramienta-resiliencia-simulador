import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def slope_time_series(model_time_series, name_year,
                                                     name_Land_Div,
                                                     names_DA,
                                                     name_NA,
                                                     names_HeterAg,
                                                     name_all_mper_Esp,
                                                     name_all_mper_fun,
                                                     name_IDivAPro,
                                                     name_DivSisAlimLocal,
                                                     name_PperxFun_nectar,
                                                     name_PperxFun_frugi,
                                                     name_PperxFun_semilla,
                                                     name_ConectBOn,
                                                     name_water,
                                                     name_SF,
                                                     name_Con_Acces,
                                                     name_p_fort_empren,
                                                     name_p_fort_inclu,
                                                     name_SAConfli,
                                                     name_sum_pyf,
                                                     name_IntCom,
                                                     name_Health,
                                                     AT,
                                                     name_PT,
                                                     posi2):
    
    names_normalized_cover = np.concatenate((name_NA, names_HeterAg))
    normalized_covers = model_time_series.loc[:, names_normalized_cover] / AT
    
    names_normalized_maxa = np.concatenate((name_Land_Div, name_water))
    data_maxa = model_time_series.loc[:, names_normalized_maxa]
    maxa = data_maxa.max()
    normalized_maxa = data_maxa / maxa 
    
    normalized_DA = 1 - (model_time_series.loc[:, names_DA] / AT)
    
    data_SAConfli = model_time_series.loc[:, name_SAConfli]
    normalized_SAConfli = 0.5 ** (data_SAConfli)
    
    PAE = np.array(model_time_series.loc[:, name_PT] )
    normalized_p_fort_empren = model_time_series.loc[:, name_p_fort_empren] / PAE
    normalized_p_fort_inclu = model_time_series.loc[:, name_p_fort_inclu] / PAE
    
    normalized_IntCom = model_time_series.loc[:, name_IntCom] / 5
    
    names_normalized_variables = np.concatenate((name_all_mper_Esp, name_all_mper_fun, name_IDivAPro, name_DivSisAlimLocal,
                                           name_PperxFun_nectar, name_PperxFun_frugi, name_PperxFun_semilla, name_ConectBOn,
                                           name_SF, name_Con_Acces, name_sum_pyf, name_Health))
    
    normalized_variables = model_time_series.loc[:, names_normalized_variables]
    
    time = model_time_series.loc[:, name_year]
    
    all_normalized_variables = pd.concat([time, normalized_DA, normalized_covers, normalized_maxa, normalized_SAConfli,
                               normalized_p_fort_empren, normalized_p_fort_inclu, normalized_IntCom,
                               normalized_variables], axis = 1)
    
    all_names_variables = np.concatenate((name_Land_Div,names_DA, name_NA, names_HeterAg, name_all_mper_Esp,
                                                     name_all_mper_fun, name_IDivAPro, name_DivSisAlimLocal,
                                                     name_PperxFun_nectar, name_PperxFun_frugi, name_PperxFun_semilla,
                                                     name_ConectBOn, name_water, name_SF, name_Con_Acces, name_p_fort_empren,
                                                     name_p_fort_inclu, name_SAConfli, name_sum_pyf,
                                                     name_IntCom, name_Health
                                          ))
    
    indicators = [[None for x in range(len(all_names_variables))] for y in range(len(time))]
    name_variables_indicator = [None for x in range(len(all_names_variables))]
    name_variables = [None for x in range(len(all_names_variables))]
    weigths = [None for x in range(len(all_names_variables))]
    
    # principle 1
    # Diversity and redundance Indicators 
    # 1. Ladscape diversity
    name_prop_land_div = np.concatenate((name_Land_Div, names_DA, name_NA, names_HeterAg))
    data_prop_land_div = all_normalized_variables.loc[:, name_prop_land_div]
    num_var_land_div = len(name_prop_land_div)
    weight_var_proper1_princ1 = np.array([12, 13, 16 , 15]) / 180
    j = 0
    for i in range(num_var_land_div):
        y = np.array(data_prop_land_div.loc[:, name_prop_land_div[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        indicators[0][j] = b1
        weigths[j] = weight_var_proper1_princ1[i]
        name_variables_indicator[j] = "Tendencia de la variable - " + name_prop_land_div[i]
        name_variables[j] = name_prop_land_div[i]
        j = j + 1
    
    # 2. diversity and functional redundance
    name_prop_div_redun = np.concatenate((name_all_mper_Esp, name_all_mper_fun))
    data_prop_div_redun = all_normalized_variables.loc[:, name_prop_div_redun]
    num_var_div_redun = len(name_prop_div_redun)
    weight_var_proper2_princ1 = np.array([4, 5]) / 180
    for i in range(num_var_div_redun):
        y = np.array(data_prop_div_redun.loc[:, name_prop_div_redun[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        indicators[0][j] = b1
        weigths[j] = weight_var_proper2_princ1[i]
        name_variables_indicator[j] = "Tendencia de la variable - " + name_prop_div_redun[i]
        name_variables[j] = name_prop_div_redun[i]
        j = j + 1
    
    # 3. diversity of activities
    name_prop_div_AcProd = name_IDivAPro
    data_prop_div_AcProd = all_normalized_variables.loc[:, name_prop_div_AcProd]
    num_var_div_AcProd = len(name_prop_div_AcProd)
    weight_var_proper3_princ1 = np.array([18]) / 180
    for i in range(num_var_div_AcProd):
        y = np.array(data_prop_div_AcProd.loc[:, name_prop_div_AcProd[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        indicators[0][j] = b1
        weigths[j] = weight_var_proper3_princ1[i]
        name_variables_indicator[j] = "Tendencia de la variable - " + name_prop_div_AcProd[i]
        name_variables[j] = name_prop_div_AcProd[i]
        j = j + 1

    # 4. diversity of ways of life
    name_prop_div_ModVida = name_DivSisAlimLocal
    data_prop_div_ModVida = all_normalized_variables.loc[:, name_prop_div_ModVida]
    num_var_div_ModVida = len(name_prop_div_ModVida)
    weight_var_proper4_princ1 =  np.array([16]) / 180
    for i in range(num_var_div_ModVida):
        y = np.array(data_prop_div_ModVida.loc[:, name_prop_div_ModVida[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        indicators[0][j] = b1
        weigths[j] = weight_var_proper4_princ1[i]
        name_variables_indicator[j] = "Tendencia de la variable - " + name_prop_div_ModVida[i]
        name_variables[j] = name_prop_div_ModVida[i]
        j = j + 1
    len_1 = len(np.concatenate((name_prop_land_div, name_prop_div_redun, name_prop_div_AcProd, name_prop_div_ModVida)))
    
    # Conectivity
    # 1. all variables
    name_prop_conectivity = np.concatenate((name_PperxFun_nectar, name_PperxFun_frugi, name_PperxFun_semilla, name_ConectBOn, name_water, name_SF, name_Con_Acces))
    data_prop_conectivity = all_normalized_variables.loc[:, name_prop_conectivity]
    num_var_div_conectivity = len(name_prop_conectivity)
    weight_var_proper_princ2 = np.array([5, 5, 5, 6, 16, 4, 4]) / 180
    for i in range(num_var_div_conectivity):
        y = np.array(data_prop_conectivity.loc[:, name_prop_conectivity[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        if b1 == 0:
            # indicators[0][j] = y[0]
            indicators[0][j] = b1
            weigths[j] = weight_var_proper_princ2[i]
        else:
            indicators[0][j] = b1
            weigths[j] = weight_var_proper_princ2[i]
        name_variables_indicator[j] = "Tendencia de la variable - " + name_prop_conectivity[i]
        name_variables[j] = name_prop_conectivity[i]
        j = j + 1
    len_2 = len(name_prop_conectivity)
        
    # principle 3
    # Learning and experimentation
    # 1. Innovation and Experimentation
    name_prop_InnovExper = name_p_fort_empren
    data_prop_InnovExper = all_normalized_variables.loc[:, name_prop_InnovExper]
    num_var_InnovExper = len(name_prop_InnovExper)
    weight_var_proper1_princ3 = np.array([4]) / 180
    
    for i in range(num_var_InnovExper):
        y = np.array(data_prop_InnovExper.loc[:, name_prop_InnovExper[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        indicators[0][j] = b1
        weigths[j] = weight_var_proper1_princ3[i]
        name_variables_indicator[j] = "Tendencia de la variable - " + name_prop_InnovExper[i]
        name_variables[j] =  name_prop_InnovExper[i]
        j = j + 1
    
     # 2. Transmission of knowledge - training
    name_prop_transmission = name_p_fort_inclu
    data_prop_transmission = all_normalized_variables.loc[:, name_prop_transmission]
    num_var_transmission = len(name_prop_transmission)
    weight_var_proper2_princ3 = np.array([4]) / 180
    for i in range(num_var_transmission):
        y = np.array(data_prop_transmission.loc[:, name_prop_transmission[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        if b1 == 0:
            # indicators[0][j] = y[0]
            indicators[0][j] = b1
            weigths[j] = weight_var_proper2_princ3[i]
        else:
            indicators[0][j] = b1
            weigths[j] = weight_var_proper2_princ3[i]
        name_variables_indicator[j] = "Tendencia de la variable - " + name_prop_transmission[i]
        name_variables[j] = name_prop_transmission[i]
        j = j + 1
    len_3 = len(np.concatenate((name_prop_InnovExper, name_prop_transmission)))
    
    # principle 4

    # Participation for equity
    # collaboration between actors
    name_prop_Colaboration = name_SAConfli
    data_prop_Colaboration = all_normalized_variables.loc[:, name_prop_Colaboration]
    num_var_Colaboration = len(name_prop_Colaboration)
    weight_var_proper1_princ4 = np.array([6]) / 180
    for i in range(num_var_Colaboration):
        y = np.array(data_prop_Colaboration.loc[:, name_prop_Colaboration[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        indicators[0][j] = b1
        weigths[j] = weight_var_proper1_princ4[i]
        name_variables_indicator[j] = "Tendencia de la variable - " + name_prop_Colaboration[i]
        name_variables[j] = name_prop_Colaboration[i]
        j = j + 1
    len_4 = len(name_prop_Colaboration)
    
    # principle 5

    # Polycentric governance
    # all variables
    name_prop_Governance = np.concatenate((name_sum_pyf, name_IntCom, name_Health))
    data_prop_Governance = all_normalized_variables.loc[:, name_prop_Governance]
    num_var_governance = len(name_prop_Governance)
    weight_var_proper1_princ5 = np.array([4, 13, 5]) / 180
    
    for i in range(num_var_governance):
        y = np.array(data_prop_Governance.loc[:, name_prop_Governance[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        if b1 == 0:
            # indicators[0][j] = y[0]
            indicators[0][j] = b1
            weigths[j] = weight_var_proper1_princ5[i]
        else:
            indicators[0][j] = b1
            weigths[j] = weight_var_proper1_princ5[i]
        name_variables_indicator[j] = "Tendencia de la variable - " + name_prop_Governance[i]
        name_variables[j] = name_prop_Governance[i]
        j = j + 1
    len_5 = len(name_prop_Governance)
    
    data_variables = all_normalized_variables.loc[:, name_variables]
    data_variables_line = np.array(data_variables)
    name_indicator = np.array(['Indice de resiliencia'])
    resilience_indicator = [None for x in range(len(time))]
    for i in range(len(time)):
        line = np.array(data_variables_line[i][:])
        line[np.isnan(line)] = 0
        pond = weigths * line
        resilience_indicator[i] = sum(pond)
    
    # plt.plot(time, resilience_indicator, label = name_indicator)
    # plt.scatter(time, resilience_indicator)
    # plt.legend(loc='best')
    # plt.xlabel('tiempo')
    # plt.grid()
    # plt.show()
    
    resi_indicator_DF = pd.DataFrame(resilience_indicator, columns=name_indicator).apply(pd.to_numeric)
    indicators_DF = pd.DataFrame(indicators, columns=name_variables_indicator).apply(pd.to_numeric)
    
    name_indicator_slope = np.array(['Tendencia del indice de resiliencia'])
    resilience_indicator_slope = [None for x in range(len(time))]
    for i in range(len(time)):
        y = np.array(resilience_indicator)
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
    
    resilience_indicator_slope[0] = b1
    indicator_slope = pd.DataFrame(resilience_indicator_slope, columns=name_indicator_slope).apply(pd.to_numeric)
    
    normalized_variables_order = np.array(all_normalized_variables.loc[:, name_variables])
    name_normalized_variables_order = [None for x in range(len(name_variables))]
    for i in range(len(name_variables)):
        name_normalized_variables_order[i] = name_variables[i] + " (normalizada)"
# -----------------------------------------------
    arr = model_time_series.to_numpy()
    nrow = len(arr[:,0])
    time_vector = arr[:,0]
    time_vector_slopes = arr[:,0]
    time_vector = ["%.0f" % x for x in time_vector]
    
    delta_time = []
    for i in range(nrow-1):
        delta_time.append(time_vector[i] + "-" +time_vector[i+1])
        
    slopes_t2_t1 = np.array(resilience_indicator[1:nrow]) - np.array(resilience_indicator[0:nrow-1])
    name_slopes_t2_t1 = np.array(['Cambio de la pendiente en el indice de resiliencia'])
    name_slopes_t2_t1_deltat = np.array(['Delta de tiempo'])
    slopes_t2_t1_Data = [None for x in range(len(time))]
    Delta_t_Data = [None for x in range(len(time))]
    Delta_t_Data[0:nrow-1] = delta_time
    slopes_t2_t1_Data[0:nrow-1] = slopes_t2_t1
    slopes_t2_t1_DF = pd.DataFrame(slopes_t2_t1_Data, columns=name_slopes_t2_t1).apply(pd.to_numeric)
    Delta_t_DF = pd.DataFrame(np.array(Delta_t_Data), columns=name_slopes_t2_t1_deltat)
    
    name_slopes_t0_ti = np.array(['Pendiente acumulada del indicador de resiliencia'])
    slopes_t0_ti_Data = [None for x in range(len(time))]
    
    for i in range(len(time)-1):
        y = np.array(resilience_indicator[0:i+2])
        x = np.array(time_vector_slopes[0:i+2])
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        slopes_t0_ti_Data[i] = xx_mean_yy_mean / xx_mean2
        
    slopes_t0_ti_DF = pd.DataFrame(slopes_t0_ti_Data, columns=name_slopes_t0_ti).apply(pd.to_numeric)
# -----------------------------------------------
    normalized_variables_order = pd.DataFrame(normalized_variables_order, columns=name_normalized_variables_order).apply(pd.to_numeric)
    output_indicator = pd.concat([indicators_DF, normalized_variables_order, resi_indicator_DF, Delta_t_DF,slopes_t0_ti_DF, slopes_t2_t1_DF], axis = 1)
    
    return output_indicator
        
       
    
    
    
    
    