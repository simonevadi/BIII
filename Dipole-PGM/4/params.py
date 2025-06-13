import numpy as np
import os
import pandas as pd


this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu = 30


#   PARAMS FOR HB 1200l/mm GRATING SIMULATIONS
hb_1200_energy        = np.arange(50, 2551,5)
hb_1200_SlitSize      = np.array([0.1])
hb_1200_cff           = np.array([2.25])
hb_1200_nrays         = 1e5
hb_1200_rounds        = 5
hb_1200_ncpu          = ncpu
hb_1200_sim_name      = 'Dipole_PGM_1200'
hb_1200_rml_file_name = 'Dipole_PGM_1200'
hb_1200_file_path     = os.path.join('rml/'+hb_1200_rml_file_name+'.rml')

#   PARAMS FOR HB 400l/mm GRATING SIMULATIONS
hb_400_energy        = np.arange(50, 2551,5)
hb_400_SlitSize      = np.array([0.1])
hb_400_cff           = np.array([2.25])
hb_400_nrays         = 1e5
hb_400_rounds        = 5
hb_400_ncpu          = ncpu
hb_400_sim_name      = 'Dipole_PGM_400'
hb_400_rml_file_name = 'Dipole_PGM_400'
hb_400_file_path     = os.path.join('rml/'+hb_400_rml_file_name+'.rml')

#   PARAMS FOR HB 2400l/mm GRATING SIMULATIONS
ml_order           = 2
ml_index           = 'MLBG_mfm_second'
ml_table           = os.path.join('ML_eff', 'grating_eff_5000.xlsx')
ml_SlitSize        = np.array([0.1])
ml_grating         = np.array([2400])
ml_nrays           = 5e5
ml_rounds          = 5
ml_ncpu            = ncpu
ml_sim_name        = 'Dipole_PGM_2400_ML'
ml_rml_file_name   = 'Dipole_PGM_2400_ML'
ml_rml_file_path   = os.path.join('rml/'+ml_rml_file_name+'.rml')

# Extract efficiency from Andrey's data 
common_energy = None

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