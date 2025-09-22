import numpy as np
import os
import pandas as pd


this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu   = 30
nrays  = 5e5
rounds = 10

big_step = 1
fine_step = 0.1


e1 = np.arange(100, 185, big_step)
e1_b = np.arange(50, 185, big_step)
e2 = np.arange(185, 195.1, fine_step)
e3 = np.arange(195, 570, big_step)
e4 = np.arange(570, 580.1, fine_step)
e5 = np.arange(580, 2035, big_step)
e5_b = np.arange(580, 1550, big_step)
e6 = np.arange(2038, 2042, fine_step)
e7 = np.arange(2045, 2501, big_step)



#   PARAMS FOR HB 1200l/mm GRATING SIMULATIONS
hb_1200_energy        = np.unique(np.concatenate([e1, e2, e3,
                                           e4, e5, e6,
                                           e7]))
hb_1200_SlitSize      = np.array([0.02])
hb_1200_cff           = np.array([2.25])
hb_1200_nrays         = nrays
hb_1200_rounds        = rounds
hb_1200_ncpu          = ncpu
hb_1200_sim_name      = '1200'
hb_1200_rml_file_name = 'HB_1200'
hb_1200_file_path     = os.path.join('rml/'+hb_1200_rml_file_name+'.rml')

#   PARAMS FOR HB 2400l/mm GRATING SIMULATIONS
ml_SlitSize        = np.array([0.02])
ml_nrays           = nrays
ml_rounds          = rounds
ml_ncpu            = ncpu
ml_sim_name        = '2400'
ml_rml_file_name   = 'HB_2400'
ml_rml_file_path   = os.path.join('rml/'+ml_rml_file_name+'.rml')


# ml_rml_file_path   = os.path.join('rml/'+ml_rml_file_name+'.rml')

grating = pd.read_csv('ML_eff/ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLbGR.dat',
                      sep='\s+')
mirror = pd.read_csv('ML_eff/ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLPM-max.dat',
                      sep='\s+')

ml_cff = grating['Cff'].to_numpy().flatten()#[::10]
ml_energy = grating['Energy'].to_numpy().flatten()#[::10]
if grating['Energy'].equals(mirror['Energy']):
    # If energy columns match, directly multiply
    efficiency = pd.DataFrame({
        'Energy[eV]': grating['Energy'],
        'Efficiency': grating['Efficiency(GR)'] * mirror['Efficiency(PM)']
    })
else:
    # Interpolate to a common energy range
    min_energy = max(grating['Energy'].min(), mirror['Energy'].min())
    max_energy = min(grating['Energy'].max(), mirror['Energy'].max())
    common_energy = np.linspace(min_energy, max_energy, num=1000)  # Define a common range

    grating_eff = np.interp(common_energy, grating['Energy'], grating['Efficiency(GR)'])
    mirror_eff = np.interp(common_energy, mirror['Energy'], mirror['Efficiency(PM)'])

    # Create a new DataFrame with interpolated values
    efficiency = pd.DataFrame({
        'Energy[eV]': common_energy,
        'Efficiency': grating_eff * mirror_eff
    })