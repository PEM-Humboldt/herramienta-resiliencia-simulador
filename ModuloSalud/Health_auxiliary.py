

def health_index(dhealth, FunDiv, num_FunDiv, WaterQualityIndex, NoiseAttenuation, AirQualityIndex, InProvAliCobi):
    Long_vias = dhealth[0, 1]
    vias_poten = dhealth[1, 1]
    Num_UPA = dhealth[2, 1]
    Num_UPA_AutCons = dhealth[3, 1]
    Ind_pobreza = dhealth[4, 1]
    Con_Acces = Long_vias / vias_poten
    Autoconsumo = Num_UPA_AutCons / Num_UPA
    
    Div_Sis_Alim_Loc = (Autoconsumo + Con_Acces + FunDiv/ num_FunDiv + InProvAliCobi)  / 3
    
    HealthIndex = (Div_Sis_Alim_Loc + (1-AirQualityIndex/500) + WaterQualityIndex + NoiseAttenuation) ** (1-Ind_pobreza)/4
    
    return HealthIndex, Div_Sis_Alim_Loc