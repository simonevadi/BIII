import os
import numpy as np
import pandas as pd
from pathlib import Path

# Standard Simulation Parameters
this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu    = 12
nrays   = 1e5
rounds  = 10

B3_hor_energy= np.arange(100, 2101,5)
B3_hor_SlitSize= np.array([.020]) # mm
B3_hor_cff= np.array([2.25])

#   PARAMS FOR BESSY III 56 m horPGM with M3_Paraboloid SIMULATIONS
B3_horPGM_M3_Para_56m_rml_file_name   = 'bessy3_56m_PGM_2Perc_coupl_0p75deg_1200l_hor_PGM_M3Paraboloid'
B3_M3Para_sim_name                           = B3_horPGM_M3_Para_56m_rml_file_name
B3_M3Para_file_path                           = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     B3_horPGM_M3_Para_56m_rml_file_name+'.rml')


#   PARAMS FOR BESSY III 56 m horPGM with M1M3_Paraboloid SIMULATIONS
B3_horPGM_M1M3_Para_56m_rml_file_name   = 'bessy3_56m_PGM_2Perc_coupl_0p75deg_1200l_hor_PGM_M1M3Paraboloid'
B3_M1M3_Para_sim_name                           = B3_horPGM_M1M3_Para_56m_rml_file_name
B3_M1M3_Para_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     B3_horPGM_M1M3_Para_56m_rml_file_name+'.rml')



#   PARAMS FOR Undulator BESSY III 56 m PGM-Standard Beamline SIMULATIONS
B3_undulator_file_path         = os.path.join(Path(__file__).resolve().parents[4],
                                           'undulators', 
                                           'UndulatorFiles_BESSY_III', 
                                           'undulator_flux_curves_SPECTRA',
                                           'UE42p5_b3_2PercCoupl_2025_smalerz_ver_300mA.csv')
B3_undulator = pd.read_csv(B3_undulator_file_path)



















import numpy as np

# Load in rml file 

# BESSY III:
rml_file_name_bessy3_56m_hor_PGM_M3Para   = 'bessy3_56m_PGM_2Perc_coupl_0p75deg_1200l_hor_PGM_M3Paraboloid'
rml_file_name_bessy3_56m_hor_PGM_M1M3Para = 'bessy3_56m_PGM_2Perc_coupl_0p75deg_1200l_hor_PGM_M1M3Paraboloid'


# Paramter
order       = 1
SlitSize    = np.array([.020]) # mm
grating     = np.array([1200])
cff         = np.array([2.25])

energy_flux = np.arange(100, 2101,5)

nrays_flux  = 1e5
nrays_rp    = 1e5

round_flux = 10

ncpu = 12
### plotting colors
import matplotlib
import matplotlib.pyplot as plt
# Generate 20 colors from the 'hsv' colormap which resembles a rainbow
colors_rainbow = plt.cm.tab20(np.linspace(0, 2, int(max(1,2))))
# Convert the colors to hex format for easy usage
colors = [matplotlib.colors.rgb2hex(color) for color in colors_rainbow]
colors = ["Red", "Orange", "Green", "Blue", "Indigo", "Violet"]