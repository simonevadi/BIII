import numpy as np
import os
import pandas as pd
from pathlib import Path


this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu = 30
nrays=2.5e5
rounds = 4

# UNDULATOR
undulator_file_path = os.path.abspath(
    os.path.join(Path(__file__).resolve().parents[4], 
                 'undulators',
                 'UndulatorFiles_BESSY_III',
                 'UE65_HL.csv') 
)

undulator = pd.read_csv(undulator_file_path)


# PARAMS FOR elisa 300l/mm GRATING SIMULATIONS 

energy_300 = np.arange(100, 1000,1)
SlitSize_300 = np.array([.010]) # mm
cff_300      = np.array([2.5])
nanoARPES_300_sim_name = 'nanoARPES_300'
nanoARPES_300_file_name  = 'nanoARPES'
nanoARPES_300_file_path  = os.path.join(Path(__file__).resolve().parents[2],
                                     'rml',
                                     nanoARPES_300_file_name+'.rml')

