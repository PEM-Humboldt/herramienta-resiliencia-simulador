

def health_index(t0, ti, t, dhealth, FunDiv, num_FunDiv, WaterQualityIndex, NoiseAttenuation, AirQualityIndex, InProvAliCobi):
    Long_vias = dhealth[0, 1]
    vias_poten = dhealth[1, 1]
    Num_UPA = dhealth[2, 1]
    Num_UPA_AutCons = dhealth[3, 1]
    Ind_pobreza = dhealth[4, 1]
    p_transitividad = dhealth[5, 1]
    
    ViasPotenAnual = p_transitividad * (Long_vias + (vias_poten / (t[-1] - t0)) * (ti - t0))
    
    if Long_vias / (Long_vias + vias_poten) <= 1:
        Con_Acces = 1 - Long_vias / ((Long_vias + ViasPotenAnual))
    else:
        Con_Acces = 0
    

    Autoconsumo = Num_UPA_AutCons / Num_UPA
    
    Div_Sis_Alim_Loc = (Autoconsumo + Con_Acces + FunDiv/ num_FunDiv + InProvAliCobi)  / 4
    
    HealthIndex = ((Div_Sis_Alim_Loc + AirQualityIndex + WaterQualityIndex + NoiseAttenuation) ** (1-Ind_pobreza))/4
    
    return HealthIndex, Div_Sis_Alim_Loc, Con_Acces