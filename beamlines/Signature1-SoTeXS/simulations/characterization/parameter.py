import numpy as np
import os
import pandas as pd
from pathlib import Path


this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu = 30
nrays=1e6
rounds = 10

##########################################################################################
# UNDULATOR
undulator_file_path = os.path.abspath(
    os.path.join(Path(__file__).resolve().parents[4], 
                 'undulators',
                 'UndulatorFiles_BESSY_III',
                 'CPMU21_300mA_100pmrad_x_100pmrad.csv')
)

undulator = pd.read_csv(undulator_file_path)

<<<<<<< HEAD

# PARAMS FOR SOTEXS 1200l/mm GRATING SIMULATIONS 3 micron
e1   = np.arange(500, 2101,1)
e2   = np.arange(2100, 6001,25)
energy_1200 = np.concatenate((e1, e2))
=======
##########################################################################################
# PARAMS FOR SOTEXS 1200l/mm GRATING SIMULATIONS
energy_1200   = np.arange(500, 2101,1)
>>>>>>> 24c93ef (fix eval, prepare new sim)
SlitSize_1200 = np.array([.020]) # mm
cff_1200      = np.array([2.25])
sotexs_1200_sim_name = 'sotexs_1200_3micron'
sotexs_1200_file_name  = 'sotexs_1200_3micron'
sotexs_1200_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     sotexs_1200_file_name+'.rml')

<<<<<<< HEAD
# PARAMS FOR SOTEXS 2400l/mm GRATING SIMULATIONS 3 micron
=======
sotexs_1200_nano_sim_name = 'sotexs_1200_nano'
sotexs_1200_nano_file_name  = 'sotexs_1200_nano'
sotexs_1200_nano_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     sotexs_1200_nano_file_name+'.rml')
#########################################################################################
# PARAMS FOR SOTEXS 2400l/mm GRATING SIMULATIONS Multilayer CrC
>>>>>>> 24c93ef (fix eval, prepare new sim)
SlitSize_2400 = np.array([.020]) # mm
sotexs_2400_sim_name = 'sotexs_2400_3micron'
sotexs_2400_file_name  = 'sotexs_2400_3micron'
sotexs_2400_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     sotexs_2400_file_name+'.rml')

<<<<<<< HEAD
########################################################################################

# PARAMS FOR SOTEXS 2400l/mm GRATING SIMULATIONS 500nano
sotexs_2400_500nano_sim_name = 'sotexs_2400_500nano'
sotexs_2400_500nano_file_name  = 'sotexs_2400_500nano'
sotexs_2400_500nano_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     sotexs_2400_500nano_file_name+'.rml')
# PARAMS FOR SOTEXS 1200l/mm GRATING SIMULATIONS 500nano
sotexs_1200_500nano_sim_name = 'sotexs_1200_500nano'
sotexs_1200_500nano_file_name  = 'sotexs_1200_500nano'
sotexs_1200_500nano_file_path  = os.path.join(Path(__file__).resolve().parents[2],
=======
sotexs_2400_nano_sim_name = 'sotexs_2400_nano_CrC'
sotexs_2400_nano_file_name  = 'sotexs_2400_nano'
sotexs_2400_nano_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     sotexs_2400_nano_file_name+'.rml')



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
    

##########################################################################################
# PARAMS FOR SOTEXS 2400l/mm GRATING SIMULATIONS Multilayer NiB4C up to 8kev
SlitSize_2400_b = np.array([.020]) # mm
sotexs_2400_b_sim_name = 'sotexs_2400_ML_NiB4C'
sotexs_2400_b_file_name  = 'sotexs_2400'
sotexs_2400_b_file_path  = os.path.join(Path(__file__).resolve().parents[2],
>>>>>>> 24c93ef (fix eval, prepare new sim)
                                     'rml',
                                     sotexs_1200_500nano_file_name+'.rml')

<<<<<<< HEAD

############################################################################################

# PARAMS FOR SOTEXS 2400l/mm GRATING SIMULATIONS 200nano
sotexs_2400_200nano_sim_name = 'sotexs_2400_200nano'
sotexs_2400_200nano_file_name  = 'sotexs_2400_200nano'
sotexs_2400_200nano_file_path  = os.path.join(Path(__file__).resolve().parents[2],
=======
sotexs_2400_b_nano_sim_name = 'sotexs_2400_nano_ML_NiB4C'
sotexs_2400_b_nano_file_name  = 'sotexs_2400_nano'
sotexs_2400_b_nano_file_path  = os.path.join(Path(__file__).resolve().parents[2],
>>>>>>> 24c93ef (fix eval, prepare new sim)
                                     'rml',
                                     sotexs_2400_200nano_file_name+'.rml')





########################################################################################

# Multilayer efficiency
efficiency_path = os.path.join(Path(__file__).resolve().parents[4],
                                'multilayer_monochromator_efficiency',
                                'calculate_ml',
                                'Ni_B4C - 40 layers', 
                                'Ni_B4C_2400lmm_2order.csv')


<<<<<<< HEAD
efficiency_2400 = pd.read_csv(efficiency_path)
cff_2400    = efficiency_2400['cff'].to_numpy().flatten()
energy_2400 = efficiency_2400['Energy[eV]'].to_numpy().flatten()

=======
# ### plotting colors
# import matplotlib
# import matplotlib.pyplot as plt
# # Generate 20 colors from the 'hsv' colormap which resembles a rainbow
# colors_rainbow = plt.cm.tab20(np.linspace(0, 2, int(max(1,2))))
# # Convert the colors to hex format for easy usage
# colors = [matplotlib.colors.rgb2hex(color) for color in colors_rainbow]
# colors = ["Red", "Orange", "Green", "Blue", "Indigo", "Violet"]
>>>>>>> 24c93ef (fix eval, prepare new sim)
