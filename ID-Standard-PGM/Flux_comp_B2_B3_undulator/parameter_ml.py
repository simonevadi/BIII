import numpy as np
import pandas as pd

# BESSY III:
rml_file_name_bessy3_long_56m_errors_on_ml      = 'bessy3_56m_PGM_2Perc_coupl_err_on0_75deg_2400l_V3'

# Paramter
order       = 2
SlitSize    = np.array([.020]) # mm
grating     = np.array([2400])
nrays       = 1e5
rounds      = 20
ncpu        = 12

grating = pd.read_csv('ML_eff/ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLbGR.dat',
                      sep='\s+')
mirror = pd.read_csv('ML_eff/ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLPM-max.dat',
                      sep='\s+')


cff    = grating['Cff'].to_numpy().flatten()[::10] # take every 10th value
energy = grating['Energy'].to_numpy().flatten()[::10] # take every 10th value

# Extract efficiency from Andrey's data 
common_energy = None

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

