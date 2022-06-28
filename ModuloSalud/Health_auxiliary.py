

def health_index(dhealth, LongVias, S, num_S, WaterQualityIndex, SoundPressureQualityIndex, AirQualityIndex):
    vias_poten = dhealth[0, 1]
    Con_fin = dhealth[1, 1]
    Num_UPA = dhealth[2, 1]
    Num_UPA_AutCons = dhealth[3, 1]
    Infra_estruc = dhealth[4, 1]
    Con_Acces = ((LongVias / vias_poten) + Con_fin) / 2
    Autoconsumo = Num_UPA_AutCons / Num_UPA
    Div_Sis_Alim_Loc = (Autoconsumo + Con_Acces + S / num_S) / num_S
    HealthIndex = (Div_Sis_Alim_Loc + AirQualityIndex + WaterQualityIndex) ** Infra_estruc / (1 + SoundPressureQualityIndex) 
    
    return HealthIndex
    