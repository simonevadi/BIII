import numpy as np
import os
import pandas as pd
from pathlib import Path


this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu = 29
nrays=5e5
rounds = 10

# UNDULATOR
undulator_file_path = os.path.abspath(
    os.path.join(Path(__file__).resolve().parents[4], 
                 'undulators',
                 'UndulatorFiles_BESSY_III',
                 'Signature2-ELISA',
                 'Elisa-IVUE42-HL-1.csv')
)

undulator = pd.read_csv(undulator_file_path)


# PARAMS FOR elisa 1200l/mm GRATING SIMULATIONS 3 micron
energy_1200 = np.arange(200, 2101,10)
SlitSize_1200 = np.array([.020]) # mm
cff_1200      = np.array([2.25, 5])
elisa_1200_sim_name = 'elisa_1200'
elisa_1200_file_name  = 'elisa_1200'
elisa_1200_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     elisa_1200_file_name+'.rml')

# PARAMS FOR elisa 2400l/mm GRATING SIMULATIONS 3 micron
SlitSize_2400 = np.array([.020]) # mm
elisa_2400_sim_name = 'elisa_2400'
elisa_2400_file_name  = 'elisa_2400'
elisa_2400_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     elisa_2400_file_name+'.rml')






########################################################################################

# Multilayer efficiency
efficiency_path = os.path.join(Path(__file__).resolve().parents[4],
                                'multilayer_monochromator_efficiency',
                                'calculate_ml',
                                'ELISA - CrC - 40 layers', 
                                'CrC_efficiency.csv')


efficiency_2400 = pd.read_csv(efficiency_path)
efficiency_2400 = efficiency_2400[efficiency_2400['Energy[eV]']<=6000]
cff_2400    = efficiency_2400['cff'].to_numpy().flatten()
energy_2400 = efficiency_2400['Energy[eV]'].to_numpy().flatten()

