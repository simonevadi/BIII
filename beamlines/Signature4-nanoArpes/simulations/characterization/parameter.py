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
                 'UE42p5_b3_2PercCoupl_2025_smalerz_ver_300mA.csv') # this is not the correct undulator
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

