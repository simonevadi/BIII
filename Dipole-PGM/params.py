import numpy as np
import os

#   PARAMS FOR 1200l/mm GRATING SIMULATIONS
hb_1200_order       = 1
hb_1200_energy_flux = np.arange(50, 2551,100)
hb_1200_energy_rp   = np.arange(50, 2551,100)
hb_1200_SlitSize    = np.array([0.1])
hb_1200_grating     = np.array([1200])
hb_1200_blaze       = np.array([0.9])
hb_1200_cff         = np.array([2.25])
hb_1200_nrays_flux  = 1e5
hb_1200_nrays_rp    = 1e5 
hb_1200_rounds_flux = 1
hb_1200_rounds_rp   = 1
hb_1200_ncpu_flux   = 10
hb_1200_ncpu_rp     = 10

hb_1200_sim_name_flux = '1200_FLUX'
hb_1200_sim_name_rp   = '1200_RP'
hb_1200_rml_file_name = 'Dipole_PGM_1200'

this_file_dir   = os.path.dirname(os.path.realpath(__file__))
hb_1200_file_path   = os.path.join('rml/'+hb_1200_rml_file_name+'.rml')



#   PARAMS FOR ML 2400l/mm GRATING SIMULATIONS
ml_order        = 2
ml_index        = 'MLBG_mfm_second'
ml_table        = os.path.join('ML_eff', 'grating_eff_5000.xlsx')
ml_energy_flux  = np.arange(500, 5001,500)
ml_energy_rp    = np.arange(500, 5001,500)
ml_SlitSize     = np.array([0.1])
ml_grating      = np.array([2400])
ml_nrays_flux   = 1e5
ml_nrays_rp     = 1e5 
ml_rounds_flux  = 1
ml_rounds_rp    = 1
ml_ncpu_flux    = 10
ml_ncpu_rp      = 10

ml_sim_name_rp     = '2400_RP'
ml_sim_name_flux   = '2400_FLUX'
ml_rml_file_name   = 'Dipole_PGM_2400_ML'

this_file_dir      = os.path.dirname(os.path.realpath(__file__))
ml_rml_file_path   = os.path.join('rml/'+ml_rml_file_name+'.rml')