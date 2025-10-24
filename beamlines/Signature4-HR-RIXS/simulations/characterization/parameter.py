import os
import numpy as np
import pandas as pd
from pathlib import Path

# Standard Simulation Parameters
this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu    = 30
nrays   = 1e6
rounds  = 2
HRRIXS_energy = np.arange(150, 2101, 25)  # eV


#   PARAMS HRRIXS 100 m with 400 l/mm
HRRIXS_100m_blaze_400_rml_file_name     = 'HRRIXS_100m_c5_400lpmm_Wolter_1_mono'
HRRIXS_100m_blaze_400_sim_name                           = HRRIXS_100m_blaze_400_rml_file_name
HRRIXS_100m_blaze_400_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_100m_blaze_400_rml_file_name+'.rml')
HRRIXS_400_cff = [1.6]
HRRIXS_400_slitsize = [20/1000] # in mm

#   PARAMS HRRIXS 100 m with 1200 l/mm
HRRIXS_100m_blaze_1200_rml_file_name     = 'HRRIXS_100m_c5_1200lpmm_Wolter_1_mono'
HRRIXS_100m_blaze_1200_sim_name                           = HRRIXS_100m_blaze_1200_rml_file_name
HRRIXS_100m_blaze_1200_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_100m_blaze_1200_rml_file_name+'.rml')
HRRIXS_1200_cff = [1.8, 5, 10]
HRRIXS_1200_slitsize = [20/1000, 5/1000, 2.5/1000] # in mm


#   PARAMS HRRIXS 100 m with 6000 l/mm
HRRIXS_100m_blaze_6000_rml_file_name     = 'HRRIXS_100m_c20_6000lpmm_Wolter_1_mono'
HRRIXS_100m_blaze_6000_sim_name                           = HRRIXS_100m_blaze_6000_rml_file_name
HRRIXS_100m_blaze_6000_file_path                          = os.path.join(Path(__file__).resolve().parents[2],
                                                     'rml',
                                                     HRRIXS_100m_blaze_6000_rml_file_name+'.rml')
HRRIXS_6000_cff = [20]
HRRIXS_6000_slitsize = [1/1000] # in mm


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

###################################################################################
#   grating 6000
gr6000_eff_path  = os.path.abspath(
                            os.path.join(Path(__file__).resolve().parents[4], 
                            'gratings',
                            'gr6000_HR-RIXS',
                            'Gr6000_k1_cff25.csv')
                            )
gr6000_eff = pd.read_csv(gr6000_eff_path)