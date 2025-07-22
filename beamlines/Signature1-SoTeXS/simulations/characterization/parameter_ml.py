import os
import numpy as np
import pandas as pd

# BESSY III:
sotexs_2400 = 'sotexs_2400'

# Paramter
SlitSize    = np.array([.020]) # mm
grating     = np.array([2400])
nrays       = 1e5
rounds      = 10
ncpu        = 30


# Grating efficiency data
this_file_dir = os.path.dirname(os.path.abspath(__file__))
ml_eff_dir = os.path.normpath(os.path.join(this_file_dir, '..', '..', '..', '..', 'multilayer_monochromator_efficiency'))

grating = pd.read_csv(
    os.path.join(ml_eff_dir, 'ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLbGR.dat'),
    sep='\s+'
)
mirror = pd.read_csv(
    os.path.join(ml_eff_dir, 'ELISA_GR2400_2ord_ML-Cr-C_N60_d4.8nm_MLPM-max.dat'),
    sep='\s+'
)


# Extract Cff and energy from the grating data
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

