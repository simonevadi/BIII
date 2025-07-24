import os
import numpy as np
import pandas as pd
from pathlib import Path

this_file_dir   = os.path.dirname(os.path.realpath(__file__))
ncpu    = 12
nrays   = 1e5
rounds  = 10

##############################################################
#   Beamline Parameters
#   PARAMS FOR BESSY II LoBeta 37 m PGM-Standard-BL SIMULATIONS
B2_LoBeta_energy            = np.arange(100, 2101,5)
B2_LoBeta_SlitSize          = np.array([.020]) # mm
B2_LoBeta_cff               = np.array([2.25])
B2_LoBeta_rml_file_name     = 'bessy2lo_37m_PGM_2Perc_coupl_1p5deg_1200l'
B2_LoBeta_sim_name          = B2_LoBeta_rml_file_name
B2_LoBeta_file_path         = os.path.join('rml_b2',
                                     B2_LoBeta_rml_file_name+'.rml')

#   PARAMS FOR BESSY II HiBeta 37 m PGM-Standard-BL SIMULATIONS
B2_HiBeta_energy            = np.arange(100, 2101,5)
B2_HiBeta_SlitSize          = np.array([.020]) # mm
B2_HiBeta_cff               = np.array([2.25])
B2_HiBeta_rml_file_name     = 'bessy2hi_37m_PGM_2Perc_coupl_1p5deg_1200l'
B2_HiBeta_sim_name          = B2_HiBeta_rml_file_name
B2_HiBeta_file_path         = os.path.join('rml_b2',
                                           B2_HiBeta_rml_file_name+'.rml')


##############################################################
#   Undulator Parameters
#   PARAMS FOR Undulator BESSY II LoBeta SIMULATIONS
B2_LoBeta_undulator_file_path         = os.path.join(Path(__file__).resolve().parents[4],
                                           'undulators', 
                                           'UndulatorFiles_BESSY_II', 
                                           'undulator_flux_curves_SPECTRA',
                                           'UE46_b2_LoBeta_2PercCoupl_2025_smalerz_300mA.txt')
B2_LoBeta_undulator = pd.read_csv(B2_LoBeta_undulator_file_path, sep='\t')


#   PARAMS FOR Undulator BESSY II HiBeta SIMULATIONS
B2_HiBeta_undulator_file_path         = os.path.join(Path(__file__).resolve().parents[4],
                                           'undulators', 
                                           'UndulatorFiles_BESSY_II', 
                                           'undulator_flux_curves_SPECTRA',
                                           'UE46_b2_HiBeta_2PercCoupl_2025_smalerz_300mA.txt')
B2_HiBeta_undulator = pd.read_csv(B2_HiBeta_undulator_file_path, sep='\t')


#   PARAMS FOR Undulator BESSY III SIMULATIONS
B3_undulator_file_path                = os.path.join(Path(__file__).resolve().parents[4],
                                           'undulators', 
                                           'UndulatorFiles_BESSY_III', 
                                           'undulator_flux_curves_SPECTRA',
                                           'UE42p5_b3_2PercCoupl_2025_smalerz_ver_300mA.csv')
B3_undulator = pd.read_csv(B3_undulator_file_path)