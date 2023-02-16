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
                                                     name_mv_AirQ,
                                                     name_mv_NoiseAte_d,
                                                     AT,
                                                     name_PT):
    
    names_normalized_cover = np.concatenate((name_NA, names_HeterAg))
    normalized_covers = model_time_series.loc[:, names_normalized_cover] / AT
    
    names_normalized_maxa = np.concatenate((name_Land_Div, name_water, name_mv_NoiseAte_d))
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
                                           name_PperxFun, name_ConectBOn, name_SF, name_Con_Acces, name_sum_pyf,
                                           name_mv_modificada, name_mv_AirQ))
    
    normalized_variables = model_time_series.loc[:, names_normalized_variables]
    
    time = model_time_series.loc[:, name_year]
    
    all_normalized_variables = pd.concat([time, normalized_DA, normalized_covers, normalized_maxa, normalized_SAConfli,
                               normalized_p_fort_empren, normalized_p_fort_inclu, normalized_IntCom,
                               normalized_variables], axis = 1)
    
    all_names_variables = np.concatenate((name_Land_Div,names_DA, name_NA, names_HeterAg, name_all_mper_Esp,
                                                     name_all_mper_fun, name_IDivAPro, name_DivSisAlimLocal,
                                                     name_PperxFun, name_ConectBOn, name_water,
                                                     name_SF, name_Con_Acces, name_p_fort_empren,
                                                     name_sum_pyf, name_p_fort_inclu, name_SAConfli,
                                                     name_IntCom, name_mv_modificada, name_mv_AirQ,name_mv_NoiseAte_d
                                          ))
    
    indicators = [[None for x in range(len(all_names_variables))] for y in range(len(time))]
    name_variables_indicator = [None for x in range(len(all_names_variables))]
    name_variables = [None for x in range(len(all_names_variables))]
    weigths = [None for x in range(len(all_names_variables))]
    
    num_principles = 5
    weight_principle = 1 / num_principles
    # principle 1
    weight_proper_princ1 = weight_principle / 4
    # Diversity and redundance Indicators 
    # 1. Ladscape diversity
    name_prop_land_div = np.concatenate((name_Land_Div, names_DA, name_NA, names_HeterAg))
    data_prop_land_div = all_normalized_variables.loc[:, name_prop_land_div]
    num_var_land_div = len(name_prop_land_div)
    weight_var_proper1_princ1 = weight_proper_princ1 / num_var_land_div
    j = 0
    for i in range(len(name_prop_land_div)):
        y = np.array(data_prop_land_div.loc[:, name_prop_land_div[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        indicators[0][j] = b1
        weigths[j] = weight_var_proper1_princ1
        name_variables_indicator[j] = "Pendiente de la variable - " + name_prop_land_div[i]
        name_variables[j] = name_prop_land_div[i]
        j = j + 1
    
    # 2. diversity and functional redundance
    name_prop_div_redun = np.concatenate((name_all_mper_Esp, name_all_mper_fun))
    data_prop_div_redun = all_normalized_variables.loc[:, name_prop_div_redun]
    num_var_div_redun = len(name_prop_div_redun)
    weight_var_proper2_princ1 = weight_proper_princ1 / num_var_div_redun
    for i in range(len(name_prop_div_redun)):
        y = np.array(data_prop_div_redun.loc[:, name_prop_div_redun[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        indicators[0][j] = b1
        weigths[j] = weight_var_proper2_princ1
        name_variables_indicator[j] = "Pendiente de la variable - " + name_prop_div_redun[i]
        name_variables[j] = name_prop_div_redun[i]
        j = j + 1
    
    # 3. diversity of activities
    name_prop_div_AcProd = name_IDivAPro
    data_prop_div_AcProd = all_normalized_variables.loc[:, name_prop_div_AcProd]
    num_var_div_AcProd = len(name_prop_div_AcProd)
    weight_var_proper3_princ1 = weight_proper_princ1 / num_var_div_AcProd
    for i in range(len(name_prop_div_AcProd)):
        y = np.array(data_prop_div_AcProd.loc[:, name_prop_div_AcProd[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        indicators[0][j] = b1
        weigths[j] = weight_var_proper3_princ1
        name_variables_indicator[j] = "Pendiente de la variable - " + name_prop_div_AcProd[i]
        name_variables[j] = name_prop_div_AcProd[i]
        j = j + 1

    # 4. diversity of ways of life
    name_prop_div_ModVida = name_DivSisAlimLocal
    data_prop_div_ModVida = all_normalized_variables.loc[:, name_prop_div_ModVida]
    num_var_div_ModVida = len(name_prop_div_ModVida)
    weight_var_proper4_princ1 = weight_proper_princ1 / num_var_div_ModVida
    for i in range(len(name_prop_div_ModVida)):
        y = np.array(data_prop_div_ModVida.loc[:, name_prop_div_ModVida[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        indicators[0][j] = b1
        weigths[j] = weight_var_proper4_princ1
        name_variables_indicator[j] = "Pendiente de la variable - " + name_prop_div_ModVida[i]
        name_variables[j] = name_prop_div_ModVida[i]
        j = j + 1
    len_1 = len(np.concatenate((name_prop_land_div, name_prop_div_redun, name_prop_div_AcProd, name_prop_div_ModVida)))
    
    # Conectivity
    # 1. all variables
    name_prop_conectivity = np.concatenate((name_PperxFun, name_ConectBOn, name_water, name_SF, name_Con_Acces))
    data_prop_conectivity = all_normalized_variables.loc[:, name_prop_conectivity]
    num_var_div_conectivity = len(name_prop_conectivity)
    weight_proper_princ2 = weight_principle / num_var_div_conectivity
    weight_var_proper_princ2 = weight_proper_princ2
    for i in range(len(name_prop_conectivity)):
        y = np.array(data_prop_conectivity.loc[:, name_prop_conectivity[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        if b1 == 0:
            indicators[0][j] = y[0]
            weigths[j] = weight_var_proper_princ2
        else:
            indicators[0][j] = b1
            weigths[j] = weight_var_proper_princ2
        name_variables_indicator[j] = "Pendiente de la variable - " + name_prop_conectivity[i]
        name_variables[j] = name_prop_conectivity[i]
        j = j + 1
    len_2 = len(name_prop_conectivity)
        
    # principle 3
    weight_proper_princ3 = weight_principle / 2
    # Learning and experimentation
    # 1. Innovation and Experimentation
    name_prop_InnovExper = name_p_fort_empren
    data_prop_InnovExper = all_normalized_variables.loc[:, name_prop_InnovExper]
    num_var_InnovExper = len(name_prop_InnovExper)
    weight_var_proper1_princ3 = weight_proper_princ3 / num_var_InnovExper
    
    for i in range(len(name_prop_InnovExper)):
        y = np.array(data_prop_InnovExper.loc[:, name_prop_InnovExper[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        indicators[0][j] = b1
        weigths[j] = weight_var_proper1_princ3
        name_variables_indicator[j] = "Pendiente de la variable - " + name_prop_InnovExper[i]
        name_variables[j] =  name_prop_InnovExper[i]
        j = j + 1
    
     # 2. Transmission of knowledge - training
    name_prop_transmission = np.concatenate((name_sum_pyf, name_p_fort_inclu))
    data_prop_transmission = all_normalized_variables.loc[:, name_prop_transmission]
    num_var_transmission = len(name_prop_transmission)
    weight_var_proper2_princ3 = weight_proper_princ3 / num_var_transmission
    for i in range(len(name_prop_transmission)):
        y = np.array(data_prop_transmission.loc[:, name_prop_transmission[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        if b1 == 0:
            indicators[0][j] = y[0]
            weigths[j] = weight_var_proper2_princ3
        else:
            indicators[0][j] = b1
            weigths[j] = weight_var_proper2_princ3
        name_variables_indicator[j] = "Pendiente de la variable - " + name_prop_transmission[i]
        name_variables[j] = name_prop_transmission[i]
        j = j + 1
    len_3 = len(np.concatenate((name_prop_InnovExper, name_prop_transmission)))
    
    # principle 4
    weight_proper_princ4 = weight_principle / 1
    # Participation for equity
    # collaboration between actors
    name_prop_Colaboration = name_SAConfli
    data_prop_Colaboration = all_normalized_variables.loc[:, name_prop_Colaboration]
    num_var_Colaboration = len(name_prop_Colaboration)
    weight_var_proper1_princ4 = weight_proper_princ4 / num_var_Colaboration
    for i in range(len(name_prop_Colaboration)):
        y = np.array(data_prop_Colaboration.loc[:, name_prop_Colaboration[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        indicators[0][j] = b1
        weigths[j] = weight_var_proper1_princ4
        name_variables_indicator[j] = "Pendiente de la variable - " + name_prop_Colaboration[i]
        name_variables[j] = name_prop_Colaboration[i]
        j = j + 1
    len_4 = len(name_prop_Colaboration)
    
    # principle 5
    weight_proper_princ5 = weight_principle / 1
    # Polycentric governance
    # all variables
    name_prop_Governance = np.concatenate((name_IntCom, name_mv_modificada, name_mv_AirQ, name_mv_NoiseAte_d))
    data_prop_Governance = all_normalized_variables.loc[:, name_prop_Governance]
    num_var_governance = len(name_prop_Governance)
    weight_var_proper1_princ5 = weight_proper_princ5 / num_var_governance
    
    for i in range(len(name_prop_Governance)):
        y = np.array(data_prop_Governance.loc[:, name_prop_Governance[i]])
        x = np.array(time.loc[:, name_year])
        x = x.reshape(len(x),)
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        xx_mean_yy_mean = sum((x - x_mean) * (y - y_mean))
        xx_mean2 = sum((x - x_mean) ** 2)
        b1 = xx_mean_yy_mean / xx_mean2
        if b1 == 0:
            indicators[0][j] = y[0]
            weigths[j] = weight_var_proper1_princ5
        else:
            indicators[0][j] = b1
            weigths[j] = weight_var_proper1_princ5
        name_variables_indicator[j] = "Pendiente de la variable - " + name_prop_Governance[i]
        name_variables[j] = name_prop_Governance[i]
        j = j + 1
    len_5 = len(name_prop_Governance)
    
    data_variables = all_normalized_variables.loc[:, name_variables]
    data_variables_line = np.array(data_variables)
    
    name_indicator = np.array(['Indice de resiliencia'])
    resilience_indicator = [None for x in range(len(time))]
    for i in range(len(time)):
        line = np.array(data_variables_line[i][:])
        pond = weigths * line
        pond_princ_1 = np.sum(pond[0:len_1] * weigths[0:len_1])
        pond_princ_2 = np.sum(pond[len_1:len_1 + len_2] * weigths[len_1:len_1 + len_2])
        pond_princ_3 = np.sum(pond[len_1 + len_2:len_1 + len_2 + len_3] * weigths[len_1 + len_2:len_1 + len_2 + len_3])
        pond_princ_4 = np.sum(pond[len_1 + len_2 + len_3:len_1 + len_2 + len_3 + len_4] * weigths[len_1 + len_2 + len_3:len_1 + len_2 + len_3 + len_4])
        pond_princ_5 = np.sum(pond[len_1 + len_2 + len_3 + len_4:len_1 + len_2 + len_3 + len_4 + len_5] * weigths[len_1 + len_2 + len_3 + len_4:len_1 + len_2 + len_3 + len_4 + len_5])
        resilience_indicator[i] = pond_princ_1 + pond_princ_2 + pond_princ_3 + pond_princ_4 + pond_princ_5
    
    resi_indicator_DF = pd.DataFrame(resilience_indicator, columns=name_indicator).apply(pd.to_numeric)
    indicators_DF = pd.DataFrame(indicators, columns=name_variables_indicator).apply(pd.to_numeric)
    
    normalized_variables_order = np.array(all_normalized_variables.loc[:, name_variables])
    name_normalized_variables_order = [None for x in range(len(name_variables))]
    for i in range(len(name_variables)):
        name_normalized_variables_order[i] = name_variables[i] + " (normalizada)"
        
    normalized_variables_order = pd.DataFrame(normalized_variables_order, columns=name_normalized_variables_order).apply(pd.to_numeric)
    
    output_indicator = pd.concat([indicators_DF, normalized_variables_order, resi_indicator_DF], axis = 1)
    return output_indicator
        
       
    
    
    
    
    