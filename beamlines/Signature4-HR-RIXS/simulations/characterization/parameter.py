import os
import numpy as np
import pandas as pd
from pathlib import Path

# Standard Simulation Parameters
this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu    = 30
nrays   = 5e5
rounds  = 1
HRRIXS_energy = np.arange(150, 2101, 5)  # eV
HRRIXS_order   = 2  # diffraction order
HRRIXS_cff     = 25
HRRIXS_SlitSize = np.array([.0012])  # mm   #NOTE: each BL has its own slit size, where the RP is max without reducing FLUX
HRRIXS_grating  = np.array([3000])  # lines/mm



#   PARAMS HRRIXS 100 m Version SIMULATIONS
HRRIXS_100m_1_rml_file_name     = 'HRRIXS_100m_1'
HRRIXS_100m_1_sim_name                           = HRRIXS_100m_1_rml_file_name
HRRIXS_100m_1_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_100m_1_rml_file_name+'.rml')



#   PARAMS HRRIXS 100 m with blaze grating (250 mm) Version SIMULATIONS
HRRIXS_100m_1_blaze_rml_file_name     = 'HRRIXS_100m_blaze'
HRRIXS_100m_1_blaze_sim_name                           = HRRIXS_100m_1_blaze_rml_file_name
HRRIXS_100m_1_blaze_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_100m_1_blaze_rml_file_name+'.rml')



###################################################################################
#   PARAMS FOR Undulator BESSY III UE42.5 by smalerz
HRRIXS_undulator_file_path  = os.path.abspath(
                            os.path.join(Path(__file__).resolve().parents[4], 
                            'undulators',
                            'UndulatorFiles_BESSY_III',
                            'IVUE42',
                            'Elisa-IVUE42-HL-1.csv')
                            )
HRRIXS_undulator = pd.read_csv(HRRIXS_undulator_file_path)

