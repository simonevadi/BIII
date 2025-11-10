import numpy as np
import os
import pandas as pd
from pathlib import Path
from undulator.ivu28.spectra import ivu28_hl as undulator


this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu = 30
nrays=1e6
rounds = 10


# PARAMS FOR SOTEXS 1200l/mm GRATING SIMULATIONS 3 micron
e1   = np.arange(500, 2101,1)
e2   = np.arange(2100, 6001,25)
energy_1200 = np.concatenate((e1, e2))
SlitSize_1200 = np.array([.020]) # mm
cff_1200      = np.array([2.25])
sotexs_1200_sim_name = 'sotexs_1200_3micron'
sotexs_1200_file_name  = 'sotexs_1200_3micron'
sotexs_1200_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     sotexs_1200_file_name+'.rml')

# PARAMS FOR SOTEXS 2400l/mm GRATING SIMULATIONS 3 micron
SlitSize_2400 = np.array([.020]) # mm
sotexs_2400_sim_name = 'sotexs_2400_3micron'
sotexs_2400_file_name  = 'sotexs_2400_3micron'
sotexs_2400_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     sotexs_2400_file_name+'.rml')

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
                                     'rml',
                                     sotexs_1200_500nano_file_name+'.rml')


############################################################################################

# PARAMS FOR SOTEXS 2400l/mm GRATING SIMULATIONS 200nano
sotexs_2400_200nano_sim_name = 'sotexs_2400_200nano'
sotexs_2400_200nano_file_name  = 'sotexs_2400_200nano'
sotexs_2400_200nano_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     sotexs_2400_200nano_file_name+'.rml')





########################################################################################

# Multilayer efficiency
efficiency_path = os.path.join(Path(__file__).resolve().parents[4],
                                'multilayer_monochromator_efficiency',
                                'calculate_ml',
                                'Ni_B4C - 40 layers', 
                                'Ni_B4C_2400lmm_2order.csv')


efficiency_2400 = pd.read_csv(efficiency_path)
cff_2400    = efficiency_2400['cff'].to_numpy().flatten()
energy_2400 = efficiency_2400['Energy[eV]'].to_numpy().flatten()

