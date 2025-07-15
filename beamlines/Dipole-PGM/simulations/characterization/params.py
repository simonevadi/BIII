import numpy as np
import os
import pandas as pd
from pathlib import Path


this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu = 30
nrays=1e5
rounds = 1

#   PARAMS FOR HB 1200l/mm GRATING SIMULATIONS
hb_1200_energy        = np.arange(50, 2551,5)
hb_1200_SlitSize      = np.array([0.02])
hb_1200_cff           = np.array([2.25])
hb_1200_nrays         = nrays
hb_1200_rounds        = rounds
hb_1200_ncpu          = ncpu
hb_1200_sim_name      = 'Dipole_PGM_1200'
hb_1200_rml_file_name = 'Dipole_PGM_1200'
hb_1200_file_path     = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     hb_1200_rml_file_name+'.rml')

#   PARAMS FOR HB 400l/mm GRATING SIMULATIONS
hb_400_energy        = np.arange(50, 2551,5)
hb_400_SlitSize      = np.array([0.02])
hb_400_cff           = np.array([2.25])
hb_400_nrays         = nrays
hb_400_rounds        = rounds
hb_400_ncpu          = ncpu
hb_400_sim_name      = 'Dipole_PGM_400'
hb_400_rml_file_name = 'Dipole_PGM_400'
hb_400_file_path     = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml'
                                     ,hb_400_rml_file_name+'.rml')

#   PARAMS FOR HB 2400l/mm GRATING SIMULATIONS
ml_SlitSize        = np.array([0.02])
ml_nrays           = nrays
ml_rounds          = rounds
ml_ncpu            = ncpu
ml_sim_name        = 'Dipole_PGM_2400_ML'
ml_rml_file_name   = 'Dipole_PGM_2400_ML'
ml_rml_file_path   = os.path.join(Path(__file__).resolve().parents[2],
                                  'rml'
                                  ,ml_rml_file_name+'.rml')

# read grating and premirror efficiency
grating_eff_path = os.path.join(Path(__file__).resolve().parents[4],
                                'multilayer_monochromator_efficiency',
                                'ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLbGR.dat')
mirror_eff_path = os.path.join(Path(__file__).resolve().parents[4], 
                               'multilayer_monochromator_efficiency',
                               'ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLPM-max.dat')

grating = pd.read_csv(grating_eff_path,
                      sep='\s+')
mirror = pd.read_csv(mirror_eff_path,
                      sep='\s+')

# combine grating and pre-mirror efficiency, 
# interpolating if necessary, and save it in new dataframe called efficiency
ml_cff = grating['Cff'].to_numpy().flatten()
ml_energy = grating['Energy'].to_numpy().flatten()
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