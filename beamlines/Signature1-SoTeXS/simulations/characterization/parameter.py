import numpy as np
import os
import pandas as pd
from pathlib import Path


this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu = 30
nrays=1e5
rounds = 1

# UNDULATOR
undulator_file_path = os.path.abspath(
    os.path.join(Path(__file__).resolve().parents[4], 
                 'undulators',
                 'UndulatorFiles_BESSY_III',
                 'undulator_flux_curves_SPECTRA',
                 'UE42p5_b3_2PercCoupl_2025_smalerz_ver_300mA.csv')
)

undulator = pd.read_csv(undulator_file_path)


# PARAMS FOR SOTEXS 1200l/mm GRATING SIMULATIONS
energy_1200   = np.arange(500, 2101,1)
SlitSize_1200 = np.array([.020]) # mm
cff_1200      = np.array([2.25])
sotexs_1200_sim_name = 'sotexs_1200'
sotexs_1200_file_name  = 'sotexs_1200'
sotexs_1200_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     sotexs_1200_file_name+'.rml')

sotexs_1200_nano_sim_name = 'sotexs_1200_nano'
sotexs_1200_nano_file_name  = 'sotexs_1200_nano'
sotexs_1200_nano_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     sotexs_1200_file_name+'.rml')
# PARAMS FOR SOTEXS 2400l/mm GRATING SIMULATIONS
SlitSize_2400 = np.array([.020]) # mm
sotexs_2400_sim_name = 'sotexs_2400'
sotexs_2400_file_name  = 'sotexs_2400'
sotexs_2400_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     sotexs_2400_file_name+'.rml')

sotexs_2400_nano_sim_name = 'sotexs_2400_nano'
sotexs_2400_nano_file_name  = 'sotexs_2400_nano'
sotexs_2400_nano_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     sotexs_2400_file_name+'.rml')


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
cff_2400    = grating['Cff'].to_numpy().flatten()
energy_2400 = grating['Energy'].to_numpy().flatten()

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
    efficiency_2400 = pd.DataFrame({
        'Energy[eV]': common_energy,
        'Efficiency': grating_eff * mirror_eff
    })
    
    
### plotting colors
import matplotlib
import matplotlib.pyplot as plt
# Generate 20 colors from the 'hsv' colormap which resembles a rainbow
colors_rainbow = plt.cm.tab20(np.linspace(0, 2, int(max(1,2))))
# Convert the colors to hex format for easy usage
colors = [matplotlib.colors.rgb2hex(color) for color in colors_rainbow]
colors = ["Red", "Orange", "Green", "Blue", "Indigo", "Violet"]