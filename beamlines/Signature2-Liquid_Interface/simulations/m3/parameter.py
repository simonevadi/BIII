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
                 'CPMU21_300mA_100pmrad_x_100pmrad.csv')
)

undulator = pd.read_csv(undulator_file_path)


# PARAMS FOR elisa 1200l/mm GRATING SIMULATIONS 3 micron
energy_1200 = 1000
SlitSize_1200 = np.array([10]) # mm
cff_1200      = np.array([2.25, 5, 10, 20, ])
elisa_1200_sim_name = 'elisa_1200_m3_radius'
elisa_1200_file_name  = 'elisa_1200_m3_radius'
elisa_1200_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     elisa_1200_file_name+'.rml')

